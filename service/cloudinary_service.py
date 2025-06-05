from flask import jsonify
import requests, os, tempfile
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
        path = data.get("path", None)
        print(path)
        is_temp_file = False  

        if not path:
            img = data.get("img")
            if not img or not hasattr(img, "save"):
                raise ValueError("Không tìm thấy file ảnh hợp lệ.")

            ext = os.path.splitext(img.filename)[-1] or ".jpg"
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
                img.save(temp_file.name)
                path = temp_file.name
                is_temp_file = True
        result = cu.upload(
            path,
            folder = folder,
            public_id = Ut.hash_filename(path),
            unique_filename=False,
            overwrite=True,
            upload = True
        )

        if is_temp_file and os.path.exists(path):
            os.remove(path)
        print(result)
        return jsonify({
            "message": "upload image successfully"
        }), 202
    except Exception as e:
        print(e)
        return jsonify({
            "message": "upload image failure"
        }), 400

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

@MW.check_permission
def get_temp_images(is_authorized):
    if not is_authorized:
        return jsonify({
            "message": "Have not permission"
        }), 401
    try:
        images = get_all_images("Temp")
        return jsonify({
            "images": images,
            "message": "Fetched successfully",
            "count": len(images)
        }), 200
    except Exception as e:
        print("Get temp images failed:", e)
        return jsonify({
            "message": "Cannot fetch temp images"
        }), 500

@MW.check_permission
def approve_image(data, is_authorized=None):
    if not is_authorized:
        return jsonify({
            "message": "Have not permission"
        }), 401
    try:
        image_url = data.get("path")
        if not image_url:
            return jsonify({"message": "Missing image URL"}), 400

        upload_response, status = upload_image(data = data)

        if status != 200:
            return jsonify({"message": "Upload failed during approval"}), 500

        part = image_url.split("Temp")
        public_id = part[1]
        public_id = public_id.split(".")[0]
        public_id = "Temp"+public_id

        print("Destroying:", public_id)
        cloudinary.uploader.destroy(public_id)

        return jsonify({"message": "Image approved and moved"}), 200
    except Exception as e:
        print("Approve failed:", e)
        return jsonify({"message": "Failed to approve image"}), 500

