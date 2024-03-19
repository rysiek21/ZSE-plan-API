import json
from flask import Flask

def init_app():
    app = Flask(__name__)
    
    # Config load
    config = None
    with open('config.json') as file:
        config = json.load(file)
    app.config.update(config)
    
    # Routes load
    from routes.zastepstwa import zastepstwa
    app.register_blueprint(zastepstwa)
    
    return app

app = init_app()

if __name__ == "__main__":
    app.run()