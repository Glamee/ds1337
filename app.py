from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from dateutil import parser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///children.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True) #создаем ячейку с int данными и без повторений
    fio = db.Column(db.String(70), nullable=False)
    group = db.Column(db.String, nullable=False)
    date_z = db.Column(db.String, nullable=False)
    delta_date = db.Column(db.Integer)
    koklyush_date = db.Column(db.String, nullable=False)
    delta_koklyush_date = db.Column(db.Integer)
    paliom_date = db.Column(db.String, nullable=False)
    delta_paliom_date = db.Column(db.Integer)
    zheltuha_date = db.Column(db.String, nullable=False)
    delta_zheltuha_date = db.Column(db.Integer)
    tuber_date = db.Column(db.String, nullable=False)
    delta_tuber_date = db.Column(db.Integer)
    medotvod = db.Column(db.String)

    def __repr__(self):
        return '<Child %r>' % self.id


def update():
    children = Child.query.all()
    for i in children:
        delta = date.today() - datetime.strptime(i.date_z, '%Y-%m-%d').date()
        i.delta_date = delta.days
        delta = date.today()-datetime.strptime(i.koklyush_date, '%Y-%m-%d').date()
        i.delta_koklyush_date = delta.days
        delta = date.today() - datetime.strptime(i.paliom_date, '%Y-%m-%d').date()
        i.delta_paliom_date = delta.days
        delta = date.today() - datetime.strptime(i.zheltuha_date, '%Y-%m-%d').date()
        i.delta_zheltuha_date = delta.days
        delta = date.today() - datetime.strptime(i.tuber_date, '%Y-%m-%d').date()
        i.delta_tuber_date = delta.days
    try:
        db.session.commit()
    except:
        return "При редактировании записи произошла ошибка"

@app.route('/')
def index():
    count = Child.query.count()
    children = Child.query.all()
    #update()
    return render_template("index.html", count=count, children=children)

@app.route('/create', methods=['POST', 'GET'])
def create_child():
    if request.method == "POST":
        fio = request.form['fio']
        group = request.form['group']
        date_z = request.form['date_z']
        delta = date.today()-datetime.strptime(date_z, '%Y-%m-%d').date()
        delta_date = delta.days
        koklyush_date = request.form['koklyush_date']
        delta = date.today()-datetime.strptime(koklyush_date, '%Y-%m-%d').date()
        delta_koklyush_date = delta.days
        paliom_date = request.form['paliom_date']
        delta = date.today()-datetime.strptime(paliom_date, '%Y-%m-%d').date()
        delta_paliom_date = delta.days
        zheltuha_date = request.form['zheltuha_date']
        delta = date.today()-datetime.strptime(zheltuha_date, '%Y-%m-%d').date()
        delta_zheltuha_date = delta.days
        tuber_date = request.form['tuber_date']
        delta = date.today()-datetime.strptime(tuber_date, '%Y-%m-%d').date()
        delta_tuber_date = delta.days
        medotvod = request.form.get('medotvod', 'off')


        child = Child(fio=fio, group=group, date_z=date_z, delta_date=delta_date, koklyush_date=koklyush_date, delta_koklyush_date=delta_koklyush_date,
                      paliom_date=paliom_date, delta_paliom_date=delta_paliom_date, zheltuha_date=zheltuha_date, delta_zheltuha_date=delta_zheltuha_date,
                      tuber_date=tuber_date, delta_tuber_date=delta_tuber_date, medotvod=medotvod)
        try:
            db.session.add(child)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении записи произошла ошибка"
    else:
        return render_template("create.html")

@app.route('/elder_group')
def elder_group():
    children = Child.query.order_by(Child.date_z).all()
    update()
    return render_template("elder_group.html", children=children)


@app.route('/junior_group')
def junior_group():
    children = Child.query.order_by(Child.date_z).all()
    update()
    return render_template("junior_group.html", children=children)


@app.route('/child/<int:id>')
def child_detail(id):
    child = Child.query.get(id)
    update()
    return render_template("child_detail.html", child=child)


@app.route('/child/<int:id>/transfer')
def transfer(id):
    child = Child.query.get(id)
    child.group = 'elder'
    child.date_z = date.today()
    try:
        db.session.commit()
        return redirect('/elder_group')
    except:
        return "При редактировании записи произошла ошибка"


@app.route('/child/<int:id>/delete')
def child_delete(id):
    child = Child.query.get_or_404(id)
    try:
        db.session.delete(child)
        db.session.commit()
        if child.group == 'elder':
            return redirect('/elder_group')
        else:
            return redirect('/junior_group')
    except:
        return "Произошла ошибка"


@app.route('/child/<int:id>/update', methods=['POST', 'GET'])
def child_update(id):
    child = Child.query.get(id)
    if request.method == "POST":
        child.fio = request.form['fio']
        child.group = request.form['group']
        child.date_z = request.form['date_z']
        delta = date.today() - datetime.strptime(child.date_z, '%Y-%m-%d').date()
        child.delta_date = delta.days
        child.koklyush_date = request.form['koklyush_date']
        delta = date.today() - datetime.strptime(child.koklyush_date, '%Y-%m-%d').date()
        child.delta_koklyush_date = delta.days
        child.paliom_date = request.form['paliom_date']
        delta = date.today() - datetime.strptime(child.paliom_date, '%Y-%m-%d').date()
        child.delta_paliom_date = delta.days
        child.zheltuha_date = request.form['zheltuha_date']
        delta = date.today() - datetime.strptime(child.zheltuha_date, '%Y-%m-%d').date()
        child.delta_zheltuha_date = delta.days
        child.tuber_date = request.form['tuber_date']
        delta = date.today() - datetime.strptime(child.tuber_date, '%Y-%m-%d').date()
        child.delta_tuber_date = delta.days

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "При редактировании записи произошла ошибка"
    else:
        return render_template("child_update.html", child=child)

if __name__ == "__main__":
    app.run(debug = True)