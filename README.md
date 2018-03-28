# EndocardiumSegmentation
Segmentation of endocardium in 2D MR images


Part 1: Parse the DICOM images and Contour Files

1) How did you verify that you are parsing the contours correctly?

I used the link.csv to find the corresponding files. 
I also visually inspected a random pair of image and mask.

![Alt text](segs/model/figure_1.png?raw=true "Title")

2) What changes did you make to the code, if any, in order to integrate it into our production code base? 

I changed dicom package to pydicom package. 
I also added three functions in the parsing.py to help streamlining the parsing process.


Part 2: Model training pipeline

1) Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?
2) How do you/did you verify that the pipeline was working correctly?
3) Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

