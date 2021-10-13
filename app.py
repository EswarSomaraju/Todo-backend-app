# app.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# insert task
@app.post("/task")
def post_task():
    if request.is_json:                                                             # only checks content-type/json or content-type/others
        task = request.get_json()
        if ("task_title" in task) and ("task_details" in task) and len(task)==2:    # check if required params exist
            # insert to db
            con = sqlite3.connect('tasks.db')                                       # create db and table
            con.execute("""
                CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_title TEXT,
                    task_details TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                );
            """)
            
            # insert
            try:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO tasks(task_title, task_details) VALUES (?,?)", 
                    (task["task_title"], task["task_details"])
                    )
                con.commit()
                con.close()
                return task, 201
            except:
                return {"error": "error in insert operation"}, 500
                con.close()
                
        else:
            return {"error": "request has invalid or missing data"}, 422
    return {"error": "request must be json"}, 415


# # fetch all tasks
@app.get("/tasks")
def get_tasks():
    with sqlite3.connect('tasks.db') as con:
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            tasks = []
            for col in rows:
                task = {}
                task["id"] = col[0]
                task["task_title"] = col[1]
                task["task_details"] = col[2]
                task["timestamp"] = col[3]
                tasks.append(task)

            if len(tasks)>0:
                return jsonify(tasks), 200 
            else:
                return {}, 204
        except Exception as e:
            print(e)
            return {"error": "error while fetching data"}, 500

        



# # fetch single task
@app.get("/task/<id>")
def get_single_task(id):
    with sqlite3.connect('tasks.db') as con:
        cursor = con.cursor()
        try:
            task={}
            id = int(id)
            row = cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
            for col in row:
                task["id"] = col[0]
                task["task_title"] = col[1]
                task["task_details"] = col[2]
                task["timestamp"] = col[3]
            if(len(task)>0):
                return task, 200
            else:
                return {}, 204                                                      # response based on tutorial - no record exists
        except Exception as e:
            print(e)
            return {"error": "error while fetching data"}, 500


# # update task
@app.put("/task")
def update_task():
    if request.is_json:
        new_task = request.get_json()
        if ("id" in new_task) and ("task_title" in new_task) and ("task_details" in new_task) and len(new_task)==3:    # check if required params exist
            with sqlite3.connect('tasks.db') as con:
                cursor = con.cursor()
                try:
                    # check if row exists
                    cursor.execute("SELECT EXISTS(SELECT * FROM tasks WHERE id=?)", (new_task["id"],))
                    exists = cursor.fetchone()[0]
                    # exists
                    if(exists):
                        cursor.execute("""UPDATE tasks SET task_title=?, task_details=?
                        WHERE id=?""", (new_task["task_title"], new_task["task_details"], new_task["id"]) )
                        con.commit()
                        return new_task, 200
                    # row not found
                    else:
                        return {}, 204
                except Exception as e:
                    print(e)
                    return {"error": "error while fetching data"}, 500
        else:
            return {"error": "request has invalid or missing data"}, 422            # invalid input data
    return {"error": "request must be json"}, 415                                   # invalid content/type


# # delete task
@app.delete("/task/<id>")
def delete_task(id):
    with sqlite3.connect('tasks.db') as con:
        cursor = con.cursor()
        try:
            # check if row exists
            id = int(id)
            cursor.execute("SELECT EXISTS(SELECT * FROM tasks WHERE id=?)", (id,))
            exists = cursor.fetchone()[0]
            # exists
            if exists:
                cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
                return {}, 204
            # not exists
            else:
                return {}, 204
        except Exception as e:
            print(e)
            return {"error": "error while fetching data"}, 500


# add condition to check if table exists
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
# table_exists = cursor.fetchone()