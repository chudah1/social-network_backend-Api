from flask import Flask, jsonify, request
import functions_framework

from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()


#flask app
app = Flask(__name__)
#profiles table
profile_table = db.collection("profile")



@functions_framework.http
def student_profile_api(request):
    """
    This is a Python function that handles HTTP requests for registering, editing, and retrieving
    student information based on the request method and parameters.
    
    :param request: The request object contains information about the incoming HTTP request, such as the
    HTTP method, headers, and body
    :return: The code is defining an HTTP Cloud Function that handles requests to a student profile API.
    The function returns different responses depending on the HTTP method and the presence of certain
    parameters in the request. However, the code snippets for the `register_student()`,
    `edit_student()`, and `retrieve_student_info()` functions are not provided, so it is not possible to
    determine what exactly is being returned by the function
    """
    if request.method=="POST" and request.json and "idNumber" in request.get_json():
        return register_student()
    elif request.method=="PUT" and request.json and "idNumber" in request.get_json() and request.args and "idNumber" in request.args:
        return edit_student()
    elif request.method=="GET" and request.args and "idNumber" in request.args:
        return retrieve_student_info()
    else:
        return jsonify({"error":"Bad request"}), 400

def register_student():
    """
    This function registers a student by checking if the student data is valid, if the student is not
    already registered, and then adding the student data to a profile table.
    :return: a JSON response with either an error message and a status code of 400 or 409, or a success
    message with a status code of 201.
    """
    student_data = request.json
    if not student_data:
        return jsonify({"error":"Bad request"}), 400
    student_id = request.json["idNumber"]
    if profile_table.document(student_id).get().exists:
        return jsonify ({"error":"Student Already Registered"}), 409
    profile_table.document(student_id).set(request.json)
    return jsonify ({"success":"Student Registered Successfully"}), 201

def edit_student():
    """
    This function edits a student's data in a profile table if the student exists.
    :return: the updated student data in JSON format if the update is successful. If the request is
    invalid or the student to update is not found, an error message in JSON format is returned with an
    appropriate HTTP status code (400 or 404).
    """
    student_data = request.json
    if not student_data:
        return jsonify({"error":"Bad request"}), 400
    student_id = request.json["idNumber"]
    if not profile_table.document(student_id).get().exists:
        return jsonify({"error": "Could not find student to update"}), 404
    profile_table.document(student_id).update(request.json)
    return request.json

def retrieve_student_info():
    """
    This function retrieves student information from a database and returns it as a JSON object, or
    returns an error message if the student is not found.
    :return: The function `retrieve_student_info()` returns a JSON response containing the details of a
    student with the given `student_id`. If the student does not exist, it returns a JSON response with
    an error message and a 404 status code.
    """
    student_id = request.args.get("idNumber")
    student_exists = profile_table.document(student_id).get()
    if not student_exists.exists:
        return jsonify({"error": "student details not found"}), 404
    else:
        student_exists_dict = student_exists.to_dict()
        return jsonify(student_exists_dict)
    
    







