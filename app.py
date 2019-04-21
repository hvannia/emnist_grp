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

#model = load_model('mnist_cnn_trained.h5')
#raph = backend.get_session().graph

cnnmodel = load_model('./static/models/cnnmodel.h5')
cnnmodel._make_predict_function()   # To mitigate ValueError when call predict

class_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'

def prepare_image(img):
    # Convert the image to a numpy array
    img = image.img_to_array(img)
    # Scale from 0 to 255
    img /= 255
    # Invert the pixels
    #img = 1 - img
    # Flatten the image to an array of pixels  
    image_array = img.flatten().reshape(-1, 28 * 28)
    #for cnn:
    #image_array=image.expand_dim(axis=2)
    # Return the processed feature array
    return img.reshape(1,28,28,1)


def get_image(data) :
    img_io = io.BytesIO(base64.b64decode(data.decode().split(',')[1]))
    img_full = PIL.Image.open(img_io)
    img_grey = img_full.convert(mode='L')
    img = img_grey.resize((28, 28), resample=PIL.Image.HAMMING)
    img_arr = np.asarray(img.getdata()) / 255.0
    return img_arr.reshape([1,28,28,1])


@app.route('/mark', methods=['GET', 'POST'])
def upload_file_mark():
    if request.method == 'POST':
        pred = int(cnnmodel.predict_classes(get_image(request.get_data()))[0])
        print(f'\n\n ************** Prediction : {pred} {class_map[pred]} \n\n')
        resp = jsonify({'prediction': pred, 'status':'success'})
    return render_template("drawer.html")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #print(request)
        data = request.get_data()
        # save image to disk (for verification)
        image_data=data[22:] # remove image filetype info
        imgdata = base64.b64decode(image_data)
        filename = 'drawing.jpg'  
        with open(filename, 'wb') as f:
            f.write(imgdata)    
        ##  end save
        encoded=binascii.b2a_base64(data)
        fio=io.BytesIO(encoded)
        print('bytesio:',f)

        img = image.load_img('drawing.jpg', target_size=(280, 280))
        image_array = prepare_image(img)
        print(image_array)
            
            #with graph.as_default():
            #    pred = int(model.predict_classes(image_array)[0])
            #return jsonify({'prediction': pred, 'status': 'success'})
    return render_template("drawer.html")

if __name__ == "__main__":
    app.run(debug=True)