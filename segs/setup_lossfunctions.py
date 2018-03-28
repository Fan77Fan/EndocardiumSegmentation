from keras import backend


# ---------------------------------------------------------------------- #
def crossentropy2D(y_true, y_pred):
    ita = 0.001
    cross_entr = backend.sum(- y_true * backend.log(y_pred + ita), axis=-1)  # sum over class axis

    return cross_entr
