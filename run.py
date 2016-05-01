import os
from pprint import pprint

from flask import Flask
from flask.ext.restful import Api

from config import config
from github import *

app = Flask(__name__)
app.config.from_object(config['default'])
api = Api(app)

from giphy import *



if __name__ == '__main__':
    app.run(port=app.config['PORT'])
