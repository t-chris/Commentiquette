# Commentiquette
Inspired by Erik Hoffstad's Internet Comment Etiquette.

# Under the Hood
It's a simple RNN model built in Tensorflow and Keras, containing three layers: an Embedding layer, a GRU layer, and a hidden (dense) layer. It's trained on datasets I make myself using the Youtube V3 API for comments.
The whole thing is put in some funky Flask framework, and tied together with some glue and sticks at the end.

# Running it Locally
Literally just do `python app.py`

As for currently model training yourself, start by moving to the youtube-api-parsing subdirectory (`cd youtube-api-parsing`) and changing the videoId to the video id of your choice (the string at the end of a YouTube URL). This will create a file that looks like `{your video id}.txt` in the appropriate folder.

After that, return to the main directory (`cd ..'`) and go to models.py and change the videoId to the same one used earlier and then run `python models.py`. You can always change the data, model, or # of epochs, etc. 100 takes a while, make sure you have a good CUDA-enabled GPU (not like me). This one should train the model using the data you created earlier (the .txt) and then save the trained model in `{your video id}.h5` in the appropraite folder.

At this point you're probably wondering how the videoId thing is pretty tedious. Yeah, don't think I didn't realize either.
I plan to have a secure/personal front-end option for this, that doesn't use a bunch of CLI and videoId manual changes.
