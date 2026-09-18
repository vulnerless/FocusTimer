"""FocusTimer web application (Flask)."""

from flask import Flask, jsonify, render_template, request

from timer_core import TaskList, Timer


def create_app():
    app = Flask(__name__)
    timer = Timer()
    tasks = TaskList()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/timer")
    def get_timer():
        return jsonify(timer.to_dict())

    @app.post("/api/timer/start")
    def start():
        timer.start()
        return jsonify(timer.to_dict())

    @app.post("/api/timer/pause")
    def pause():
        timer.pause()
        return jsonify(timer.to_dict())

    @app.post("/api/timer/reset")
    def reset():
        timer.reset()
        return jsonify(timer.to_dict())

    @app.post("/api/timer/tick")
    def tick():
        data = request.get_json(silent=True) or {}
        try:
            timer.tick(data.get("seconds", 1))
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        return jsonify(timer.to_dict())

    @app.post("/api/settings")
    def settings():
        data = request.get_json(silent=True) or {}
        try:
            timer.set_durations(data.get("work"), data.get("break"))
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        return jsonify(timer.to_dict())

    @app.get("/api/tasks")
    def list_tasks():
        return jsonify(tasks.all())

    @app.post("/api/tasks")
    def add_task():
        data = request.get_json(silent=True) or {}
        try:
            task = tasks.add(data.get("title"))
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        return jsonify(task), 201

    @app.post("/api/tasks/<int:task_id>/complete")
    def complete_task(task_id):
        try:
            return jsonify(tasks.complete(task_id))
        except KeyError:
            return jsonify({"error": "Task not found"}), 404

    @app.delete("/api/tasks/<int:task_id>")
    def delete_task(task_id):
        try:
            tasks.delete(task_id)
        except KeyError:
            return jsonify({"error": "Task not found"}), 404
        return "", 204

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
