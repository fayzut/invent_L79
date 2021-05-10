import os
from urllib.parse import quote
from io import BytesIO

import pytils
from barcode import EAN13, Code39
from barcode.writer import ImageWriter, SVGWriter

# print to a file-like object:
# rv = BytesIO()
# EAN13(str(100000902922), writer=ImageWriter()).write(rv)

# or sure, to an actual file:
from flask import url_for


class ImageWriterCyr(ImageWriter):
    # Подписывает штрихкод русским текстом, унаследован от стандартного класса
    def _paint_text(self, xpos, ypos):
        backup_text = self.text
        if self.human != '':
            self.text = self.human
        super()._paint_text(xpos, ypos)
        self.text = backup_text


def get_barcode_file(text, folder):
    filename = os.path.join(folder, f'barcode_{quote( text)}.png')
    text1 = f'{quote(text)}'
    # text1 = pytils.translit.translify(text)

    # print(text1)
    with open('static\\' + filename, 'wb') as f:
        iw = ImageWriterCyr()
        iw.human = text
        ean = Code39(text1, writer=iw)
        ean.write(f)
        full_filename = os.path.join('\\static', filename)
        return full_filename
