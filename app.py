from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from apis.hi import RetrievalView, TimeoutView


app = Flask(__name__)

api = Api(app)
CORS(app)

api.add_resource(RetrievalView, '/retrieval')
api.add_resource(TimeoutView, '/timeout')


@app.route('/')
def hello():
    return "Hello"


if __name__ == '__main__':
    app.run(debug=True)
