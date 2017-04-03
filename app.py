from datetime import *
from flask import *
from models.images import Image
import mlab
import os
from werkzeug.utils import *
from models.user import User
from flask_login import *
from sessionuser import SessionUser


app = Flask(__name__)
mlab.connect()
app.config["UPLOAD_PATH"] = os.path.join(app.root_path, "uploads")
if not os.path.exists(app.config["UPLOAD_PATH"]):
    os.makedirs(app.config["UPLOAD_PATH"])

app.secret_key = "abc"

login_manager = LoginManager()
login_manager.init_app(app)

# admin_user = User()
# admin_user.useraname = 'admin'
# admin_user.password = 'admin'
# admin_user.save()


@login_manager.user_loader
def user_loader(user_token):
    found_user = User.objects(token=user_token).first()
    if found_user:
        session_user = SessionUser(found_user.id)
        return session_user


@app.route('/')
def hello_world():
    return redirect(url_for("foodblog"))

number_of_visitor = 0


@app.route('/login')
def login():
    current_time_on_server = str(datetime.now())
    global number_of_visitor
    number_of_visitor += 1

    return render_template("login.html", current_time=current_time_on_server, number_of_visitor_1=number_of_visitor)


@app.route('/food')
def food():
    return render_template("food.html", list_food = Image.objects())


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/css')
def css():
    return render_template("css_demo.html")


@app.route('/w3css')
def w3css():
    return render_template("w3css.html")


@app.route('/delete_image', methods=["GET", "POST"])
def delete():
    if(request.method == "GET"):
        return render_template("delete_image.html")
    if(request.method == "POST"):
        new_image = Image.objects(title=request.form["title"]).first()
        if new_image is not None:
            new_image.delete()
        return render_template("delete_image.html")

@app.route('/add_image', methods=["GET", "POST"])
@login_required
def add():
    if(request.method == "GET"):
        return render_template("add_image.html")
    if(request.method == "POST"):
        file =request.files["source"]
        if file:
            filename = secure_filename(file.filename)
            if os.path.exists(os.path.join(os.path.join(app.config["UPLOAD_PATH"], filename))):
                name_index = 0
                #filename =home.png
                original_name = filename.rsplit('.', 1)[0]
                original_extension = filename.rsplit('.', 1)[1]
                while os.path.join(app.config["UPLOAD_PATH"], filename):
                    name_index += 1
                    # new filename = home (1).png
                    filename = "{0} ({1}).{2}".format(original_name, name_index, original_extension)
                    #change filename add(name_index)
            file.save(os.path.join(app.config["UPLOAD_PATH"], filename))
            new_image = Image()
            new_image.src = url_for('uploaded_file', filename=filename)
            new_image.title = request.form["title"]
            new_image.description = request.form["description"]
            new_image.save()
            return render_template("add_image.html")


@app.route('/update_image', methods=["GET", "POST"])
def update():
    if (request.method == "GET"):
        return render_template("update_image.html")
    if (request.method == "POST"):
        new_image = Image.objects(title=request.form["title"]).first()
        if new_image is not None:
            new_image.src = request.form["new_source"]
            new_image.description = request.form["new_description"]
            new_image.save()
        return render_template("update_image.html")


@app.route('/foodblog')
def foodblog():
    return render_template("foodblog.html", list_food = Image.objects())


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_PATH"], filename)


@app.route('/login_web', methods=["GET", "POST"])
def login_web():
    if request.method == "GET":
        return render_template("login_web.html")
    elif request.method == "POST":
        user = User.objects(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            session_user = SessionUser(user.id)
            user.update(set__token=str(user.id))
            login_user(session_user)
            return render_template("login_web.html")
        else:
            pass
            return redirect(url_for("foodblog"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login_web'))

if __name__ == '__main__':
    app.run()