from flask import jsonify
from utilities.utility import Utilities as Ut
import cloudinary.uploader as cu
import cloudinary.api as ca

def upload_image(data, folder = "temp"):
    try:
        path = data["path"]
        result = cu.upload(
            path,
            folder = folder,
            public_id = Ut.hash_filename(path),
            unique_filename=False,
            overwrite=True,
            upload = True
        )

        print(result)
        return jsonify({
            "message": "upload image successfully"
        }), 200
    except:
        return jsonify({
            "message": "upload image failure"
        }), 500

# def get_image():
#     pass