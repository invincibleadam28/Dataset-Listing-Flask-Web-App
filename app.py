from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Dataset(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(200),nullable=False)
    desc= db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/show')
def show_table():
    all_datasets = Dataset.query.all()
    print(all_datasets)
    return ("This page shows all available datasets")

@app.route('/update/<int:sno>')
def update(sno):
    dataset = Dataset.query.filter_by(sno=sno).first()
    return render_template('update.html',dataset=dataset)

@app.route('/delete/<int:sno>')
def delete(sno):
    dataset = Dataset.query.filter_by(sno=sno).first()
    db.session.delete(dataset)
    db.session.commit()
    return redirect('/')

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        dataset = Dataset(title= title, desc = desc)
        db.session.add(dataset)
        db.session.commit()
    all_datasets = Dataset.query.all()
    return render_template('index.html',all_datasets=all_datasets)

if __name__ == "__main__":
    app.run(debug=True)