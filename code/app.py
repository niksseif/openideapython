from falsk import Flask
import flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)



app.run(port=5000, debug = True)
