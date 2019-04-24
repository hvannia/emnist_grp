# preinstalls:
# tensorflow (using 1.13.1)
# scikit-image

import os
import io
import base64
import binascii
import PIL
import numpy as np

from skimage.feature import corner_harris, corner_peaks
from flask import Flask, request, jsonify, render_template

from keras.preprocessing import image
from keras.models import load_model

os.environ['KMP_DUPLICATE_LIB_OK']='True'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

cnnmodel = load_model('./static/models/cnnmodel.h5')
cnnmodel._make_predict_function()   # To mitigate ValueError when call predict

class_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'

def get_image(data) :
    img_io = io.BytesIO(base64.b64decode(data.decode().split(',')[1]))
    img_full = PIL.Image.open(img_io)
    #(8-bit pixels, black and white), 1 for 1bit b&w
    img_grey = img_full.convert(mode='L')  
    #resampling filter (map multiple input pixels to a single output pixel)
    #print('Img gr converted to 8bit',img_grey)



    img = img_grey.resize((28, 28), resample=PIL.Image.HAMMING)
    #print('img',img)
    img_array=np.asarray(img.getdata()).reshape(28,28)
    print('img as array 28x28 not yet normalized\n', img_array)
    #print('shape',img_array.shape)
    
    # FIND AREA W dwg
    sqsize=img_array.shape[0]
    minx = sqsize-1
    miny = sqsize-1
    maxx=0
    maxy=0

    for i in range(0,sqsize-1): 
        for j in range(0,sqsize-1): 
            if img_array[i,j]!=0: 
                if i < minx: 
                    minx=i 
                if i > maxx: 
                    maxx=i 
                if j< miny: 
                    miny=j 
                if j>maxy: 
                    maxy=j 
    #[]
    newarea=img_array[minx:maxx+1,miny:maxy+1]
    print('zoom area\n',newarea)
    print('new area shape: ',newarea.shape)
    #print('reshaped\n',newarea.reshape(28,28))

    #center shape
    startx=(sqsize-newarea.shape[0])//2
    
    starty=(sqsize-newarea.shape[1])//2
    print('new x:',startx)
    print('new y:',starty)
    newImg=np.zeros((28, 28))
    #square[2:8, 2:8] = 1
    
    #newImg[8:19,11:17]=newarea
    newImg[startx:startx+newarea.shape[0],starty:starty+newarea.shape[1]]=newarea
        
       # startx:startx+newarea.shape[0], starty:starty.shape[1]]=newImg
    print(newImg)






    img_arr = np.asarray(img.getdata()) / 255.0
    return img_arr.reshape([1,28,28,1])

def saveImageFile(data):
    image_data=data[22:] # remove image filetype info
    imgdata = base64.b64decode(image_data)
    filename = 'drawing.jpg'  
    with open(filename, 'wb') as f:
	    f.write(imgdata)

def preprocessImage(doodle):
    #save original as reference (temp)
    saveImageFile(doodle)
    #convert to array
    ppImage=get_image(doodle)
    return '' #preprocesedImage


@app.route('/mark', methods=['GET', 'POST'])
def upload_file_mark():
    print("In mark route")
    if request.method == 'POST':
        pimage2= preprocessImage(request.get_data())  # get ROI, 'zoom' and center
        pimage=get_image(request.get_data())
        #do prediction
        print("starting prediction... getting magic ball")
        pred = int(cnnmodel.predict_classes(pimage)[0])
        print(f'\n ************** Prediction : {pred} {class_map[pred]} \n\n')
        resp ="Predicted value: "+class_map[pred]
        return resp 

    nav_dict = {'home':'active', 'cnn':'not-active', 'dcgan':'not-active', 'about':'not-active'}
    return render_template('drawer.html', nav_dict = nav_dict)

@app.route('/', methods=['GET', 'POST'])
def iAmRoot():
    print("In /")
    nav_dict = {'home':'active', 'cnn':'not-active', 'dcgan':'not-active', 'about':'not-active'}
    return render_template('drawer.html', nav_dict = nav_dict)

@app.route('/dcgan')
def dcgan():
    print('In /dcgan')
    nav_dict = {'home':'not-active', 'cnn':'not-active', 'dcgan':'active', 'about':'not-active'}
    return render_template('dcgan.html', nav_dict = nav_dict)

@app.route('/cnn')
def cnn():
    print('In /cnn')
    nav_dict = {'home':'not-active', 'cnn':'active', 'dcgan':'not-active', 'about':'not-active'}
    return render_template('emnist_cnn.html', nav_dict = nav_dict)

if __name__ == "__main__":
    app.run(debug=True)



''' References
https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_corner.html#sphx-glr-auto-examples-features-detection-plot-corner-py

'''
