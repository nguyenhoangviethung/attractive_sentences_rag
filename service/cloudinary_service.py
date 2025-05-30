from flask import jsonify
import requests
from utilities.utility import Utilities as Ut
import cloudinary.uploader as cu
import cloudinary.api as ca
import cloudinary
from database import connect_db
from config import load_config
from utilities.middleware import MiddleWare as MW
CONFIG = load_config()

db = connect_db(CONFIG)

@MW.check_permission
def upload_image(data, is_authorized = None):
    try:
        folder = ""
        if is_authorized:
            folder = "Images_Unsupervise"
        else:
            folder = "Temp"
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

def download_image(url, filename = 'download.jpg', is_authorized = None):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    except Exception as e:
        raise e

def get_all_images(folder, is_authorized = None):
    try:
        all_images = []
        resources = cloudinary.api.resources(
            type="upload",
            prefix=folder + "/",
            resource_type="image",
            max_results=500 
        )
        
        all_images.extend(resources['resources'])

        while 'next_cursor' in resources:
            resources = cloudinary.api.resources(
                type="upload",
                prefix=folder + "/",
                resource_type="image",
                max_results=500, 
                next_cursor=resources['next_cursor'] 
            )
            all_images.extend(resources['resources'])
        
        return sorted(all_images, key=lambda x: x['created_at'])

    except Exception as e:
        raise