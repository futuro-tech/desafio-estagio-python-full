from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "desafio"

mysql = pymysql.connect(
    host="localhost", port=3306, user="root", password="root", db="desafio"
)


def create_table():
    try:
        print("Creating table")
        cur = mysql.cursor()
        cur.execute(
            """
          CREATE TABLE `desafio`.`tasks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(255) NOT NULL,
  `status` ENUM('To-Do', 'Doing', 'Done') NOT NULL,
  PRIMARY KEY (`id`));

                """
        )
        mysql.commit()
        cur.close()
        print("Table created successfully")
    except Exception as e:
        print("Error while create", e)


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


if __name__ == "__main__":
    create_table()
    app.run(debug=True)


@app.route("/tasks")
def get_tasks():
    try:
        cur = mysql.cursor()
        cur.execute("SELECT * FROM tasks")
        data = cur.fetchall()
        cur.close()
        tasks = [
            {"id": item[0], "description": item[1], "status": item[2]} for item in data
        ]
        response = {
            "error": False,
            "data": tasks,
            "message": "Tasks fetched successfully",
        }
        return jsonify(response), 200
    except Exception as e:
        response = {"error": True, "message": f"Error Occurred: {e}", "data": None}

        return jsonify(response), 500


@app.route("/add_task", methods=["POST"])
def add_task():
    try:
        data = request.get_json()
        description = data["description"]
        status = data["status"]
        cur = mysql.cursor()
        cur.execute(
            "INSERT INTO tasks (description, status) VALUES (%s, %s)",
            (description, status),
        )
        mysql.commit()
        cur.close()
        response = {"error": False, "message": "Task added successfully", "data": data}
        return jsonify(response), 201
    except Exception as e:
        response = {"error": True, "message": f"Error Occurred: {e}", "data": None}

        # Return a JSON response with HTTP status code 500 (Internal Server Error)
        return jsonify(response), 500


@app.route("/update_task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        data = request.get_json()
        description = data["description"]
        status = data["status"]
        cur = mysql.cursor()
        cur.execute(
            "UPDATE tasks SET description = %s, status = %s WHERE id = %s", (task_id)
        )
        mysql.commit()
        cur.close()
        response = {
            "error": False,
            "message": "Task updated successfully",
            "data": data,
        }
        return jsonify(response), 201
    except Exception as e:
        response = {"error": True, "message": f"Error Occurred: {e}", "data": None}
        return jsonify(response), 500
