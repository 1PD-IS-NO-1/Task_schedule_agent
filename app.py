from flask import Flask, render_template, request, jsonify
from models import db, Task, Column
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate after app is defined

@app.route('/')
def index():
    return render_template('task_table.html')

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])
    
    if request.method == 'POST':
        data = request.get_json()
        new_task = Task(
            name=data['name'],
            assignee=data['assignee'],
            status=data['status'],
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d') if data['due_date'] else None,
            priority=data['priority'],
            custom_fields=data.get('custom_fields', {})  # Add custom_fields
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def single_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        task.name = data['name']
        task.assignee = data['assignee']
        task.status = data['status']
        task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if data['due_date'] else None
        task.priority = data['priority']
        task.custom_fields = data.get('custom_fields', task.custom_fields)  # Update custom_fields
        db.session.commit()
        return jsonify(task.to_dict())
    
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})

@app.route('/tasks/save', methods=['POST'])
def save_all_tasks():
    try:
        data = request.get_json()
        for task_data in data:
            task = Task.query.get(task_data['id'])
            if task:
                task.name = task_data.get('name', task.name)
                task.assignee = task_data.get('assignee', task.assignee)
                task.status = task_data.get('status', task.status)
                task.due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d') if task_data.get('due_date') else None
                task.priority = task_data.get('priority', task.priority)
                task.custom_fields = task_data.get('custom_fields', task.custom_fields)  # Update custom_fields
        db.session.commit()
        return jsonify({'message': 'All changes saved successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/columns', methods=['GET', 'POST'])
def manage_columns():
    if request.method == 'GET':
        columns = Column.query.all()
        return jsonify([{
            'id': col.id,
            'name': col.name,
            'type': col.type,
            'options': col.options
        } for col in columns])
    
    if request.method == 'POST':
        data = request.get_json()
        new_col = Column(
            name=data['name'],
            type=data['type'],
            options=data.get('options')
        )
        db.session.add(new_col)
        db.session.commit()
        return jsonify({'message': 'Column created successfully'})

@app.route('/columns/<int:col_id>', methods=['DELETE'])
def delete_column(col_id):
    column = Column.query.get_or_404(col_id)
    db.session.delete(column)
    db.session.commit()
    return jsonify({'message': 'Column deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)