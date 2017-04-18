from flask import *
import sqlite3
import differ_loader
import ast

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar("DIFF_SETTINGS", silent=True)

def importance(result):
    important = []
    unimportant = []
    for format, text in result:
        if text[0] == "added" or text[0] == "removed":
            important.append((format, text))
        else:
            unimportant.append((format, text))
    return important, unimportant

@app.cli.command("init_db")
def init_db():
    db = sqlite3.connect("results.db")
    with app.open_resource("schema.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

@app.route("/")
def index():
    return redirect(url_for("get_rpm_request"))

@app.route("/rpm")
def get_rpm_request():
    return render_template("rpm_request.html")

@app.route("/diff", methods=["POST"])
def request_processor():
    pkg = request.form["pkg"]
    additional = (request.form["pkg1_release"],
                  request.form["pkg1_arch"],
                  request.form["pkg2_release"],
                  request.form["pkg2_arch"]
                )
    db = sqlite3.connect("results.db")
    cur = db.cursor()
    cur.execute("SELECT result FROM results WHERE pkg=? AND pkg1_release=? AND pkg1_arch=? AND pkg2_release=? AND pkg2_arch=?",(pkg, *additional))
    result = cur.fetchone()
    if result is None:
        differ = differ_loader.load_differ(pkg,
                                           pkg,
                                           "RPM",
                                           additional
                                          )
        result = differ.get_diff()
        id = cur.lastrowid

        cur.execute("INSERT INTO results (pkg, pkg1_release, pkg1_arch, pkg2_release, pkg2_arch, result) values (?,?,?,?,?,?);",
                    (pkg, *additional, repr(result)))
        db.commit()
    else:
        result = ast.literal_eval(result[0])
    db.close()
    important, unimportant = importance(result)
    return render_template("result.html", important=important, unimportant=unimportant)
