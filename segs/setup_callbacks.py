from keras import callbacks

# ---------------------------------------------------------------------- #
def construct_callbacks(result_outputdir, p_es):
    model_callbacks = [
        callbacks.BaseLogger(),
        callbacks.History(),
        callbacks.ModelCheckpoint(filepath=result_outputdir + 'model', monitor='loss', mode='min', save_best_only=True),
        callbacks.EarlyStopping(monitor='loss', mode='max', min_delta=0.001, patience=p_es),
        # callbacks.ReduceLROnPlateau(monitor='loss', mode='min', factor=0.5, patience=10),
        callbacks.CSVLogger(filename=result_outputdir + 'training_log.csv', separator=',', append=False)
    ]
    return model_callbacks
