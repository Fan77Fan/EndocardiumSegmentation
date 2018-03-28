import time

from keras.optimizers import Adam
from keras.utils import plot_model

from setup_model import construct_model
from setup_callbacks import construct_callbacks
from setup_lossfunctions import crossentropy2D
from setup_generator import generator_data
from parsing import compile_all_data


# -------------------------------------------------------------------- #
def main():
    time_start = time.time()

    n_epoch = 20
    n_step_train = 100
    batch_size = 8

    lr = 0.0001     # learning rate
    p_es = 10       # patience for early stopping
    img_size = (256, 256)

    resultpath = 'model/'  # a directory to store model and some results

    n_class = 2  # number of classes for classification

    data_list = compile_all_data()  # a list feasible pairs (index, zslize)

    # -------------------------------------------------------------------- #
    model = construct_model(input_size=img_size, n_class=n_class)
    model_optimizer = Adam(lr=lr)
    model.compile(loss=[crossentropy2D],
                  optimizer=model_optimizer)

    model.summary()
    plot_model(model, to_file=resultpath+'architecture'+'.png', show_shapes=True)

    model_callbacks = construct_callbacks(result_outputdir=resultpath, p_es=p_es)
    model_generator = generator_data(batch_size=batch_size, image_size=img_size, data_pool=data_list)
    model.fit_generator(generator=model_generator,
                        steps_per_epoch=n_step_train, epochs=n_epoch,
                        callbacks=model_callbacks)

    # -------------------------------------------------------------------- #
    time_elapsed = time.time() - time_start
    print("Time elapsed = %2.1f minutes" % (time_elapsed/60))


if __name__ == "__main__":
    main()
