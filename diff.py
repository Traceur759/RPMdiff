from flask import *
import sqlite3
import differ_loader

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DIFF_SETTINGS', silent=True)

@app.route('/')
def index():
    return redirect(url_for('get_rpm_request'))

@app.route('/rpm')
def get_rpm_request():
    return render_template('rpm_request.html')

@app.route('/diff', methods=['POST'])
def request_processor():
    pkg1 = request.form['pkg1']
    pkg2 = request.form['pkg2']
    additional = (request.form['pkg1_release'],
                  request.form['pkg1_arch'],
                  request.form['pkg2_release'],
                  request.form['pkg2_arch']
                )
    differ = differ_loader.load_differ(pkg1,
                                       pkg2,
                                       "RPM",
                                       additional
                                      )
    text_diff = differ.get_diff()
    return render_template('result.html', result=text_diff)
