import os
from io import BytesIO

import pytils
from barcode import EAN13, Code39
from barcode.writer import ImageWriter, SVGWriter

# print to a file-like object:
# rv = BytesIO()
# EAN13(str(100000902922), writer=ImageWriter()).write(rv)

# or sure, to an actual file:
from flask import url_for


def get_barcode_file(text, folder):
    filename = os.path.join(folder, f'barcode_{text}.png')
    text = pytils.translit.translify(text)
    with open('static\\' + filename, 'wb') as f:
        ean = Code39(text, writer=ImageWriter())
        ean.write(f)
        full_filename = os.path.join('\\static', filename)
        return full_filename
