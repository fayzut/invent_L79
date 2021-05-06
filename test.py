from flask import Flask, render_template, url_for
import os

PEOPLE_FOLDER = 'image'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_url_path, PEOPLE_FOLDER)


@app.route('/')
@app.route('/index')
def show_index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'barcode.png')
    full_filename = url_for('static', filename='images/barcode.png')
    print(full_filename)
    return render_template("test.html", user_image=full_filename)


print(app.static_url_path)
print(app.config['UPLOAD_FOLDER'])
app.run(port=8000, host='127.0.0.1', debug=True)
