# EndocardiumSegmentation
Segmentation of endocardium in 2D MR images


# Part 1: Parse the DICOM images and Contour Files

  ## 1) How did you verify that you are parsing the contours correctly?

  I used the link.csv to find the corresponding files. 
  I also visually inspected a random pair of image and mask.
  ![Alt text](segs/model/figure_1.png?raw=true "Title")

  ## 2) What changes did you make to the code, if any, in order to integrate it into our production code base? 

  I changed dicom package to pydicom package. 
  I also added three functions in the parsing.py to help streamlining the parsing process (__link_file__, __parse_data__, and __compile_all_data__)


# Part 2: Model training pipeline

  ## 1) Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?

  Yes. I added a function __compile_all_data__ in order to extract all the possible pairs of images and contours. This function search through all the files in the folder and output a list that contains tuples of image index and contour index.

  ## 2) How do you/did you verify that the pipeline was working correctly?

  In a preliminary test, I ran the pipeline (i.e. __main.py__) on a local machine and examine compile time and run time errors.

  ## 3) Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

  Yes. There should be a data I/O function for handling parsing tasks. The __compile_all_data__ function is fulfilling that functionality, but it will not be efficient if it were to handle large dataset. Second, the various unit test files (i.e. __parsing_test.py__) are not complete yet. 


# Output


```
Using TensorFlow backend.
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to                     
==================================================================================================
input_1 (InputLayer)            (None, 256, 256, 1)  0                                            
__________________________________________________________________________________________________
dropout_1 (Dropout)             (None, 256, 256, 1)  0           input_1[0][0]                    
__________________________________________________________________________________________________
unet_1_1 (Conv2D)               (None, 256, 256, 16) 160         dropout_1[0][0]                  
unet_3_2 (Conv2D)               (None, 64, 64, 64)   36928       dropout_6[0][0]                  
unet_5_1 (Conv2D)               (None, 256, 256, 16) 6928        dropout_9[0][0]                  
......
__________________________________________________________________________________________________
unet_5_2 (Conv2D)               (None, 256, 256, 16) 2320        dropout_10[0][0]                 
__________________________________________________________________________________________________
unet_out (Conv2D)               (None, 256, 256, 2)  34          unet_5_2[0][0]                   
==================================================================================================
Total params: 118,002
Trainable params: 118,002
Non-trainable params: 0
```


```
100/100 [==============================] - 9s 94ms/step - loss: 0.2157
Epoch 2/20
100/100 [==============================] - 7s 74ms/step - loss: 0.1251
Epoch 3/20
100/100 [==============================] - 7s 73ms/step - loss: 0.1228
......
Epoch 13/20
100/100 [==============================] - 7s 72ms/step - loss: 0.1235
Epoch 14/20
100/100 [==============================] - 7s 72ms/step - loss: 0.1218
Time elapsed = 1.8 minutes

```


