## EndocardiumSegmentation phase 2
Segmentation of endocardium in 2D MR images


### Part 1: Parse the o-contours

  #### 1) Using your code from Phase 1, add the parsing of the o-contours into your pipeline. Note that there are only half the number of o-contour files as there are i-contour files, so not every i-contour will have a corresponding o-contour. After building the pipeline, please discuss any changes that you made to the pipeline you built in Phase 1, and why you made those changes.

The first change was to add 'contour_type' argument to function __parse_data__ in order to control whether the function outputs a pair of (image, in-contour) or (image, out-contour). The argument value is default to 'in' in order to add compatibility with codes using the previous version where 'contour_type' input is absent.

The second change is to add __parse_data_both__ function to fulfill the functionality of outputting three data types at the same time, meaning (image, in-contour, out-contour)

The last change is to add 'contour_type' input in __compile_all_data__ and __main__ where __parse_data__ function is called.


### Part 2: Heuristic LV Segmentation approaches

  #### 1) Let’s assume that you want to create a system to outline the boundary of the blood pool (i-contours), and you already know the outer border of the heart muscle (o-contours). Compare the differences in pixel intensities inside the blood pool (inside the i-contour) to those inside the heart muscle (between the i-contours and o-contours); could you use a simple thresholding scheme to automatically create the i-contours, given the o-contours? Why or why not? Show figures that help justify your answer.



  #### 2) Do you think that any other heuristic (non-machine learning)-based approaches, besides simple thresholding, would work in this case? Explain
