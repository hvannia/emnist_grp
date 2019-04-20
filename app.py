import os
from flask import Flask, request, jsonify, render_template

from keras.preprocessing import image
from keras.models import load_model
from keras import backend

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

#model = load_model('mnist_cnn_trained.h5')
#raph = backend.get_session().graph

def prepare_image(img):
    # Convert the image to a numpy array
    img = image.img_to_array(img)
    # Scale from 0 to 255
    img /= 255
    # Invert the pixels
    #img = 1 - img
    # Flatten the image to an array of pixels  
    #image_array = img.flatten().reshape(-1, 28 * 28)
    #for cnn:
    #image_array=image.expand_dim(axis=2)
    # Return the processed feature array
    return img.reshape(1,28,28,1)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request)
        data = request.get_data()
        print(data)
          # gotta: 
          #  f=io.Bytes(base64.b64decode(s))  
          #img = image.load_img(filepath, target_size=(28, 28), grayscale=True)

            # Convert the 2D image to an array of pixel values
            #image_array = prepare_image(im)
            #print(image_array)
            
            #with graph.as_default():
            #    pred = int(model.predict_classes(image_array)[0])
            #return jsonify({'prediction': pred, 'status': 'success'})
    return render_template("drawer.html")

if __name__ == "__main__":
    app.run(debug=True)