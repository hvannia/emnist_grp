import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def getTrainSet():
    train = pd.read_csv('data/emnist-balanced-train.csv', header=None)
    train.head()
    train_data = train.iloc[:, 1:]  # do not use header column
    train_data = train_data.values  # make numpy matrix
    train_labels = train.iloc[:, 0] # header column only
    train_labels = pd.get_dummies(train_labels) # convert to 0s 1s
    train_labels.head() 
    train_labels = train_labels.values #make matrix
    del train
    return train_data,train_labels

def getTestSet():
    test = pd.read_csv('data/emnist-balanced-test.csv', header=None)
    test_data = test.iloc[:, 1:] # do not use header column   
    test_data = test_data.values
    test_labels = test.iloc[:, 0] # header column only
    test_labels = pd.get_dummies(test_labels)
    test_labels = test_labels.values
    del test
    return test_data,test_labels




class ImageHelper(object):
    def save_image(self, generated, epoch, directory):
        fig, axs = plt.subplots(5, 5)
        count = 0
        for i in range(5):
            for j in range(5):
                axs[i,j].imshow(generated[count, :,:,0], cmap='gray')
                axs[i,j].axis('off')
                count += 1
        fig.savefig("{}/{}.png".format(directory, epoch))
        plt.close()
        
    def make_gif(self, directory):
        filenames = np.sort(os.listdir(directory))
        filenames = [ fnm for fnm in filenames if ".png" in fnm]
    
        with imageio.get_writer(directory + '/image.gif', mode='I') as writer:
            for filename in filenames:
                image = imageio.imread(directory + filename)
                writer.append_data(image)