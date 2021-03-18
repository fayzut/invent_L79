from flask import Flask, render_template, redirect

from loginform import LoginForm

main_app = Flask(__name__)
main_app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


if __name__ == '__main__':
    main_app.run(port=8000, host='127.0.0.1')
