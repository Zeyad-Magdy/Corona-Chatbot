# Part 1
import nltk 
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer() # stemmer used to reach the root of the word : whats -> what  , help?  -> help
import pickle
import numpy as np
import tflearn
#import tensorflow as tf
import random
import json



def chat(inp):
    training_model = True

    with open("intents-arabic.json",  encoding='utf8') as file:
        data = json.load(file)
        

    if(not training_model): 
        #make error here if you want to update
        with open("data.pickle","rb") as f:
            words, labels, training,output = pickle.load(f)
            

    else:
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])
            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        # Part 2        

        words = [stemmer.stem(w.lower()) for w in words if w != "?"] #stemmer and lowercase
        words = sorted(list(set(words))) #remove duplicates and list to return it as list and sort words

        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []
            wrds = [stemmer.stem(w.lower()) for w in doc] #stemmer and lowercase
            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        training =  np.array(training)
        output = np.array(output)

        # Part 3

        training = np.array(training)
        output = np.array(output)

        with open("data.pickle","wb") as f:
            pickle.dump((words, labels, training,output),f)
        

    #tf.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])

    net = tflearn.fully_connected(net, 320) #8 neurons
    net = tflearn.fully_connected(net, 160) #8 neurons
    net = tflearn.fully_connected(net, 80) #8 neurons
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax") 
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    
    if(not training_model):
        model.load("model.tflearn")
    else:    
        model.fit(training, output, n_epoch=2000, batch_size=32, show_metric=True)
        model.save("model.tflearn")
    
    while True:
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp,words)])[0]
        results_index = np.argmax(results) #Get Index of Max Prediction
        tag = labels[results_index]
        if results[results_index] > 0.7:  
            for tg in data["intents"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]
            response = random.choice(responses)
            return 0, response
        else:    
            response = "Sorry, I don't understand ! "
            return 0, response


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
               bag[i] = 1

    return np.array(bag)



    

        