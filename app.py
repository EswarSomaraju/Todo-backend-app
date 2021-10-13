# app.py
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

tasks= []

# search task
# def search_task(id):
#     for task in tasks:
#         if(task["id"]==int(id)):
#             return task
#     return {}


# insert task
@app.post("/task")
def post_task():
    if request.is_json:                                                             # only checks content-type/json or content-type/others
        task = request.get_json()
        if ("task_title" in task) and ("task_details" in task) and len(task)==2:    # check if required params exist
            task["id"] = len(tasks)+1
            task["timestamp"] = datetime.now()
            tasks.append(task)
            return task, 201
        else:
            return {"error": "request has invalid or missing data"}, 422
    return {"error": "request must be json"}, 415


# fetch all tasks
@app.get("/tasks")
def get_tasks():
    if(len(tasks)>0):
        return jsonify(tasks), 200
    else:
        return jsonify(tasks), 204


# fetch single task
@app.get("/task/<id>")
def get_single_task(id):
    for task in tasks:
        if(task["id"]==int(id)):
            return task, 200
    return {}, 204                  # response based on tutorial - no record exists


# update task
@app.put("/task")
def update_task():
    if request.is_json:
        new_task = request.get_json()
        if ("id" in new_task) and ("task_title" in new_task) and ("task_details" in new_task) and len(new_task)==3:    # check if required params exist
            for task in tasks:
                if(task["id"]==new_task["id"]):
                    task["task_title"] = new_task["task_title"]
                    task["task_details"] = new_task["task_details"]
                    task["timestamp"] = datetime.now()
                    return task, 200
            return {}, 204
        else:
            return {"error": "request has invalid or missing data"}, 422
    return {"error": "request must be json"}, 415


# delete task
@app.delete("/task/<id>")
def delete_task(id):
    for task in tasks:
        if(task["id"]==int(id)):
            tasks.remove(task)
            return task, 200   # return task,200 on delete
    return {}, 204


