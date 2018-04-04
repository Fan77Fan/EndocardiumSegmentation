import numpy as np
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt

from parsing import compile_all_data, parse_data_both


# -------------------------------------------------------------------- #
def main():
    ''' a function to experiment the thresholding scheme.
        It compares the best possible threshold value with the one generated from Ostu's method.
    '''
    img_size = (256, 256)

    # resultpath = 'model/'  # a directory to store model and some results

    data_list = compile_all_data(contour_type='both')  # a list feasible pairs (index, zslize)
    # n_data = len(data_list)

    i = 12
    index, zslice = data_list[i]
    img, mask_in, mask_out = parse_data_both(index=index, zslice=zslice)

    mask_myo = mask_out * (~mask_in)
    mask_bld = mask_in

    map_seg = np.zeros(shape=img_size)
    map_seg[mask_myo] = 1
    map_seg[mask_bld] = 2

    img_myo = img * mask_myo
    img_bld = img * mask_bld

    plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(img_myo, cmap=plt.get_cmap('gray'), vmin=0, vmax=255)
    plt.title('image: myocardium')
    plt.subplot(2,2,2)
    plt.imshow(img_bld, cmap=plt.get_cmap('gray'), vmin=0, vmax=255)
    plt.title('image: blood pool')
    plt.subplot(2,2,3)
    plt.imshow(mask_myo, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
    plt.title('mask: myocardium')
    plt.subplot(2,2,4)
    plt.imshow(mask_bld, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
    plt.title('mask: blood pool')

    # -------------------------------------------------------------------- #
    error_pct_best, threshold_best, error_pct_all, bin_centers = find_min_errorpct(img=img, mask1=mask_myo, mask2=mask_bld)

    fig, ax1 = plt.subplots()
    ax1.hist(img_myo[mask_myo>0], 100, density=True, facecolor='r', alpha=0.5, label='myocardium')
    ax1.hist(img_bld[mask_bld>0], 100, density=True, facecolor='g', alpha=0.5, label='blood pool')
    ax1.set_xlabel('image intensity')
    ax1.set_ylabel('histogram')
    ax1.legend()
    ax2 = ax1.twinx()
    ax2.plot(bin_centers, error_pct_all, color='k')
    ax2.set_ylabel('error', color='k')
    fig.tight_layout()
    plt.show()

    print("best possible error percentage is " + str(error_pct_best))

    # -------------------------------------------------------------------- #
    threshold = threshold_otsu(img[mask_out>0])  # Ostu threshold
    mask_myo_threshold = (img <= threshold) * mask_out
    mask_bld_threshold = (img > threshold) * mask_out

    map_seg_threshold = np.zeros(shape=img_size)
    map_seg_threshold[mask_myo_threshold] = 1
    map_seg_threshold[mask_bld_threshold] = 2

    img_myo_threshold = img * mask_myo_threshold
    img_bld_threshold = img * mask_bld_threshold

    plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(img_myo_threshold, cmap=plt.get_cmap('gray'), vmin=0, vmax=255)
    plt.title('image: myocardium')
    plt.subplot(2,2,2)
    plt.imshow(img_bld_threshold, cmap=plt.get_cmap('gray'), vmin=0, vmax=255)
    plt.title('image: blood pool')
    plt.subplot(2,2,3)
    plt.imshow(mask_myo_threshold, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
    plt.title('mask: myocardium')
    plt.subplot(2,2,4)
    plt.imshow(mask_bld_threshold, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
    plt.title('mask: blood pool')
    plt.show()

    error = map_seg != map_seg_threshold
    error_pct = np.sum(error) / np.sum(mask_in)
    print("error percentage using Ostu algorithm is " + str(error_pct))

    plt.figure()
    plt.imshow(error, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)


# -------------------------------------------------------------------- #
def find_min_errorpct(img, mask1, mask2):
    """ a function to return the best possible threshold given an image and two masks

    :param img:     image
    :param mask1:   mask of myocardium (lower intensity)
    :param mask2:   mask of bloodpool (higher intensity)
    :return:    error_pct_min:  minimal error percentage at best possible threshold
                threshold:      best possible threshold
                error_pct_all:  an array that contains all error percentage
                bin_centers:    an array that contains all possible thresholds
    """

    max_value = np.max(img * (mask1 | mask2))
    bin_num = 100
    bin_edges = np.linspace(0, max_value, num=bin_num, endpoint=True, retstep=False, dtype=None)
    bin_centers = np.zeros(shape=(bin_num-1))
    for i in range(0, len(bin_centers)):
        bin_centers[i] = (bin_edges[i] + bin_edges[i+1]) / 2
    bin_counts_1, _ = np.histogram(img[mask1>0], bins=bin_edges)
    bin_counts_2, _ = np.histogram(img[mask2>0], bins=bin_edges)
    error_pct_all = np.zeros(shape=(bin_num-1,))
    n_total = np.sum(bin_counts_1) + np.sum(bin_counts_2)
    for i in range(0, bin_num-1):
        n_err_1 = np.sum(bin_counts_1[i:])
        n_err_2 = np.sum(bin_counts_2[0:i])
        error_pct_all[i] = (n_err_1 + n_err_2) / n_total
    min_ind = np.argmin(error_pct_all)
    threshold = bin_centers[min_ind]
    error_pct_min = error_pct_all[min_ind]
    return error_pct_min, threshold, error_pct_all, bin_centers


if __name__ == "__main__":
    main()