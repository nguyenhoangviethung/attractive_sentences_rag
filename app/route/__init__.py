from app.route.mongoDB_route import mongoDB_bp
from app.route.cloudinary_route import cloudinary_bp

def register_routes(app):
    app.register_blueprint(mongoDB_bp)
    app.register_blueprint(cloudinary_bp)