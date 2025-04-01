from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from models import db, User

#DIRECTORY
app = Flask(__name__, template_folder='templates')

# Configure the SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'db.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



# MODELS
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    link = db.Column(db.String(255), nullable=True)
    date = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Application {self.name}>"


# ROUTES
@app.route('/')
def home():
    applications = Application.query.all()  # Query all applications
    return render_template('home.html', applications=applications)

@app.route('/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        link = request.form['link']
        salary = request.form['salary']
        date = request.form.get('date', '')  # Optional field, default to empty string

        new_application = Application(name=name, position=position, link=link, salary=float(salary), date=date)
        db.session.add(new_application)
        db.session.commit()
        return redirect(url_for('home'))  # Redirect to home instead of view_applications
    return render_template('add_application.html')

@app.route('/update/<int:application_id>', methods=['GET', 'POST'])
def update_application(application_id):
    application = Application.query.get_or_404(application_id)
    if request.method == 'POST':
        application.name = request.form['name']
        application.position = request.form['position']
        application.salary = float(request.form['salary'])
        application.link = request.form['link']
        application.date = request.form.get('date', '')
        db.session.commit()
        return redirect(url_for('home'))  # Redirect to home instead of view_applications
    return render_template('update_application.html', application=application)

@app.route('/delete/<int:application_id>')
def delete_application(application_id):
    application = Application.query.get_or_404(application_id)
    db.session.delete(application)
    db.session.commit()
    return redirect(url_for('home'))  # Redirect to home instead of view_applications

# Error handling
if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)