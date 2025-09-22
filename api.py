from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'msg': 'hello, world'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug = True)