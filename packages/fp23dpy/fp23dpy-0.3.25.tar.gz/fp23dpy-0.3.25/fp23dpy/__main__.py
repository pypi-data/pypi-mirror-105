"""
Main script for 3D reconstruction of Fringe Pattern images
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path as osp
from skimage import io, filters, morphology
from tqdm import tqdm

from . import Calibration
from . import Roi
from . import fp23d 
from . import export3D 
from .export import max_vertices
from . import helpers as h
from . import post_processing


def main():
    ### Open calibration instead if first argument is calibrate ###
    import sys
    if 'calibrate' in sys.argv:
        sys.argv.remove('calibrate')
        from .__calibrate_main__ import calibration_main
        calibration_main()
        exit()
    elif 'segment' in sys.argv:
        sys.argv.remove('segment')
        from .__segmentation_main__ import segmentation_main
        segmentation_main()
        exit()

    parser = argparse.ArgumentParser(description='3D reconstruct images with Fringe Patterns, use calibrate or segment arguments to show options for those operations.')
    parser.add_argument('files', type=str, nargs='+',
                        help='Input image files to reconstruct, files with prefix "reconstructed" and "segmented" will not be considered')
    parser.add_argument('--output', '-o', type=str,
                        help='Output file for the reconstructed 3D files, default is the same as the first input file')
    parser.add_argument('--prefix', type=str, default='reconstructed_',
                        help='Prefix of the reconstructed 3D files, default is "reconstructed_"')
    parser.add_argument('--ext', type=str, default='glb',
                        help='Output 3D file format, default is GL transmission format "glb"')
    # parser.add_argument('--ransac', action='store_true',
    #                     help='Use ransac to estimate a quadratic background carrier (currently not implemented).')
    parser.add_argument('--negative_theta', action='store_true',
                        help='If the camera is above or to the right of the projector this option should be used or a negative theta should be set in calibration file.')
    parser.add_argument('--with-texture', action='store_true',
                        help='Search for a texture file for output reconstruction with prefix "texture_" to file name.')
    parser.add_argument('--print-image', action='store_true',
                        help='Print each reconstruction as an image filed scaled for simple visualisation of the result, the pixel values will only correspond to relative reconstruction.')
    parser.add_argument('--print-image-cmap', type=str, default=None,
                        help='The matplotlib cmap used in the printing.')
    parser.add_argument('--print-image-gradient', action='store_true',
                        help='Take the gradient image of the visualisation before printing.')
    parser.add_argument('--print-npy', action='store_true',
                        help='Print each reconstruction as an numpy .npy file to later load into python, these files might be very large.')
    parser.add_argument('--print-ascii', '--print-csv', action='store_true',
                        help='Print each reconstruction as an ascii csv text file for later import into python, these files might be very large.')
    parser.add_argument('--print-roi', action='store_true',
                        help='Print the rectangle of interest used for the output (one for all).')
    parser.add_argument('--print-roi-each', action='store_true',
                        help='Print the rectangle of interest used for the output (one for each image).')
    parser.add_argument('--roi-file', type=str, default='roi.txt',
                        help='The name for the output roi file, default is "roi.txt"')
    parser.add_argument('--out-3D-size', type=float, default=None,
                        help='If scaling parameter is not used this is used to set half the size of the 3D structure')
    parser.add_argument('--max-vertices', type=int, default=max_vertices,
                        help='This will set the maximum nuber of vertices in the output 3D file.')
    parser.add_argument('--temporal-alignment', action='store_true',
                        help='Attempt to do an aligment of the third dimension for multiple reconstructions over time. Here, all input images must have the same shape. The first and second images can not be aligned for the current implementation.')
    args = parser.parse_args()
    method_args = ['negative_theta']
    d_args = {key: vars(args)[key] for key in method_args}

    # output_image_type = np.uint8

    ###### Manipulating input files ######
    to_reconstruct = args.files
    if osp.isdir(to_reconstruct[0]):
        input_dir = to_reconstruct[0]
        to_reconstruct = [f for f in os.listdir(input_dir) if h.is_image_file(f)]
    else:
        input_dir = osp.dirname(to_reconstruct[0])

    if len(to_reconstruct) > 0:
        to_reconstruct = [f for f in to_reconstruct if not 'calibrat' in f and not 'segment' in f and not 'reconstruct' in f]
    if len(to_reconstruct) == 0:
        print("No images found to reconstruct")
        exit()
    to_reconstruct = sorted(to_reconstruct)

    ###### Demodulation of files ######
    reconstructions = []
    for input_file in tqdm(to_reconstruct, disable=len(to_reconstruct) == 1):
        input_dir, input_filename = osp.split(input_file)
        input_filename_base, _ = osp.splitext(input_filename)
        if not osp.isfile(input_file):
            print("Warning: File {} not found".format(input_file))
            continue

        signal = io.imread(input_file, as_gray=True)

        calibration = h.get_calibration(input_file)
        if calibration is None:
            print("Warning: No calibration file found, using automatic calibration algorithm") 
            calibration = Calibration.calibrate(signal)
            print(calibration)

        segmentation = h.get_segmentation(input_file)
        if segmentation is None:
            roi = Roi.full(signal.shape)
        else:
            mask = ~segmentation
            signal = np.ma.array(signal, mask=mask, fill_value=0)
            roi = Roi.find_from_mask(mask)

        texture_file = osp.join(input_dir, input_filename_base + '_texture.png')
        texture = None
        if args.with_texture and osp.isfile(texture_file):
            texture = io.imread(texture_file)
            # texture = roi.apply(texture)

        name = '{}{}'.format(args.prefix, input_filename_base)
        grid3d = fp23d(signal, calibration, **d_args)
        reconstruction = {'filename': input_file, 'name': name, 'signal': signal, 'grid': grid3d, 'texture': texture, 'calibration': calibration, 'roi': roi}
        reconstructions.append(reconstruction)

        # post_processing of reconstruction
        if args.temporal_alignment:
            print("Temporal alignment")
            post_processing.temporal_alignment(reconstructions[-2:])
        
        if args.ext != "glb" and len(to_reconstruct) > 1:
            output_file = '{}.{}'.format(name, args.ext)
            export3D(output_file, reconstruction, args.out_3D_size, args.max_vertices, args.prefix)
            if len(reconstructions) > 2:
                # only keep results for temporal alignment
                reconstructions.pop(0)

        #### Possible extra prints for each reconstruction
        input_dir = osp.dirname(input_file)
        output_dir = input_dir if args.output is None else osp.dirname(args.output)

        if args.print_roi_each:
            roi.write(osp.join(output_dir, '{}_{}'.format(name, args.roi_file)))

        if args.print_roi_each or args.print_npy or args.print_image:
            grid3d_copy = grid3d.copy()
            if np.ma.isMaskedArray(grid3d_copy):
                grid3d_copy.data[grid3d_copy.mask] = np.nan
                grid3d_copy = grid3d_copy.data

            if args.print_npy:
                np.save(osp.join(output_dir, '{}.npy'.format(name)), grid3d_copy)

            if args.print_ascii:
                ascii_array = grid3d_copy.reshape((grid3d_copy.shape[1] * 3, grid3d_copy.shape[2]))
                np.savetxt(osp.join(output_dir, '{}.csv'.format(name)), ascii_array, fmt='%.3e')

            if args.print_image:
                # Only printing the image of the third dimension values to get a quick feel of the results
                threeD = grid3d_copy[2]
                vmax = None
                mask = np.isnan(threeD)
                if args.print_image_gradient:
                    # try to estimate gradient of image to find spikes
                    threeD = filters.scharr(threeD)
                    # this removes one pixel of the mask in all directions so compensate
                    threeD[np.isnan(threeD)] = 0
                    threeD = morphology.dilation(threeD, morphology.disk(1))
                    vmax = 0.3
                else:
                    threeD[mask] = 0
                output_file = osp.join(output_dir, '{}.png'.format(name))
                if args.print_image_cmap == "gray":
                    threeD = h.image_scaled(threeD, (0, 255), (None, vmax))
                    threeD[mask] = 0
                    io.imsave(output_file, threeD.astype(np.uint8), check_contrast=False)
                else:
                    plt.imsave(output_file, threeD, cmap=args.print_image_cmap, vmax=vmax)
        #######


    if args.ext == "glb" or len(to_reconstruct) == 1:
        # Deducing what output file to use
        if args.output is None:
            input_dir = osp.dirname(reconstructions[0]['filename'])
            output_file = osp.join(input_dir, '{}.{}'.format(reconstructions[0]['name'], args.ext))
        elif osp.isdir(args.output):
            output_file = osp.join(args.output, '{}.{}'.format(reconstructions[0]['name'], args.ext))
        else:
            output_file = args.output

        # Export all to the same 3D file
        export3D(output_file, reconstructions, args.out_3D_size, args.max_vertices, args.prefix)


if __name__ == '__main__':
    main()
