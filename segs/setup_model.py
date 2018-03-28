from keras import layers
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Input
from keras.layers.core import Dropout
from keras import initializers
from keras.models import Model


def xavier():
    """ a Xavier initializer

    :return: a Xavier initializer
    """
    return initializers.glorot_normal(seed=888)


def hyper_layer(layer_input, n_channel, drate=0.0, name=None):
    """ a hyper layer that represents a combination of all the layers in one level of the U-net.
        in this case, it contains 2 dropout layers and 2 convolutional layers

    :param layer_input:     input layer
    :param n_channel:       number of channels
    :param drate:           dropout rate
    :param name:            naming convention in each layer
    :return:                the output of this hyper layer
    """

    layer = Dropout(rate=drate, seed=888)(layer_input)
    layer = Conv2D(n_channel, (3, 3), strides=(1, 1), padding='same', activation='relu',
                   dilation_rate=1, kernel_initializer=xavier(), name=name+'_1')(layer)
    layer = Dropout(rate=drate, seed=777)(layer)
    layer_output = Conv2D(n_channel, (3, 3), strides=(1, 1), padding='same', activation='relu',
                          dilation_rate=1, kernel_initializer=xavier(), name=name+'_2')(layer)
    return layer_output


def box_unet(layer_input, n_class, n_base=16, drate=0.0, name=None):
    """ a typical U-net architecture

    :param layer_input:     input layer for the U-net model
    :param n_class:         number of classes in classification task
    :param n_base:          number of channels in the first level of U-net
    :param drate:           rate of dropout
    :param name:            naming convention in each layer
    :param return:          the output layer of the U-net model
    """

    layer_l1 = hyper_layer(layer_input, n_base, drate, name=name + '_1')
    layer_l2 = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid')(layer_l1)
    layer_l2 = hyper_layer(layer_l2, n_base * 2, drate, name=name + '_2')
    layer_l3 = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid')(layer_l2)
    layer_l3 = hyper_layer(layer_l3, n_base * 4, drate, name=name + '_3')

    layer_r2 = UpSampling2D(size=(2, 2))(layer_l3)
    layer_r2 = layers.concatenate([layer_r2, layer_l2], axis=-1)
    layer_r2 = hyper_layer(layer_r2, n_base * 2, drate, name=name + '_4')

    layer_r1 = UpSampling2D(size=(2, 2))(layer_r2)
    layer_r1 = layers.concatenate([layer_r1, layer_l1], axis=-1)
    layer_r1 = hyper_layer(layer_r1, n_base, drate, name=name + '_5')
    y_output_r1 = Conv2D(n_class, (1, 1), strides=(1, 1), padding='same', activation='softmax', name=name+'_out')(layer_r1)

    y_output = y_output_r1

    return y_output


def construct_model(input_size, n_class):
    """ a function to construct a model

    :param input_size:      size of input (e.g. (256, 256))
    :param n_class:         number of classes for classification
    :return:                a classification model
    """
    n_base = 16  # number of channels in the first level of U-net
    drate = 0.1  # dropout rate
    x_input = Input(shape=input_size + (1,))  # input image has only one channel
    y_output = box_unet(x_input, n_class=n_class, n_base=n_base, drate=drate, name='unet')

    model = Model(inputs=[x_input], outputs=[y_output])

    return model


