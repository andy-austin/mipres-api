from flask_cors import CORS
from mipres_app.mipres import create_app

app = create_app('mipres_api')

CORS(app)
