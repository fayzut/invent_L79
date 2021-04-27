import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Condition(SqlAlchemyBase):
    __tablename__ = 'condition'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


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
    status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("condition.id"),
                                  default=0)
    status = relationship(Condition)
    # Тип - ид_тип_имущества
    item_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("item_type.id"),
                                     default=0)
    item_type = relationship(ItemType)
    #     Подтип - ид_подтип_имущества
    item_subtype_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(
        "item_subtype.id"), default=0)
    item_subtype = relationship(ItemSubtype)
    # Местонахождение - ид_место
    location_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("location.id"),
                                    default=0)
    location = relationship(Location)
    # Ответственный - ид_ответственного
    responsible_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"),
                                       default=0)
    responsible = relationship(User)
    # !!! Часть комплекта: ид_комплекта - не реализовано
    #  # Не реализовано

    # Дата приобретения
    bought_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now().date())
    # Время эксплуатации (через сколько можно списывать)
    can_be_used = sqlalchemy.Column(sqlalchemy.Integer, default=5)



