from app.app import create_app
from config import load_config

CONFIG = load_config()
app = create_app(CONFIG)

if __name__ == '__main__':
    app.run(debug=True)
