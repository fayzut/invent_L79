from flask import Flask, render_template, redirect
from data import db_session
from data.models import Good
from loginform import LoginForm

main_app = Flask(__name__)
main_app.config['SECRET_KEY'] = 'yandex_lyceum_project_secret_key'


@main_app.route('/')
@main_app.route('/index')
def index():
    db_ses = db_session.create_session()

    user = db_ses.query(Good).all()
    return render_template('index.html', title='Главная',
                           goods=user)


@main_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init('db/inventarizaciya10.db')
    main_app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
