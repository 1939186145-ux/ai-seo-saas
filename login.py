@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            print("LOGIN SUCCESS:", user.username)

            return redirect(url_for("home"))

        return "账号或密码错误"

    return render_template("login.html")