from flask import Flask, escape, request, jsonify
from ariadne.constants import PLAYGROUND_HTML
from ariadne import QueryType, graphql_sync, make_executable_schema,load_schema_from_path, ObjectType
import resolver as r

type_defs = load_schema_from_path('schema.graphql')
query = QueryType()
mutation = ObjectType('Mutation')
student = ObjectType('student')
classes = ObjectType('classes')
app = Flask(__name__)

#GET method 
query.set_field('get_student', r.get_student)
query.set_field('get_class', r.get_class)

#POST method
mutation.set_field('create_student',r.create_student)
mutation.set_field('create_class',r.create_class)

#PATCH method
mutation.set_field('add_student_to_class',r.add_student_to_class)

schema = make_executable_schema(type_defs, [student,classes,query,mutation])

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
    
@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    return PLAYGROUND_HTML, 200
  
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code