from app.route.mongoDB_route import mongoDB_bp
from app.route.cloudinary_route import cloudinary_bp
from app.route.chatbot_route import chatbot_bp

def register_routes(app):
    app.register_blueprint(mongoDB_bp)
    app.register_blueprint(cloudinary_bp)
    app.register_blueprint(chatbot_bp)

