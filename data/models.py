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
    status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("condition.id"))
    status = relationship(Condition)
    # Тип - ид_тип_имущества
    item_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("item_type.id"))
    item_type = relationship(ItemType)
    #     Подтип - ид_подтип_имущества
    item_subtype_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(
        "item_subtype.id"))
    item_subtype = relationship(ItemSubtype)
    # Местонахождение - ид_место
    location_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("location.id"))
    location = relationship(Location)
    # Ответственный - ид_ответственного
    responsible_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    responsible = relationship(User)
    # !!! Часть комплекта: ид_комплекта - не реализовано
    #  # Не реализовано

    # Дата приобретения
    bought_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now().date())
    # Время эксплуатации (через сколько можно списывать)
    can_be_used = sqlalchemy.Column(sqlalchemy.Integer, default=5)


class ImportData:
    workbook = None
    worksheet = None

    def parse_source(self, session):
        the_sheet = self.workbook[self.worksheet]
        values = []
        columns = "AGH"
        row = 8
        rows_on_list = 20
        rows_between_lists = 10
        on_list = 0
        # self.items_table.setColumnCount(len(columns))
        # con = sqlite3.connect(self.db_name_edit.text())
        # cursor = con.cursor()
        all_goods = []
        que = ''
        while row <= the_sheet.max_row and self.not_braked:
            if on_list >= rows_on_list:
                on_list = 0
                row += rows_between_lists
            no = the_sheet[f"{columns[0]}{row}"]
            name = the_sheet[f"{columns[1]}{row}"]
            inv_num = the_sheet[f"{columns[2]}{row}"]
            if not inv_num.value:
                # если нет инвентарного номера то
                inv_num.value = "NO_INV_" + str(no.value)
            if no.value and int(no.value) == len(values) + 1:
                values.append((no.value, name.value, inv_num.value))
                self.items_table.setRowCount(self.items_table.rowCount() + 1)
                for i, item in enumerate(values[-1]):
                    self.items_table.setItem(self.items_table.rowCount() - 1, i, QTableWidgetItem(
                        str(item)))
                all_goods.append(tuple([name.value, inv_num.value]))
            else:
                print(f"{no.value} != {len(values) + 1}\n"
                      f"the data is not added:\n"
                      f"{name.value},{inv_num.value}")
            excluded = "excluded"  # только чтобы не подсвечивалась как ошибка
            que = f"INSERT into goods(goods_name, invent_number) " \
                  f"VALUES {', '.join([str(x) for x in all_goods])} " \
                  f"ON CONFLICT (invent_number) DO " \
                  f"UPDATE SET " \
                  f"comment = comment ||'\n Старое значение Наименования'||goods_name, " \
                  f"goods_name = {excluded}.goods_name"
            row += 1
            on_list += 1
            # self.keyPressEvent()
        cursor.execute(que)

        # db_sess.add(newtype)
        # db_sess.commit()

        # con.commit()
        # self.items_table.repaint()
        # con.close()
        # print(the_sheet['A28'].value)
        print("Импортировано записей:", len(values))
