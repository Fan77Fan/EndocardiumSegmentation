"""Parsing code for DICOMS and contour files"""

import pydicom  # change dicom to pydicom
from pydicom.errors import InvalidDicomError

import numpy as np
from PIL import Image, ImageDraw
import csv


def parse_contour_file(filename):
    """ Parse the given contour filename

    :param filename:    filepath to the contourfile to parse
    :return:            list of tuples holding x, y coordinates of the contour
    """

    coords_lst = []

    with open(filename, 'r') as infile:
        for line in infile:
            coords = line.strip().split()

            x_coord = float(coords[0])
            y_coord = float(coords[1])
            coords_lst.append((x_coord, y_coord))

    return coords_lst


def parse_dicom_file(filename):
    """ Parse the given DICOM filename

    :param filename:        filepath to the DICOM file to parse
    :return:                dictionary with DICOM image data
    """

    try:
        dcm = pydicom.read_file(filename)
        # dcm = dicom.read_file(filename)
        dcm_image = dcm.pixel_array

        try:
            intercept = dcm.RescaleIntercept
        except AttributeError:
            intercept = 0.0
        try:
            slope = dcm.RescaleSlope
        except AttributeError:
            slope = 0.0

        if intercept != 0.0 and slope != 0.0:
            dcm_image = dcm_image * slope + intercept
        dcm_dict = {'pixel_data' : dcm_image}
        return dcm_dict
    except InvalidDicomError:
        return None


def poly_to_mask(polygon, width, height):
    """ Convert polygon to mask

    :param polygon:         list of pairs of x, y coords [(x1, y1), (x2, y2), ...] in units of pixels
    :param width:           scalar image width
    :param height:          scalar image height
    :return:                Boolean mask of shape (height, width)
    """

    # http://stackoverflow.com/a/3732128/1410871
    img = Image.new(mode='L', size=(width, height), color=0)
    ImageDraw.Draw(img).polygon(xy=polygon, outline=0, fill=1)
    mask = np.array(img).astype(bool)
    return mask


def link_file(index):
    """ return the corresponding patient_id and original_id given an index

    :param index:   the index of files (e.g. 3)
    :return:        if index is feasible, return (patient_id, original_id);
                    if not feasible, return (None, None).
    """

    index = index + 1  # to skip the headers in csv
    csv_name = 'final_data/link.csv'

    csv_file = open(csv_name, 'r')
    reader = csv.DictReader(csv_file)
    for row in reader:
        if reader.line_num is index:
            # print(row['patient_id'], row['original_id'])
            csv_file.close()
            return row['patient_id'], row['original_id']

    csv_file.close()
    return None, None


# TODO: separate file exist testing and reading
def parse_data(index, zslice, contour_type='in'):
    """ return the a pair of 2D image and its contour

    :param index:           the index of files (e.g. 1, 2, 3, 4, 5)
    :param zslice:          the number of slice in z axis
    :param contour_type:    type of contour to output ('in' or 'out')
    :return:                if (index, zslice) is feasible, return (image, boolean mask);
                            if not feasible, return (None, None).
    """

    patient_id, original_id = link_file(index)
    if patient_id and original_id is not None:
        try:
            dicom_datapath = 'final_data/dicoms/' + patient_id + '/'
            dicom_filename = str(zslice) + '.dcm'
            temp_dicom_file = dicom_datapath + dicom_filename
            temp_dicom_dct = parse_dicom_file(temp_dicom_file)
            temp_img = temp_dicom_dct['pixel_data']
            temp_size = temp_img.shape

            if contour_type is 'in':
                contour_datapath = 'final_data/contourfiles/' + original_id + '/i-contours/'
                contour_filename = 'IM-0001-' + "%04d" % zslice + '-icontour-manual.txt'
                temp_contour_file = contour_datapath + contour_filename
                temp_coord_list = parse_contour_file(temp_contour_file)
                contour = poly_to_mask(polygon=temp_coord_list, width=temp_size[0], height=temp_size[1])
            elif contour_type is 'out':
                contour_datapath = 'final_data/contourfiles/' + original_id + '/o-contours/'
                contour_filename = 'IM-0001-' + "%04d" % zslice + '-ocontour-manual.txt'
                temp_contour_file = contour_datapath + contour_filename
                temp_coord_list = parse_contour_file(temp_contour_file)
                contour = poly_to_mask(polygon=temp_coord_list, width=temp_size[0], height=temp_size[1])
            else:
                raise Exception("Invalid argument contour_type.")

            return temp_img, contour
        except FileNotFoundError:
            return None, None
    else:
        return None, None


def parse_data_both(index, zslice):
    """ return the a pair of 2D image and its contour

    :param index:           the index of files (e.g. 1, 2, 3, 4, 5)
    :param zslice:          the number of slice in z axis
    :return:                if (index, zslice) is feasible, return (image, boolean mask);
                            if not feasible, return (None, None).
    """

    patient_id, original_id = link_file(index)
    if patient_id and original_id is not None:
        try:
            dicom_datapath = 'final_data/dicoms/' + patient_id + '/'
            dicom_filename = str(zslice) + '.dcm'
            temp_dicom_file = dicom_datapath + dicom_filename
            temp_dicom_dct = parse_dicom_file(temp_dicom_file)
            temp_img = temp_dicom_dct['pixel_data']
            temp_size = temp_img.shape

            contour_datapath = 'final_data/contourfiles/' + original_id + '/i-contours/'
            contour_filename = 'IM-0001-' + "%04d" % zslice + '-icontour-manual.txt'
            temp_contour_file = contour_datapath + contour_filename
            temp_coord_list = parse_contour_file(temp_contour_file)
            contour_in = poly_to_mask(polygon=temp_coord_list, width=temp_size[0], height=temp_size[1])

            contour_datapath = 'final_data/contourfiles/' + original_id + '/o-contours/'
            contour_filename = 'IM-0001-' + "%04d" % zslice + '-ocontour-manual.txt'
            temp_contour_file = contour_datapath + contour_filename
            temp_coord_list = parse_contour_file(temp_contour_file)
            contour_out = poly_to_mask(polygon=temp_coord_list, width=temp_size[0], height=temp_size[1])

            return temp_img, contour_in, contour_out
        except FileNotFoundError:
            return None, None, None
    else:
        return None, None, None


def compile_all_data(contour_type='in'):
    """ A simple function to return a list of feasible pairs (index, zslice) in the data.
        It searches through all combinations of (index, zslice) brutally.

    :param contour_type:    type of contour to output ('in', 'out', or 'both')
    :return:                a list of feasible tuple pairs (index, zslice) in the data
    """

    data_all = []

    for i in range(1, 5 + 1):  # there are five folders in our dataset
        for j in range(1, 260 + 1):  # the maximal zslice is 260
            if contour_type is 'both':
                _, contour_in, contour_out = parse_data_both(index=i, zslice=j)
                if contour_out is not None:
                    data_all.append((i, j))
            elif contour_type in ('in', 'out'):
                _, contour = parse_data(index=i, zslice=j, contour_type=contour_type)
                if contour is not None:
                    data_all.append((i, j))
            else:
                raise Exception("Invalid argument contour_type.")
    return data_all


