from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, \
    IntegerField, SelectField
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
