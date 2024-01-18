from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
import face_recognition
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
CORS(app, resources={r'/*':{'origins':'http://localhost:8080', "allow_headers": "Access-Control-Allow-Origin"}})






@app.route('/', methods=['GET'])
def greetings():
    return("Hello, world")

@app.route('/upload-images', methods=['POST'])
def test():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify(message="Missing images"), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1.filename == '' or image2.filename == '':
        return jsonify(message="No selected file"), 400

    if image1 and image2:
        filename1 = secure_filename(image1.filename)
        filename2 = secure_filename(image2.filename)

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        image1.save(filepath1)
        image2.save(filepath2)
        
        # getting face encodings for first image
        image_1 = find_face_encodings(filepath1)
        # getting face encodings for second image
        image_2  = find_face_encodings(filepath2)
        
    # return jsonify(message="ready"), 200    

        is_same = face_recognition.compare_faces([image_1], image_2)[0]
        print(f"Is Same: {is_same}")
        if is_same:
            # finding the distance level between images
            distance = face_recognition.face_distance([image_1], image_2)
            distance = round(distance[0] * 100)

            # calcuating accuracy level between images
            accuracy = 100 - round(distance)
            return jsonify(message="Identical. Accuracy Level: {accuracy}%"), 200
        else:
            return jsonify(message="The images are not same"), 200
     
def find_face_encodings(image_path):
    # reading image
    image = cv2.imread(image_path)
    # get face encodings from the image
    face_enc = face_recognition.face_encodings(image)
    # return face encodings
    return face_enc[0]


if __name__ == "__main__":
    app.run(debug=True)
    
    
