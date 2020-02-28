from flask import Flask, escape, request, jsonify
from ariadne.constants import PLAYGROUND_HTML
from ariadne import gql, QueryType, MutationType, graphql_sync, make_executable_schema,load_schema_from_path, ObjectType

type_defs = gql(load_schema_from_path("schema.graphql"))
query = QueryType()
mutation = MutationType()


DB = {
	"students":[],
	"classes":[]
}

student_id = 100
class_id = 10


@mutation.field("createStudent")

def create_student(_, info, name):
	
 global DB, student_id, class_id
	
 stu = {
	"name": name,
	"id": student_id
 }
 
 DB["students"].append(stu)
 
 student_id = student_id + 1
 
 return stu

  
@mutation.field("createClass")

def create_class(_, info, name):
 
 global DB, student_id, class_id
	
 cls = {
	"id": class_id,
	"name": name, 
	"students":[]
 }
 DB["classes"].append(cls)
 class_id = class_id + 1
 return cls


@mutation.field("addStudentToClass")

def add_student_to_class(_, info, stu_id, clas_id):
	
 global DB, student_id, class_id
 
 for cls in DB["classes"]:
    
    if cls["id"] == clas_id:

      for stu in DB["students"]:	
			
        if stu["id"] == stu_id:
				
         cls["students"].append(stu)
			
 return cls         

@query.field("getStudent")
def get_student(_, info, id):
	
    global DB, student_id, class_id
	
    for stu in DB["students"]:
		
        if id == stu["id"]:
			
            return stu
	
    return f"This student does not exist."


@query.field("getClass")
def get_class(_, info, id):
	
    global DB, student_id, class_id
	
    for cls in DB["classes"]:
		
        if id == cls["id"]:
			
            return cls
	
    return f"This class does not exist."
  

schema = make_executable_schema(type_defs, [query, mutation])

app = Flask(__name__)




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

if __name__ == "__main__":
    app.run(debug=True)
