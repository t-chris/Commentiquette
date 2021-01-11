# Commentiquette
Inspired by Erik Hoffstad's Internet Comment Etiquette.

# Under the Hood
It's a simple RNN model built in Tensorflow and Keras, containing three layers: an Embedding layer, a GRU layer, and a hidden (dense) layer. It's trained on datasets I make myself using the Youtube V3 API for comments.
The whole thing is put in some funky Flask framework, and tied together with some glue and sticks at the end.

# Running it Locally
Literally just do `python app.py`

I plan to have a secure/personal front-end option for training models for new video that doesn't use the command line for simplicity's sake.
