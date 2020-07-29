from flask import Flask, request, jsonify
from celery import Celery
from celery.result import AsyncResult

from deploy import run_command, Endpoint

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://52.167.48.81:6379/0',
    CELERY_RESULT_BACKEND='redis://52.167.48.81:6379/0'
)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])


@app.route('/execute', methods=['POST'])
def execute():
    data = request.form
    task = _execute.delay(data['ip_address'], data['username'], data['password'], data['process'], data['command'])
    return jsonify(task_id=task.id)


@app.route('/status/<task_id>', methods=['GET'])
def status(task_id):
    res = AsyncResult(task_id, app=celery)
    if res.status in ["FAILURE", "SUCCESS"]:
        return jsonify(**res.get())
    else:
        return jsonify(status=res.status)


@celery.task()
def _execute(ip_address, username, password, process, command):
    return run_command(Endpoint(ip_address, username, password), process, command)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
