import numpy as np
from parsing import parse_data


def generator_data(batch_size, image_size, data_pool, contour_type='in'):
    """ a generator for generating batches of training data

    :param batch_size:      size of each batch (e.g. 8)
    :param image_size:      size of input image (e.g. (256, 256))
    :param data_pool:       a list of feasible pairs (index, zslize). Output from parsing.compile_all_data().
    :return:                batch of training data
    """
    while True:
        [x, y] = random_image_sampling(batch_size=batch_size, image_size=image_size, data_pool=data_pool, contour_type=contour_type)

        yield (x, y)


def random_image_sampling(batch_size, image_size, data_pool, contour_type='in'):
    data_pool_size = len(data_pool)
    selected_item = np.random.choice(a=range(0, data_pool_size), size=batch_size)
    batch_x_img = np.zeros(shape=(batch_size,) + image_size + (1,))  # one channel per image
    batch_y_mask = np.zeros(shape=(batch_size,) + image_size + (2,))  # two channels per mask
    for i in range(0, batch_size):
        index, zslice = data_pool[selected_item[i]]
        img, mask = parse_data(index=index, zslice=zslice, contour_type=contour_type)
        batch_x_img[i, :, :, 0] = img
        batch_y_mask[i, :, :, 0] = mask
        batch_y_mask[i, :, :, 1] = ~mask

    return batch_x_img, batch_y_mask

