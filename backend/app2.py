from flask import Flask, request, jsonify, url_for, send_file
from celery import Celery, shared_task
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

CORS(app, origins='http://localhost:5173')

@celery.task
def generate_csv_task(data):
    df = pd.DataFrame(data)
    csv_path = './export.csv'
    df.to_csv(csv_path, index=False)
    return csv_path

@app.route('/export-csv', methods=['POST'])
def export_csv():
    data = request.json  # The data you want to export
    task = generate_csv_task.apply_async(args=[data])
    return jsonify({"task_id": task.id, "status_url": url_for('task_status', task_id=task.id)})

@app.route('/status/<task_id>')
def task_status(task_id):
    task = generate_csv_task.AsyncResult(task_id)
    print(task.state)
    if task.state == 'SUCCESS':
        return send_file(task.result, as_attachment=True)
    else:
        return jsonify({"state": task.state})
    
    

if __name__ == '__main__':
    app.run(debug=True)
