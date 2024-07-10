from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

db.create_all()

class NewsForm(FlaskForm):
    title = StringField\
        ('Название',
         validators=[DataRequired(message="Поле не должно быть пустым"),
                     Length(max=255, message='Введите заголовок длиной до 255 символов')]
        )
    text = TextAreaField('Текст',
         validators=[DataRequired(message = "Поле не должно быть пустым")])
    submit = SubmitField('Добавить')

news = [{'title': 'Удивительное событие в школе',
         'text': 'Вчера в местной школе произошло удивительное событие - все '
                 'ученики одновременно зевнули на уроке математики. '
                 'Преподаватель был так поражен этим коллективным зевком, '
                 'что решил отменить контрольную работу.'},
        {'title': 'Случай в зоопарке',
         'text': 'В зоопарке города произошел необычный случай - ленивец '
                 'решил не лениться и взобрался на самое высокое дерево в '
                 'своем вольере. Посетители зоопарка были поражены такой '
                 'активностью и начали снимать ленивца на видео. В итоге он '
                 'получил свой собственный канал на YouTube, где он размещает '
                 'свои приключения.'},
        {'title': 'Самый красивый пёс',
         'text': 'Сегодня в парке прошел необычный конкурс - "Самый красивый '
                 'пёс". Участники конкурса были так красивы, что судьи не '
                 'могли выбрать победителя. В итоге, конкурс был объявлен '
                 'ничейным, а участники получили награды за участие, '
                 'в том числе - пакетики конфет и игрушки в виде косточек. '
                 'Конкурс вызвал большой интерес у посетителей парка, '
                 'и его решили повторить в более масштабном формате.'}]

@app.route('/')
def index():
    news_list = News.query.all()
    return render_template("index.html", news=news_list)

@app.route('/add_news', methods =['GET','POST'])
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        news.append({'title': title, 'text': text})
        return redirect(url_for('index'))
    return render_template('add_news.html', form=form)

@app.route('/news_detail/<int:id>')
def news_detail(id):
    news_detail = News.query.det(id)
    return render_template ("news_detail.html", news=news_detail)

if __name__ == '__main__':
    app.run(debug=True)
