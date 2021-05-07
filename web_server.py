import os
from datetime import datetime as dt

from flask import Flask, render_template, redirect, request

from data import db_session
from data.barcode_maker import get_barcode_file
from data.models import *
from data.my_classes import ImportData
from forms import LoginForm, NewUser, NewGood, NewLocation, NewItemType, NewItemSubtype, Import
from flask_login import login_user, logout_user, login_required, LoginManager
import openpyxl

main_app = Flask(__name__)
main_app.config['SECRET_KEY'] = 'yandex_lyceum_project_secret_key'
login_manager = LoginManager()
login_manager.init_app(main_app)
for_import = ImportData()


def get_choises(session, table):
    return [(choice.id, choice.name) for choice in
            session.query(table).all()]


@main_app.errorhandler(401)
def page_not_found(e):
    form = LoginForm()
    return render_template('login.html',
                           message="Для выполнения данной операции необходимо "
                                   "авторизоваться",
                           form=form), 401


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@main_app.route('/')
@main_app.route('/index')
def index():
    db_sess = db_session.create_session()
    all_goods = db_sess.query(Good).all()
    return render_template('index.html', title='Главная', goods=all_goods)


@main_app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = NewUser()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.about = form.about.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.created_date = dt.now()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация пользователя',
                           form=form)


@main_app.route('/new_good', methods=['GET', 'POST'])
@main_app.route('/edit_good/<the_id>', methods=['GET', 'POST'])
@login_required
def edit_good(the_id=None):
    db_sess = db_session.create_session()
    item = Good()
    if the_id:
        item = db_sess.query(Good).filter(Good.id == the_id).first()
    form = NewGood()
    form.name.data = item.name
    form.invent_number.data = item.invent_number
    form.comment.data = item.comment
    form.is_on_balance.data = item.is_on_balance
    form.status_id.choices = get_choises(db_sess, Condition)
    form.status_id.default = item.status_id
    form.item_type_id.choices = get_choises(db_sess, ItemType)
    form.item_type_id.default = item.item_type_id
    form.item_subtype_id.choices = get_choises(db_sess, ItemSubtype)
    form.item_subtype_id.default = item.item_subtype_id
    form.location_id.choices = get_choises(db_sess, Location)
    form.location_id.default = item.location_id
    form.responsible_id.choices = get_choises(db_sess, User)
    form.responsible_id.default = item.responsible_id
    form.bought_date.data = item.bought_date
    form.can_be_used.data = item.can_be_used
    # form.process()
    if form.validate_on_submit():
        item.name = request.form['name']
        item.invent_number = request.form['invent_number']
        item.comment = request.form['comment']
        item.is_on_balance = True if request.form.get('is_on_balance', default=False) else False
        item.status_id = int(request.form['status_id'])
        item.item_type_id = int(request.form['item_type_id'])
        item.item_subtype_id = int(request.form['item_subtype_id'])
        item.location_id = int(request.form['location_id'])
        item.responsible_id = int(request.form['responsible_id'])
        item.bought_date = dt.strptime(request.form['bought_date'], '%d.%m.%Y').date()
        item.can_be_used = int(request.form['can_be_used'])
        if the_id:
            pass
        else:
            db_sess.add(item)
        db_sess.commit()
        return redirect('/')
    title = 'Новая вещь'
    if the_id:
        form.submit.label.text = 'Изменить'
        title = 'Редактирование'
    return render_template('new_good.html', title=title, form=form)


@main_app.route('/get_barcode/<text>', methods=['GET'])
@login_required
def get_barcode(text):
    link = get_barcode_file(text, 'images')
    print(link)
    return render_template('barcode.html', text=text, image_link=link)


@main_app.route('/new_location', methods=['GET', 'POST'])
@login_required
def new_location():
    form = NewLocation()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        location = Location()
        location.name = form.name.data
        db_sess.add(location)
        db_sess.commit()
        return redirect('/new_good')

    return render_template('new_property_id_name.html', title='Новое место', form=form)


@main_app.route('/new_item_type', methods=['GET', 'POST'])
@login_required
def new_item_type():
    form = NewItemType()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        newtype = ItemType()
        newtype.name = form.name.data
        db_sess.add(newtype)
        db_sess.commit()
        return redirect('/new_good')
    return render_template('new_property_id_name.html', title='Новый тип вещи', form=form)


@main_app.route('/new_item_subtype', methods=['GET', 'POST'])
@login_required
def new_item_subtype():
    form = NewItemSubtype()
    db_ses = db_session.create_session()
    form.type_id.choices = [(choice.id, choice.name) for choice in db_ses.query(ItemType).all()]
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        newtype = ItemSubtype()
        newtype.name = form.name.data
        newtype.type_id = form.type_id.data
        db_sess.add(newtype)
        db_sess.commit()
        return redirect('/new_good')
    return render_template('new_property_id_name.html', title='Новый подтип вещи', form=form)


@main_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@main_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@main_app.route('/import', methods=['GET', 'POST'])
@login_required
def import_from_file():
    global for_import
    form = Import()
    if request.method == 'POST':
        if request.form["submit"] == 'Загузить файл':
            form.f = request.files["name"]
            if not form.f:
                print('No file')
            for_import.workbook = openpyxl.load_workbook(form.f)
            form.worksheets.choices = for_import.workbook.sheetnames
            return render_template('file_upload.html', title='Импорт из файла', form=form)
        elif request.form["submit"] == 'Импортировать данные':
            for_import.worksheet = form.worksheets.data
            print("Импортируем!!!")
            db_ses = db_session.create_session()
            for_import.parse_source(db_ses)
            """
            Добавить обработку файла - возможно старая пойдет!!!
            """

            return redirect('/')

    return render_template('file_upload.html', title='Импорт из файла', form=form)


def main():
    db_session.global_init('db/invent_db.sqlite')
    main_app.run(port=8000, host='127.0.0.1', debug=True)



if __name__ == '__main__':
    main()
