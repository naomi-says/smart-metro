from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import numpy as np

app = Flask(__name__)
CORS(app)

users = {}

@app.route("/register", methods=["POST"])
def register():
    file = request.files["image"]
    name = request.form.get("name", "user")

    image = face_recognition.load_image_file(file)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        return jsonify({"status": "No face detected"})

    users[name] = encodings[0].tolist()
    return jsonify({"status": f"{name} registered"})


@app.route("/verify", methods=["POST"])
def verify():
    file = request.files["image"]

    image = face_recognition.load_image_file(file)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        return jsonify({"status": "No face detected"})

    for name, encoding in users.items():
        match = face_recognition.compare_faces(
            [np.array(encoding)], encodings[0]
        )[0]

        if match:
            return jsonify({"status": "Access Granted", "user": name})

    return jsonify({"status": "Access Denied"})


if __name__ == "__main__":
    app.run(debug=True)
