from datetime import datetime

from flask import Flask, render_template, redirect
from data import db_session
from data.models import Good, User
from loginform import LoginForm, NewUser, NewGood
from flask_login import login_user, logout_user, login_required

main_app = Flask(__name__)
main_app.config['SECRET_KEY'] = 'yandex_lyceum_project_secret_key'


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
        user = User()
        user.name = form.name.data
        user.about = form.about.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        user.created_date = datetime.now()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация пользователя',
                           form=form)


@main_app.route('/new_good', methods=['GET', 'POST'])
# @login_required
def new_good():
    form = NewGood()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        good = Good()
        good.name = form.name.data
        good.invent_number = form.invent_number.data
        good.comment = form.comment.data
        good.is_on_balance = form.is_on_balance.data
        good.status_id = form.status_id
        good.item_type_id = form.item_type_id
        good.item_subtype_id = form.item_subtype_id
        good.location_id = form.location_id
        good.responsible_id = form.responsible_id
        good.bought_date = form.bought_date.data
        good.can_be_used = form.can_be_used.data
        db_sess.add(good)
        db_sess.commit()
        return redirect('/')

    return render_template('new_good.html', title='Новая вещь', form=form)


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


def main():
    db_session.global_init('db/invent_db.sqlite')
    main_app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
