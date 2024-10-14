from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://OlegBamperShchuka:OlegBamperShchuka27062024@localhost/calendar_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)

@app.route('/')
def index():
    sort_order = request.args.get('sort', 'asc')  # по умолчанию сортировка по возрастанию
    if sort_order == 'asc':
        events = Event.query.order_by(Event.date.asc()).all()
    else:
        events = Event.query.order_by(Event.date.desc()).all()

    return render_template('index.html', events=events, sort_order=sort_order)

@app.route('/add', methods=['POST'])
def add_event():
    title = request.form['title']
    description = request.form['description']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    new_event = Event(title=title, description=description, date=date)
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get_or_404(id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.description = request.form['description']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('event.html', event=event)

@app.route('/delete/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_events():
    title_query = request.args.get('title')
    description_query = request.args.get('description')
    date_query = request.args.get('date')

    filters = []
    if title_query:
        filters.append(Event.title.contains(title_query))
    if description_query:
        filters.append(Event.description.contains(description_query))
    if date_query:
        date_obj = datetime.strptime(date_query, '%Y-%m-%d')
        filters.append(Event.date == date_obj)

    results = Event.query.filter(*filters).all()
    return render_template('index.html', events=results)

if __name__ == '__main__':
    app.run(debug=True)
