from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS,cross_origin
import os


## Init app
app = Flask(__name__)
# configuring cors
CORS(app,resources={r"/api": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
# path setup
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(400))

    def __init__(self,title,description):
        # Add the data to the instance
        self.title = title
        self.description = description
         
# Todo schema
class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id','title','description')

# Init Schema
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

# Cors configuration

# Create a todo
@app.route('/api/todo', methods=['POST'])
@cross_origin(origin='*',headers=['content-type'])
def add_todo():
    # get the data
    title = request.json['title']
    description = request.json['description']

    # Create an instance
    new_todo = Todo(title, description)

    # Save the todo in the db
    db.session.add(new_todo)
    db.session.commit()

    # return the created todo
    return todo_schema.jsonify(new_todo)

# Get all todos
@app.route('/api/todo', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def get_todos():
    # get the todos from db
    all_todos = Todo.query.all()
    # get the todos as per the schema
    result = todos_schema.dump(all_todos)
    # return the todos
    return jsonify(result)

# Get a single todo
@app.route('/api/todo/<id>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def get_todo(id):
    # get a single todo
    todo = Todo.query.get(id)
    # return the todo as per the schema
    return todo_schema.jsonify(todo)

# update a todo
@app.route('/api/todo/<id>', methods=['PUT'])
@cross_origin(origin='*',headers=['Content-Type'])
def update_todo(id):
    # get the todo first
    todo = Todo.query.get(id)
    # get the data
    title = request.json['title']
    description = request.json['description']

    # set the data
    todo.title = title
    todo.description = description
    
    # commit to the database
    db.session.commit()

    # return the new todo as per the schema
    return todo_schema.jsonify(todo)

# Delete a todo
@app.route('/api/todo/<id>', methods=['DELETE'])
@cross_origin(origin='*',headers=['Content-Type'])
def delete_todo(id):
    # get the todo to be deleted
    todo = Todo.query.get(id)

    # delete from the database
    db.session.delete(todo)

    # commit on the database
    db.session.commit()

    # return thr deleted todo as per the schema
    return todo_schema.jsonify(todo)

# Start the app
if __name__ == '__main__':
    app.run(debug=True)