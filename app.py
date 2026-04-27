from flask import Flask, jsonify, request, abort

app = Flask(__name__)

todos = []
next_id = 1


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/todos", methods=["GET"])
def list_todos():
    return jsonify(todos), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json()
    if not data or not data.get("title"):
        abort(400, description="title is required")
    todo = {"id": next_id, "title": data["title"], "done": False}
    next_id += 1
    todos.append(todo)
    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        abort(404, description="todo not found")
    return jsonify(todo), 200


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        abort(404, description="todo not found")
    data = request.get_json()
    if not data:
        abort(400, description="request body is required")
    if "title" in data:
        todo["title"] = data["title"]
    if "done" in data:
        todo["done"] = bool(data["done"])
    return jsonify(todo), 200


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        abort(404, description="todo not found")
    todos = [t for t in todos if t["id"] != todo_id]
    return "", 204


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e.description)}), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e.description)}), 404


if __name__ == "__main__":
    app.run(debug=True)
