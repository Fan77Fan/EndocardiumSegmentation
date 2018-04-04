## EndocardiumSegmentation phase 2
Segmentation of endocardium in 2D MR images


### Part 1: Parse the o-contours

#### 1) Using your code from Phase 1, add the parsing of the o-contours into your pipeline. Note that there are only half the number of o-contour files as there are i-contour files, so not every i-contour will have a corresponding o-contour. After building the pipeline, please discuss any changes that you made to the pipeline you built in Phase 1, and why you made those changes.

The first change was to add 'contour_type' argument to function __parse_data__ in order to control whether the function outputs a pair of (image, in-contour) or (image, out-contour). The argument value is default to 'in' in order to add compatibility with codes using the previous version where 'contour_type' input is absent.

The second change is to add __parse_data_both__ function to fulfill the functionality of outputting three data types at the same time, meaning (image, in-contour, out-contour). This function is only used in the part 2 experimentations (__experiment_threshold.py__ and __main_threshold.py__), but not in the part 1 machine learning pipeline (__main.py__).

The last change is to add 'contour_type' input in __compile_all_data__, __setup_generator__, and __main__ where __parse_data__ function is called.


### Part 2: Heuristic LV Segmentation approaches

#### 1) Let’s assume that you want to create a system to outline the boundary of the blood pool (i-contours), and you already know the outer border of the heart muscle (o-contours). Compare the differences in pixel intensities inside the blood pool (inside the i-contour) to those inside the heart muscle (between the i-contours and o-contours); could you use a simple thresholding scheme to automatically create the i-contours, given the o-contours? Why or why not? Show figures that help justify your answer.

First, we design a metric called error percentage to measure how accurate the i-contour estimation is. It is defined as the number of misclassification pixels over total number of pixels inside the region of interest, namely o-contour mask.

**Eq.1: error_pct = N_error / N_total**

Given an arbitrary global threshold T to classify myocardium and blood pool for each image, we can calculate the error percentage associated with that threshold T. Hence, given an image and knowing the ground truth classification of the two classes, we can calculate a curve error_pct(T) as a function of T, and calculate the minimal error percentage. This is a theoretical lower bound of error percentage, namely, the best possible solution we can get using a single thresholding scheme.

**Eq.2: error_pct_best = min( error_pct(T) )**

To give an example (__experiment_threshold.py__), we select the data pair #2 (SCD0000201, SC-HF-I-2) at slice 120. This is an illustration of images and masks for myocardium and blood pool:
  ![Alt text](segs/model/example_masks_gt.png?raw=true "Title")

This is an illustration of histograms of the two classes and the error percentage curve as a function of threshold T. The best possible error percentage is 18% in this case.
  ![Alt text](segs/model/experiment_hist_thresh_error.png?raw=true "Title")

We also tried a simple thresholding scheme using Otsu's method (https://en.wikipedia.org/wiki/Otsu%27s_method), implemented using toolkit **skimage.filters.threshold_otsu**. The method finds a threshold that minimizes a weighted sum of intra-class variance. As in this example, the error percentage is 29%. A result of this method is illustrated here:
  ![Alt text](segs/model/example_masks_otsu.png?raw=true "Title")

For a final comparison (__main_threshold.py__), we computed the error percentage in all images, both the theoretical lower bound __error_pct_best__ and the error percentage from the Otsu method. The result is 
```
mean best error percentage is 0.120835845404
mean error percentage using Otsu algorithm is 0.345768146028
```

In conclusion, we think using a global thresholding scheme to separate myocardium and blood pool is possible, as shown by the results that the best error percentage is around 12%. However, the implementation needs further deliberation. Ostu method, a simple algorithm available in open-source toolkits, may not generate satisfying results (35%).

#### 2) Do you think that any other heuristic (non-machine learning)-based approaches, besides simple thresholding, would work in this case? Explain

Based on the shape of the myocardium, my guess is that a level-set method may be able to generate good results. The smooth contour of the endocardium can be utilized as a shape prior to guide heuristic methods.


