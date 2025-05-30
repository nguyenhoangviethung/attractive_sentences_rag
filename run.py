from app.app import create_app
from config import load_config
import cloudinary.uploader as cu
from utilities.utility import Utilities
import os
CONFIG = load_config()
app = create_app(CONFIG)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
