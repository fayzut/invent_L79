from sqlalchemy.orm import Session

from data.models import Good


class ImportData:
    workbook = None
    worksheet = None
    not_braked = True

    def parse_source(self, session: Session):
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
            new_item = Good()
            if no.value and int(no.value) == len(values) + 1:
                values.append((no.value, name.value, inv_num.value))

                new_item.name = name.value
                new_item.invent_number = inv_num.value

                all_goods.append(new_item)
                # print(no.value, new_item.name, new_item.invent_number, new_item.status,
                #       new_item.id)
                qw = session.query(Good)
                qw = qw.filter(Good.id == inv_num.value)
                old_item = qw.first()
                if old_item:
                    session.merge(new_item)
                else:
                    session.add(new_item)
            else:
                print(f"{no.value} != {len(values) + 1}\n"
                      f"the data is not added:\n"
                      f"{name.value},{inv_num.value}")
                new_item.comment = f"old_comment ||'\n Старое значение Наименования'||{name.value}"
                new_item.name = f"excluded.{name.value}"
                # print(no.value, new_item.name, new_item.invent_number)
                session.add(new_item)
            # excluded = "excluded"  # только чтобы не подсвечивалась как ошибка
            # que = f"INSERT into goods(goods_name, invent_number) " \
            #       f"VALUES {', '.join([str(x) for x in all_goods])} " \
            #       f"ON CONFLICT (invent_number) DO " \
            #       f"UPDATE SET " \
            #       f"comment = comment ||'\n Старое значение Наименования'||goods_name, " \
            #       f"goods_name = {excluded}.goods_name"
            row += 1
            on_list += 1
            # self.keyPressEvent()
        session.commit()

        # print(the_sheet['A28'].value)
        print("Импортировано записей:", len(values))
