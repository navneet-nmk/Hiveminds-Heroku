from flask import Flask
import requests
from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def load_and_return():
    # Declaration of constants
    MAX_SEQUENCE_LENGTH = 1000
    MAX_NB_WORDS = 20000
    bali_data = pd.read_csv("36 Hours in Bali - The New York Times.csv", names=['Activity', 'Description'])
    baltimore_data = pd.read_csv("36 Hours in Baltimore - The New York Times.csv", names=['Activity', 'Description'])
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    descriptions  = bali_data['Description']
    bali_predictions = []
    for text in descriptions:
        text = np.array([text.lower()])
        tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
        tokenizer.fit_on_texts(text)
        sequence = tokenizer.texts_to_sequences(text)
        data = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH)
        prediction = loaded_model.predict(np.array(data))
        bali_predictions.append(prediction)
    bali_diffs = []
    for p in bali_predictions:
        pos = p[0][0]
        neg = p[0][1]
        bali_diffs.append(pos-neg)
    bali_data['Sentiment'] = bali_diffs
    bali_data = bali_data.sort('Sentiment', ascending=False)
    print(bali_data.head())
    final_string  = "Top 5 attractions of bali are : \n"
    for att in bali_data['Activity'].head(5):
        final_string  += att + "\n"
    return final_string




if __name__ == '__main__':
    app.run()
