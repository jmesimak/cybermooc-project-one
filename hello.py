# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, make_response, g, send_file
import db_connection
import uuid
import hashlib

app = Flask(__name__)

# In-memory user logins.
# There might've been an article regarding data lifetime, long was good right?
logged_in_users = {}

@app.before_request
def check_token():
    if request.headers.get('Cookie'):
        token = request.headers.get('Cookie').split('=')[1]

        if token in logged_in_users.keys():
            g._user = logged_in_users[token]
            return

    g._user = False

@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.context_processor
def inject_user():
    return dict(user=g._user)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    else:
        # Wow, much secure, Yahoo enterprise best practice!!
        hasher = hashlib.md5()
        user_uuid = uuid.uuid4()
        username, password, bio = request.form.get("username"), request.form.get("password"), request.form.get("bio")
        hasher.update(password)

        users = db_connection.query("SELECT * FROM uzrs")
        usernames = [user[1] for user in users]
        if unicode(username) in usernames:
            return render_template("register.html", errors=["Username already exists"])

        else:
            db_connection.insert(
                '''INSERT INTO uzrs (uuid, name, password, bio) VALUES (?,?,?,?)''',
                [unicode(str(user_uuid), "utf-8"), username, unicode(hasher.hexdigest()), bio]
            )
            return redirect(url_for('hello', messages=["Thanks for registering :)"]))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        hasher = hashlib.md5()
        username, password = request.form.get("username"), request.form.get("password")
        user = db_connection.query('SELECT * FROM uzrs where name = "{0}"'.format(username))
        hasher.update(password)
        response = make_response(render_template("login.html"))
        if hasher.hexdigest() == user[0][2]:
            token = str(uuid.uuid4())
            response.set_cookie("auth-token", value=token)
            logged_in_users[token] = user[0]

        return response

@app.route("/recipe/<recipe_uuid>", methods=["GET"])
def get_recipe(recipe_uuid):
    recipe = db_connection.query('SELECT * FROM recipe WHERE uuid = "{0}"'.format(recipe_uuid))[0]
    return render_template("recipe.html", recipe=recipe)

@app.route("/recipe/add", methods=["GET"])
def create_recipe_form():
    return render_template("add_recipe.html")

@app.route("/recipe", methods=["POST"])
def add_recipe():
    recipe_id = str(uuid.uuid4())
    img = request.files['file']
    filename = ""
    if img is not None:
        filepath = "./static/images/"+recipe_id+".png"
        filename = recipe_id+".png"

    db_connection.add_recipe({
        "recipe_id": recipe_id,
        "owner": "0208315f-96ae-46d8-8366-6af5e26d0f86",
        "title": request.form.get("title"),
        "content": request.form.get("content"),
        "image": filename
    })
    img.save(filepath)
    return redirect(url_for('list_recipes'))

@app.route("/recipe/list")
def list_recipes():
    recipes = db_connection.get_n_latest_recipes(100)
    return render_template("recipes.html", recipes=recipes)

@app.route("/recipe/search")
def search_recipes():
    keyword = request.args.get('keyword')
    if keyword is not None:
        recipes = db_connection.search_recipes(keyword)
        return render_template("recipes.html", recipes=recipes)
    else:
        return render_template("search.html")

@app.route("/recipe/image")
def download_recipe_image():
    img = request.args.get('img')
    filepath = "static/images/{0}".format(img)
    return send_file(filepath, mimetype="image/png")

if __name__ == "__main__":
    app.run()
