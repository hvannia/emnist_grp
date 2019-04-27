#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:01:55 2019

@author: mflynn
"""

import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt

HEIGHT = 28
WIDTH  = 28

def rotate(image):
    image = image.reshape([HEIGHT, WIDTH])
    image = np.fliplr(image)
    image = np.rot90(image)
    return image

# Function to generate random set of indexes for image plots
def get_cat_index(cat_str, cat_arr, char=None, idx_cnt=40) :
    
    if char == None :
        # Compute random index array in images
        rtn_idx = np.random.randint(0, len(cat_arr), idx_cnt)
        
    else :
        # Compute random index array for category
        cat_idx = cat_str.find(char[0])
        if cat_idx == -1 : 
            cat_idx = cat_str.find(char[0].upper())
            if cat_idx == -1 :
                cat_idx = 0
        img_idx = np.arange(0,len(cat_arr))[cat_arr == cat_idx]
        rtn_idx = img_idx[np.random.randint(0, len(img_idx), idx_cnt)]
        
    return rtn_idx

# Function to plot 4 x 10 grid of images based on index array input
def plot_grid_40(cat_str, cat_arr, img_arr, plt_idx) :
    global test_x, idx_y, class_map
    plt.figure(figsize=(15, 8))
    for i in range(0,40):
        ax = plt.subplot(4, 10, i+1)
        ax.axis('off')
        plt.imshow(img_arr[plt_idx[i]], cmap=plt.get_cmap('gray'))
        plt.title(cat_str[cat_arr[plt_idx[i]]])
    return plt