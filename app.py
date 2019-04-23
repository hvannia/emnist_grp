import os
import io
import base64
import binascii
import PIL
import numpy as np
from flask import Flask, request, jsonify, render_template

from keras.preprocessing import image
from keras.models import load_model
#from keras import backend

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

cnnmodel = load_model('./static/models/cnnmodel.h5')
cnnmodel._make_predict_function()   # To mitigate ValueError when call predict

class_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'

def get_image(data) :
    img_io = io.BytesIO(base64.b64decode(data.decode().split(',')[1]))
    img_full = PIL.Image.open(img_io)
    img_grey = img_full.convert(mode='L')
    img = img_grey.resize((28, 28), resample=PIL.Image.HAMMING)
    img_arr = np.asarray(img.getdata()) / 255.0
    return img_arr.reshape([1,28,28,1])


@app.route('/mark', methods=['GET', 'POST'])
def upload_file_mark():
    print("In mark route")
    if request.method == 'POST':
        data=request.get_data()
         # save image to disk (for verification)
        image_data=data[22:] # remove image filetype info
        imgdata = base64.b64decode(image_data)
        filename = 'drawing.jpg'  
        with open(filename, 'wb') as f:
            f.write(imgdata)    
            print("Saved image for verification")
        ##  end save
        print("starting prediction... getting magic ball")
        pred = int(cnnmodel.predict_classes(get_image(data))[0])
        print(f'\n ************** Prediction : {pred} {class_map[pred]} \n\n')
        resp ="Predicted value: "+class_map[pred]
        return resp 
    render_template("drawer.html")

@app.route('/', methods=['GET', 'POST'])
def iAmRoot():
    print("In /")
    return render_template("drawer.html")

@app.route('/dcgan')
def dcgan():
    print('In /dcgan')
    return render_template('dcgan.html')

if __name__ == "__main__":
    app.run(debug=True)