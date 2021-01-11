# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import tensorflow as tf
import numpy as np
import pprint

#I probably don't intend on letting this script be runnable through Flask.
def main():
    videoId = "ivCY3Ec4iaU"
    #Checking the length of characters to see if it's of ample size.
    texts = open("./youtube-api-parsing/txt-data/" + videoId + ".txt", 'rb').read().decode(encoding = 'utf-8')
    print('Length of text: {} characters'.format(len(texts)))
    
    #Get unique set of all words.
    word_set = sorted(set(texts))
    print('{} unique chars'.format(len(word_set)))

    #Change characters to integer representation (idx)
    char_to_idx = {unique: idx for idx, unique in enumerate(word_set)}
    #Other way around.
    idx_to_char = np.array(word_set)

    text_as_int = np.array([char_to_idx[char] for char in texts])

    #Time to start sectioning the text file. 
    seq_length = 100
    #The +1 comes from inputting a character and trying to predict subsequent characters.
    data_per_epoch = len(texts)//(seq_length + 1)
    char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

    #Batching.
    sequences = char_dataset.batch(seq_length + 1, drop_remainder=True)

    def split_input_targ(chunk):
        input = chunk[:-1]
        target = chunk[1:]
        return input, target

    ds = sequences.map(split_input_targ)

    BATCH_SIZE = 64
    BUFFER_SIZE = 10000
    ds = ds.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
    word_set_size = len(word_set)
    embedding_dimensions = 256
    rnn_units = 1024

    #Building model.
    #Adding a GRU which serves as sort of an LSTM for RNNs.
    def build_model(word_set_size, embedding_dimensions, rnn_units, BATCH_SIZE):
        model = tf.keras.Sequential([ #Start with embedding layer since int -> reduced dim representation, orthogonal/no overlap.
            tf.keras.layers.Embedding( word_set_size, embedding_dimensions, batch_input_shape=[BATCH_SIZE, None]),
            tf.keras.layers.GRU(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
            tf.keras.layers.Dense(word_set_size)
        ])
        return model
    
    #We'll start building the model before training it.
    model = build_model(word_set_size, embedding_dimensions, rnn_units, BATCH_SIZE)

    #for input_ex_batch, target_ex_batch in ds.take(1):
    #    example_batch_pred = model( input_ex_batch )
    #    print(example_batch_pred.shape, '# (batch_size, seq_length, word_set_size)')
    
    model.summary()

    #Loss function.
    def loss_function(labels, logits):
        return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

    #Training the model!
    model.compile(optimizer='adam', loss=loss_function)

    checkpoint_directory = './training_checkpoint'
    #Keras will pass in the epoch param.
    checkpoint_prefix = os.path.join(checkpoint_directory, 'checkpoint_{epoch}')
    checkpoint_callbacks = tf.keras.callbacks.ModelCheckpoint(checkpoint_prefix, save_weights_only=True)
    epochs = 100

    history = model.fit(ds, epochs=epochs, callbacks=[checkpoint_callbacks])

    #since training our model, we'll save it via checkpoints
    model = build_model(word_set_size, embedding_dimensions, rnn_units, 1)

    model.load_weights(tf.train.latest_checkpoint(checkpoint_directory))

    model.build(tf.TensorShape([1, None]))

    model.summary()

    titleName = videoId + '.h5'
    model.save(filepath='./models/' + titleName, overwrite=True)

    def text_prediction(model, starting_string):
        num_generated = 1000
        input_evaluate = [char_to_idx[char] for char in starting_string]
        input_evaluate = tf.expand_dims(input_evaluate, 0)

        text_generated = []
        #Temperature determines predictability/unpredictability of text generated. Controls 'randomness', essentially.
        temperature = 1.0

        model.reset_states()

        for i in range(num_generated):
            pred = model(input_evaluate)
            pred = tf.squeeze(pred, 0)

            pred /= temperature
            pred_id = tf.random.categorical(pred, num_samples=1)[-1,0].numpy()
            
            input_evaluate = tf.expand_dims([pred_id], 0)
            text_generated.append(idx_to_char[pred_id])

        #Now, combine the starting_string to the generated predicted text.
        return (starting_string + ''.join(text_generated))

    print(text_prediction(model, 'K'))



if __name__ == "__main__":
    main()