from flask import Flask, render_template, redirect
from data import db_session
from loginform import LoginForm

main_app = Flask(__name__)
main_app.config['SECRET_KEY'] = 'yandex_lyceum_project_secret_key'


@main_app.route('/')
@main_app.route('/index')
def index():
    user = "Ученик Яндекс.Лицея"
    return render_template('index.html', title='Домашняя страница',
                           username=user)


@main_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init('db/invent_db.sqlite')
    main_app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
