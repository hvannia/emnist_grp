# preinstalls:
# tensorflow (using 1.13.1)
# scikit-image
# Pillow
import os
import io
import base64
import binascii
import PIL
import numpy as np
import datetime
#from jinja2 import Template

#from io import BytesIO
#from PIL import image
#from skimage.feature import corner_harris, corner_peaks
from flask import Flask, request, jsonify, render_template, session, redirect, url_for


from keras.preprocessing import image
from keras.models import load_model

os.environ['KMP_DUPLICATE_LIB_OK']='True'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
#app.config['SECRET_KEY'] = 'seeecretkey'

cnnmodel = load_model('./static/models/cnnmodel.h5')
cnnmodel._make_predict_function()   # To mitigate ValueError when call predict

class_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'

def get_image(data) :
    img_io = io.BytesIO(base64.b64decode(data.decode().split(',')[1]))
    img_full = PIL.Image.open(img_io)
    img_grey = img_full.convert(mode='L')  #(8-bit pixels, black and white)
    img = img_grey.resize((28, 28), resample=PIL.Image.HAMMING) #(map multiple input pixels to a single output pixel)
    img_array=np.asarray(img.getdata()).reshape(28,28)
    #print('img as array 28x28 not yet normalized\n', img_array)
    #print('shape',img_array.shape)
    img_arr = np.asarray(img.getdata()) / 255.0
    return img_arr.reshape([1,28,28,1])

def saveImageFile(data, filename):
    image_data=data[22:] # remove image filetype info
    imgdata = base64.b64decode(image_data)
    #filename = 'drawing.jpg'  
    with open(filename, 'wb') as f:
	    f.write(imgdata)

def preprocessImage(doodle,url):
    im=PIL.Image.open(io.BytesIO(base64.b64decode(doodle[22:])))
    imbw=im.convert('L')
    cropped=imbw.crop(imbw.getbbox())
    
    #####
    bbox=imbw.getbbox()
    print(bbox)
    height=bbox[3]-bbox[1]
    width=bbox[2]-bbox[0]
    hw=height/width
    wh=width/height
    print('proportion height/w : ',hw)
    print('proportion width/h', wh)

    if ( hw > 2.5 or hw < 0.25 or wh>2.5 or wh <0.25):
        print('disproportional')
    #####
    resized=cropped.resize([28,28])
    resized.save(url)
    arr=np.asarray(resized.getdata())/255.0
    arrmtrx=arr.reshape([1,28,28,1])
    return arrmtrx

## get data from webpage, run prediction for original and preprocessed images

@app.route('/predict', methods=['GET', 'POST']) 
def predict():
    print("In predict")
   #print(imagen)
    if request.method == 'POST':
        #print(request.get_data()[:50])
        dtstr=datetime.datetime.now().strftime('%y%m%d%M%S')
        originalurl='./static/images/original'+dtstr+'.jpg'
        processedurl='./static/images/processed'+dtstr+'.jpg'

        saveImageFile(request.get_data(),originalurl)
        image=get_image(request.get_data())
        predOriginal = class_map[int(cnnmodel.predict_classes(image)[0])]
        #print("\n starting prediction of original image...  ")
        
        #print(f'\n ************** Prediction : {pred} {class_map[pred]} \n\n')
        pimage=preprocessImage(request.get_data(),processedurl)
        predProcessed = class_map[int(cnnmodel.predict_classes(pimage)[0])]
        #print(f'\n ************** Prediction : {pred} {class_map[pred]} \n\n')
        predictData={'original':predOriginal,'preprocessed':predProcessed,'originalUrl':originalurl, 'processedUrl':processedurl}
        #imageurls={'original':originalurl,'preprocessed':processedurl}
        #print(type(predict))
        print(predictData)
    return jsonify(predictData)
 

@app.route('/')
def root():
    print("In root")
    nav_dict = {'home':'active', 'cnn':'not-active', 'dcgan':'not-active', 'about':'not-active'}
    return render_template('drawer.html', nav_dict = nav_dict, predict='',imageurls='')

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