#!/usr/bin/env python3
import numpy as np
from skimage import filters, morphology, measure
from scipy.signal import convolve2d


from . import helpers
from . import demodulation


def ft2_segmentation(im, calibration):
    extracted_freq = np.abs(
        helpers.ft2_helper(im, calibration["T"], calibration["theta"], 70, 30)
    )

    minblurred = np.min(extracted_freq)
    cp = (extracted_freq - minblurred) / (np.max(extracted_freq) - minblurred)
    segmentation = (cp > 0.4).astype(np.uint8)

    selem = morphology.disk(10)
    segmentation = morphology.closing(segmentation, selem)
    segmentation = morphology.opening(segmentation, selem)
    # plt.subplot(121)
    # plt.imshow(cp)
    # plt.subplot(122)
    # plt.imshow(segmentation)
    # plt.show()
    return segmentation


def simple_segmentation(im, calibration):
    """ Using a high pass filter that is blurred and then threshold and some morphology """
    k_size = 2 * int(helpers.get_T_from_square(calibration["T"], im.shape)) + 1
    blurred = filters.gaussian(im, k_size)
    abs_hpf_im = np.abs(im - blurred)
    blurred2 = filters.gaussian(abs_hpf_im, k_size)
    minblurred = np.min(blurred2)
    cp = (blurred2 - minblurred) / (np.max(blurred2) - minblurred)
    segmentation = (cp > 0.2).astype(np.uint8)

    segmentation = morphology.opening(segmentation, morphology.disk(10))
    segmentation = morphology.erosion(segmentation, morphology.disk(2))
    # segmentation = morphology.closing(segmentation, morphology.disk(2))

    # plt.subplot(121)
    # plt.imshow(cp)
    # plt.subplot(122)
    # plt.imshow(segmentation)
    # plt.show()
    return segmentation


def simple_segmentation_improvement(
    im, calibration, segmentation, T_lims=None, min_island_size=50, min_hole_size=5
):
    """ Using the phase derivative to remove pixels from segmentation that are probably background """
    im = im.astype(float)

    im = np.ma.array(im, mask=~segmentation)

    if T_lims is None:
        T_lims = np.array([4, 2 * calibration["T"]])
    derivative_lims = (2 * np.pi / T_lims)[::-1]

    gamma = calibration["gamma"]
    y_kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) / 3 / 2
    x_kernel = y_kernel.T
    gamma_kernel = y_kernel * np.sin(gamma) + x_kernel * np.cos(gamma)

    phase = demodulation.demodulate(im, calibration)
    phase[~segmentation] = np.nan
    gamma_gradient = convolve2d(phase, gamma_kernel, "same", "fill", np.nan)

    temp_mask = np.isnan(gamma_gradient)
    edge_pixels = temp_mask & segmentation

    edge_coordinates = np.array(np.where(edge_pixels), dtype=int).T
    shape = temp_mask.shape
    for r, c in edge_coordinates:
        possible_neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for neighbour_coordinate in possible_neighbours:
            if (
                neighbour_coordinate[0] >= 0
                and neighbour_coordinate[0] < shape[0]
                and neighbour_coordinate[1] >= 0
                and neighbour_coordinate[1] < shape[1]
                and ~temp_mask[neighbour_coordinate]
            ):
                gamma_gradient[r, c] = gamma_gradient[neighbour_coordinate]
                break

    bad_pixels = (gamma_gradient < derivative_lims[0]) | (
        gamma_gradient > derivative_lims[1]
    )
    new_segmentation = segmentation & ~bad_pixels

    labels, n_labels = measure.label(new_segmentation, return_num=True, connectivity=1)
    for l in range(1, n_labels + 1):
        area = labels == l
        if np.sum(area) < min_island_size:
            new_segmentation[area] = False
    labels, n_labels = measure.label(~new_segmentation, return_num=True, connectivity=1)
    for l in range(1, n_labels + 1):
        area = labels == l
        if np.sum(area) < min_hole_size:
            new_segmentation[area] = True
    return new_segmentation


# import matplotlib.pyplot as plt
# from sklearn.mixture import GaussianMixture
# def gmm_phase_feature(
#     signal, calibration, segmentation=None, max_recursions=10
# ):
#     """ This is not only not working, it is super ugly coding aswell """
#     signal = signal.astype(float)
#     if segmentation is None:
#         # need a first guess of the segmentation
#         segmentation = np.ones(signal.shape, dtype=bool)
#     # segmentation = np.ones(signal.shape, dtype=bool)
#
#     # signal = np.ma.array(signal, mask=~segmentation)
#
#     gamma = calibration["gamma"]
#     T_lims = np.array([4, 2 * calibration["T"]])
#     derivative_lims = (2 * np.pi / T_lims)[::-1]
#     print(derivative_lims)
#
#     y_kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) / 3 / 2
#     x_kernel = y_kernel.T
#
#     gamma_kernel = y_kernel * np.sin(gamma) + x_kernel * np.cos(gamma)
#
#     i = 0
#     done = False
#     while not done and i < max_recursions:
#         phase, amplitude = demodulation.demodulate(signal, calibration, return_amplitude=True)
#         amplitude = helpers.image_scaled(amplitude, (0, 1), (0, None))
#
#         # phase[~segmentation] = np.nan
#         # amplitude[~segmentation] = np.nan
#
#         # y_gradient = convolve2d(phase, y_kernel, "same", "fill", np.nan)
#         # x_gradient = convolve2d(phase, x_kernel, "same", "fill", np.nan)
#         # gamma_gradient2 = y_gradient * np.sin(gamma) + x_gradient * np.cos(gamma)
#         gamma_gradient = convolve2d(phase, gamma_kernel, "same", "symm", np.nan)
#
#         # X = np.column_stack((gamma_gradient.flatten(), amplitude.flatten()))
#         # gmm = GaussianMixture(2).fit(X)
#         # labels = gmm.predict(X)
#
#         # plt.figure()
#         # plt.imshow(labels.reshape(signal.shape))
#
#         # plt.figure()
#         # plt.plot(gamma_gradient.flatten()[labels == 0], amplitude.flatten()[labels == 0], '*')
#         # plt.plot(gamma_gradient.flatten()[labels == 1], amplitude.flatten()[labels == 1], '*')
#
#         plt.figure()
#         plt.plot(gamma_gradient[~segmentation], amplitude[~segmentation], '*')
#         plt.plot(gamma_gradient[segmentation], amplitude[segmentation], '*')
#         plt.show()
#         exit()
#
#         new_segmentation = segmentation & (gamma_gradient > derivative_lims[0]) & (gamma_gradient < derivative_lims[1])
#         print(np.sum(new_segmentation) / new_segmentation.size)
#         # print(gamma_gradient[:3, :3])
#         # print(gamma_gradient2[:3, :3])
#         # exit()
#
#         plt.figure()
#         plt.imshow(amplitude)
#         plt.figure()
#         plt.imshow(gamma_gradient, vmin=derivative_lims[0], vmax=derivative_lims[1])
#         plt.figure()
#         plt.imshow(new_segmentation)
#         plt.show()
#         exit()
#
#         new_segmentation = segmentation
#         done = np.all(new_segmentation == segmentation)
#         done = True
#         i += 1
#         segmentation = new_segmentation
#
#     return segmentation
