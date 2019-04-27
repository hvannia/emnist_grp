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
import pandas as pd
import datetime
import matplotlib
from cnn_plot import rotate, get_cat_index, plot_grid_40

from flask import Flask, request, jsonify, render_template, session, redirect, url_for

from keras.preprocessing import image
from keras.models import load_model

os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Initialize/Configure the app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load the model into the app
cnnmodel = load_model('./static/models/cnn_model.hd5')
cnnmodel._make_predict_function()   # To mitigate ValueError when call predict

# Read in EMNIST test data set (train data set too large)
class_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'
cat_list  = list(class_map)
data_file = './static/data/emnist-balanced-test.csv'
test   = pd.read_csv(data_file,  delimiter = ',')
test_x = test.iloc[:,1:]
test_y = test.iloc[:,0]
test_x = np.asarray(test_x)
test_x = np.apply_along_axis(rotate, 1, test_x)
test_x = test_x.astype('float32')
test_x /= 255

# Utility function definitions
def get_image(data) :
    img_io = io.BytesIO(base64.b64decode(data.decode().split(',')[1]))
    img_full = PIL.Image.open(img_io)
    img_grey = img_full.convert(mode='L')  #(8-bit pixels, black and white)
    img = img_grey.resize((28, 28), resample=PIL.Image.HAMMING) #(map multiple input pixels to a single output pixel)
    img_array=np.asarray(img.getdata()).reshape(28,28)
    img_arr = np.asarray(img.getdata()) / 255.0
    return img_arr.reshape([1,28,28,1])

def saveImageFile(data, filename):
    image_data=data[22:] # remove image filetype info
    imgdata = base64.b64decode(image_data)
    with open(filename, 'wb') as f:
	    f.write(imgdata)

def preprocessImage(doodle,url):
    im=PIL.Image.open(io.BytesIO(base64.b64decode(doodle[22:])))
    imbw=im.convert('L')
    #####
    bbox=imbw.getbbox()
    print(bbox)
    height=bbox[3]-bbox[1]
    width=bbox[2]-bbox[0]
    hw=height/width
    wh=width/height
    print('proportion height/w : ',hw)
    print('proportion width/h', wh)

    if hw < 0.5: 
        print('too wide')
        newbox=(bbox[0],bbox[1]+(height//2)-(width//2),bbox[2],bbox[3]-(height//2)+(width//2) )
        print(newbox)
        cropped=imbw.crop(newbox)
    elif wh<0.5:
        print('too tall')
        newbox=( bbox[0]+(width//2)-(height//2), bbox[1], bbox[2]-(width//2)+(height//2), bbox[3])
        print(newbox)
        cropped=imbw.crop(newbox)
    else:
        cropped=imbw.crop(imbw.getbbox())
    resized=cropped.resize([28,28])
    resized.save(url)
    arr=np.asarray(resized.getdata())/255.0
    arrmtrx=arr.reshape([1,28,28,1])
    return arrmtrx

## get data from webpage, run prediction for original and preprocessed images

@app.route('/predict', methods=['GET', 'POST']) 
def predict():
    print("In predict")
    if request.method == 'POST':
        dtstr=datetime.datetime.now().strftime('%y%m%d%M%S')
        originalurl='./static/images/original'+dtstr+'.jpg'
        processedurl='./static/images/processed'+dtstr+'.jpg'
        saveImageFile(request.get_data(),originalurl)
        image=get_image(request.get_data())
        predOriginal = class_map[int(cnnmodel.predict_classes(image)[0])]
        #print(f'\n ************** Prediction : {pred} {class_map[pred]} \n\n')
        pimage=preprocessImage(request.get_data(),processedurl)
        predProcessed = class_map[int(cnnmodel.predict_classes(pimage)[0])]
        #print(f'\n ************** Prediction : {pred} {class_map[pred]} \n\n')
        predictData={'original':predOriginal,'preprocessed':predProcessed,'originalUrl':originalurl, 'processedUrl':processedurl}
        print(predictData)
    return jsonify(predictData)
 

@app.route('/')
def root():
    print("In root")
    nav_dict = {'home':'active', 'data':'not-active', 'cnn':'not-active', 'imgen':'not-active', 'dcgan':'not-active', 'about':'not-active'}
    return render_template('drawer.html', nav_dict = nav_dict, predict='',imageurls='')

@app.route('/dcgan')
def dcgan():
    print('In /dcgan')
    nav_dict = {'home':'not-active', 'data':'not-active', 'cnn':'not-active', 'imgen':'not-active', 'dcgan':'active', 'about':'not-active'}
    return render_template('dcgan.html', nav_dict = nav_dict)

@app.route('/cnn')
def cnn():
    print('In /cnn')
    nav_dict = {'home':'not-active', 'data':'not-active', 'cnn':'active', 'imgen':'not-active', 'dcgan':'not-active', 'about':'not-active'}
    return render_template('emnist_cnn.html', nav_dict = nav_dict)

@app.route('/cnn_imggen')
def cnn_imggen():
    print('In /cnn_imggen')
    nav_dict = {'home':'not-active', 'data':'not-active', 'cnn':'not-active', 'imgen':'active', 'dcgan':'not-active', 'about':'not-active'}
    return render_template('emnist_cnn_image_gen.html', nav_dict = nav_dict)

@app.route("/getdata/<category>")
def get_data(category):
    print(f'Entry getdata {category}')
    
    if category =="_" :
        data_plt = plot_grid_40(class_map, test_y, test_x, get_cat_index(class_map, test_y))
    else :
        data_plt = plot_grid_40(class_map, test_y, test_x, get_cat_index(class_map, test_y, category))

    data_plt.savefig('./static/images/tmp.png', format='png')
    with open('./static/images/tmp.png', mode='rb') as file: 
        fileContent = file.read()

    plot = f'data:image/png;base64,{base64.b64encode(fileContent).decode()}'
    nav_dict = {'home':'not-active', 'data':'active', 'cnn':'not-active', 'imgen':'not-active', 'dcgan':'not-active', 'about':'not-active'}
    
    return render_template("data.html", plot=plot, ref_list=cat_list, nav_dict=nav_dict)

if __name__ == "__main__":
    app.run(debug=True)