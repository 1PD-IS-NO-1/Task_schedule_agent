from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    assignee = db.Column(db.String(50))
    status = db.Column(db.String(20), default='TO DO')
    due_date = db.Column(db.Date)
    priority = db.Column(db.String(20))
    custom_fields = db.Column(db.JSON)  # Store custom columns data

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'assignee': self.assignee,
            'status': self.status,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else '',
            'priority': self.priority,
            'custom_fields': self.custom_fields or {}
        }

class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), default='text')
    options = db.Column(db.JSON)  # For select type columns