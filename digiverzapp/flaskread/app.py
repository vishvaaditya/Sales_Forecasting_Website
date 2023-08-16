
from flask import Flask, Blueprint
from flask_cors import CORS

from endpoints import project_api_routes



def create_app():
    web_app = Flask(__name__,template_folder="template")  # Initialize Flask Application.
    CORS(web_app)

    api_blueprint = Blueprint('api_blueprint', __name__)
    api_blueprint = project_api_routes(api_blueprint)

    web_app.register_blueprint(api_blueprint, url_prefix='/api')

   # web_app.config['SECRET_KEY'] = 'mysecretkey' 

  
    return web_app


app = create_app()
app.config.from_mapping(
    SECRET_KEY='your_secret_key',
    PERMANENT_SESSION_LIFETIME=60 # Set session expiry time to 1 hour (in seconds)
)

if __name__ == "__main__":
    app.run(debug=True)
