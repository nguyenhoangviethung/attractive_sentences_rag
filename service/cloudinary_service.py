from flask import jsonify
import requests
from utilities.utility import Utilities as Ut
import cloudinary.uploader as cu
import cloudinary.api as ca
import cloudinary

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

def download_image(url, filename = 'download.jpg'):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    except Exception as e:
        raise e

def get_all_images(folder):
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