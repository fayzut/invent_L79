from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, \
    IntegerField, SelectField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class NewUser(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Логин-почта', validators=[DataRequired()])
    about = TextAreaField('Кратко')
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
    cancel = SubmitField('Отмена')


class NewGood(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    invent_number = StringField('Инвентарный номер', validators=[DataRequired()])
    comment = TextAreaField('Описание')
    is_on_balance = BooleanField('На балансе', default=True)
    bought_date = DateField('Дата приобретения', format='%d.%m.%Y')
    can_be_used = IntegerField('Срок до возможного списания', default='5')
    status_id = SelectField('Работоспособность')
    item_type_id = SelectField('Тип вещи')
    item_subtype_id = SelectField('Подтип вещи')
    location_id = SelectField('Местонахождение')
    responsible_id = SelectField('Ответственный')
    submit = SubmitField('Добавить')
    cancel = SubmitField('Отмена')


class NewPropertyWithIdName(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    submit = SubmitField('Добавить')
    cancel = SubmitField('Отмена')


class NewLocation(NewPropertyWithIdName):
    pass


class NewItemType(NewPropertyWithIdName):
    pass


class NewItemSubtype(NewPropertyWithIdName):
    type_id = SelectField('Тип вещи')


class Import(NewPropertyWithIdName):
    name = FileField('Файл ', validators=[DataRequired()])

    '''
    def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    return """
        <html>
            <body>
                <h1>Transform a file demo</h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """

@app.route('/transform', methods=["POST"])
def transform_view():
    file = request.files['data_file']
    if not file:
        return "No file"

    file_contents = file.stream.read().decode("utf-8")

    result = transform(file_contents)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response
   '''