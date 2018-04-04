import time

import numpy as np
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt

from parsing import compile_all_data, parse_data_both
from experiment_threshold import find_min_errorpct


# -------------------------------------------------------------------- #
def main():
    time_start = time.time()

    img_size = (256, 256)

    # resultpath = 'model/'  # a directory to store model and some results

    data_list = compile_all_data(contour_type='both')  # a list feasible pairs (index, zslize)
    n_data = len(data_list)

    error_pct_all = np.zeros(shape=(n_data,))
    error_pct_best_all = np.zeros(shape=(n_data,))

    for i in range(0, n_data):
        index, zslice = data_list[i]
        img, mask_in, mask_out = parse_data_both(index=index, zslice=zslice)

        mask_myo = mask_out * (~mask_in)
        mask_bld = mask_in

        map_seg = np.zeros(shape=img_size)
        map_seg[mask_myo] = 1
        map_seg[mask_bld] = 2

        error_pct_best, _, _, _ = find_min_errorpct(img=img, mask1=mask_myo, mask2=mask_bld)
        error_pct_best_all[i] = error_pct_best

        threshold = threshold_otsu(img[mask_out>0])
        mask_myo_threshold = (img <= threshold) * mask_out
        mask_bld_threshold = (img > threshold) * mask_out

        map_seg_threshold = np.zeros(shape=img_size)
        map_seg_threshold[mask_myo_threshold] = 1
        map_seg_threshold[mask_bld_threshold] = 2

        error = map_seg != map_seg_threshold
        error_pct = np.sum(error) / np.sum(mask_in)
        error_pct_all[i] = error_pct

    error_pct_best_all_mean = np.mean(error_pct_best_all)
    error_pct_all_mean = np.mean(error_pct_all)
    print("mean best error percentage is " + str(error_pct_best_all_mean))
    print("mean error percentage using Otsu algorithm is " + str(error_pct_all_mean))

    # plt.figure()
    # # plt.subplot(1,2,1)
    # plt.hist(error_pct_best_all, 5, density=True)
    # plt.title("best")
    # # plt.subplot(1,2,2)
    # plt.hist(error_pct_all, 5, density=True)
    # plt.title("Otsu algorithm")
    # plt.show()

    # -------------------------------------------------------------------- #
    time_elapsed = time.time() - time_start
    print("Time elapsed = %2.1f minutes" % (time_elapsed/60))


if __name__ == "__main__":
    main()
