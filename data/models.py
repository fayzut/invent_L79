import datetime

import sqlalchemy

from .db_session import SqlAlchemyBase


class Good(SqlAlchemyBase):
    __tablename__ = 'goods'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # Инвентарный номер
    invent_number = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    # Примечание: описание текстом
    comment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Баланс/Забаланс - ?
    is_on_balance = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    # Состояние - ид_состояние
    status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("condition.id"))
    # Тип - ид_тип_имущества
    item_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("item_type.id"))
    #     Подтип - ид_подтип_имущества
    item_subtype_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(
        "item_subtype.id"))
    # Местонахождение - ид_место
    location_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("location.id"))
    # Ответственный - ид_ответственного
    responsible_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    # !!! Часть комплекта: ид_комплекта - не реализовано
    #  # Не реализовано

    # Дата приобретения
    bought_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now().date())
    # Время эксплуатации (через сколько можно списывать)
    can_be_used = sqlalchemy.Column(sqlalchemy.Integer, default=5)


class User(SqlAlchemyBase):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)


class Condition(SqlAlchemyBase):
    __tablename__ = 'condition'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Location(SqlAlchemyBase):
    __tablename__ = 'location'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class ItemType(SqlAlchemyBase):
    __tablename__ = 'item_type'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class ItemSubtype(SqlAlchemyBase):
    __tablename__ = 'item_subtype'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('item_type.id'))
