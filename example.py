from flask import *

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
    text_diff = ("This is a format string that is gonna be\n"
                +"in the website after sending request from form.\n"
                +"Some random Monty Python reference\n"
                +"Ni!\n")
    return render_template('result.html', result=text_diff)
