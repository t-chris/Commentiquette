# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import tensorflow as tf
import numpy as np
import pprint

def main():

    videoId = "RjriHA-MLPg"
    #Checking the length of characters to see if it's of ample size.
    texts = open("./youtube-api-parsing/txt-data/" + videoId + ".txt", 'rb').read().decode(encoding = 'utf-8')
    print('Length of text: {} characters'.format(len(texts)))
    
    #Get unique set of all words.
    word_set = sorted(set(texts))

    #Change characters to integer representation (idx)
    char_to_idx = {unique: idx for idx, unique in enumerate(word_set)}
    #Other way around.
    idx_to_char = np.array(word_set)

    #After saving our h5 model (weights and optimizer), we can load it in.
    titleName = videoId + '.h5'
    load_model = tf.keras.models.load_model(filepath='./models/' + titleName)

    load_model.build(tf.TensorShape([1, None]))

    load_model.summary()

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

    print(text_prediction(load_model, 'Melon'))


if __name__ == "__main__":
    main()