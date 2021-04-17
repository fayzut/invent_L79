from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, \
    IntegerField
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
    status_id = 0
    item_type_id = 0
    item_subtype_id = 0
    location_id = 0
    responsible_id = 0
    submit = SubmitField('Добавить')
    cancel = SubmitField('Отмена')
