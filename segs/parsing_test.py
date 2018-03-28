import unittest
from os import listdir
from os.path import isfile, isdir, join

from parsing import *


class TestLinkFile(unittest.TestCase):
    def test_link(self):
        patient_id, original_id = link_file(5)
        self.assertEqual(patient_id, 'SCD0000501')
        self.assertEqual(original_id, 'SC-HF-I-6')

    def test_None(self):
        patient_id, original_id = link_file(6)
        self.assertEqual(patient_id, None)
        self.assertEqual(original_id, None)


# class TestMask(unittest.TestCase):
#     def test_isboolean(self):
#         contour_datapath = 'final_data/contourfiles/'
#         for dir in listdir(contour_datapath):
#             if isdir(join(contour_datapath, dir)):
#                 subdir = join(contour_datapath, dir, 'i-contours/')
#                 for file in listdir(subdir):
#                     if isfile(join(subdir, file)):
#                         select_contour = join(subdir, file)
#                         coord_list = parse_contour_file(select_contour)
#                         mask = poly_to_mask(polygon=coord_list, width=256, height=256)
#                         self.assertIsInstance(mask.all(), bool)


if __name__ == '__main__':
    unittest.main()



# index = 1
# zslice = 100

# def test_parse_contour_file(filename):

# dicom_datapath = 'final_data/dicoms/SCD0000101/'
# dicom_filename = str(zslice) + '.dcm'
#
# temp_dicom_file = rootpath + dicom_datapath + dicom_filename
# temp_dicom_dct = parse_dicom_file(temp_dicom_file)
# temp_img = temp_dicom_dct['pixel_data']
# temp_size = temp_img.shape
#
# contour_datapath = 'final_data/contourfiles/SC-HF-I-1/i-contours/'
# contour_filename = 'IM-0001-' + f'{zslice:04}' + '-icontour-manual.txt'
#
# temp_contour_file = rootpath + contour_datapath + contour_filename
# temp_coord_list = parse_contour_file(temp_contour_file)
# temp_contour = poly_to_mask(polygon=temp_coord_list, width=temp_size[0], height=temp_size[1])
#

# img, contour = parse_data(index=index, zslice=zslice)
# data_list = compile_all_data()

# plt.figure()
# plt.subplot(1,2,1)
# plt.imshow(img)
# plt.subplot(1,2,2)
# plt.imshow(contour)
