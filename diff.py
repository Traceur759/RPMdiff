from flask import *
import json
import differ_loader

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DIFF_SETTINGS', silent=True)

@app.route('/')
def show_entries():
    return render_template('rpm_request.html')

@app.route('/diff', methods=['POST'])
def request_processor():
    pkg1 = request.form['pkg1']
    pkg2 = request.form['pkg2']
    differ = differ_loader.load_differ(pkg1,
                                       pkg2
                                      )
    text_diff = differ.get_diff()
    return render_template('result.html', result=text_diff)
