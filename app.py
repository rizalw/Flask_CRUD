from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask_crud.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, title, description, date_created):
        self.title = title
        self.description = description
        self.date_created = date_created

with app.app_context():
    db.create_all()

@app.get("/")
def index():
    data_buku = Books.query.order_by(Books.date_created).all()
    return render_template("index.html", data_buku = data_buku)

@app.post("/")
def upload():
    nama_buku = request.form['nama_buku']
    deskripsi_buku = request.form['deskripsi_buku']
    date_created = datetime.now()
    input_baru = Books(nama_buku, deskripsi_buku, date_created)
    try:
        db.session.add(input_baru)
        db.session.commit()
        return redirect( url_for('index') )
    except:
        return "Upload gagal"

@app.get("/update/<int:id>")
def update(id):
    data_buku = Books.query.get_or_404(id)
    return render_template('update.html', data_buku = data_buku)

@app.post("/update")
def updatefix():
    id_buku = request.form['id_buku']
    nama_buku = request.form['nama_buku']
    deskripsi_buku = request.form['deskripsi_buku']
    data_buku = Books.query.filter_by(id=id_buku).first()
    data_buku.title = nama_buku
    data_buku.description = deskripsi_buku
    data_buku.date_updated = datetime.now()
    db.session.commit()
    return  redirect(url_for('index'))

@app.get('/delete/<int:id>')
def delete(id):
    delete_data = Books.query.get_or_404(id)
    try:
        db.session.delete(delete_data)
        db.session.commit()
        return redirect("/")
    except:
        return "Terdapat masalah dalam menghapus data"

app.run(debug=True)