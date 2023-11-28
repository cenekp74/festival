from app.db_classes import User
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response
from app.forms import LoginForm# , UpdateaccForm, RegistrationForm
from app import app, db, bcrypt
from flask_login import login_user, logout_user, current_user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static/img', 'favicon.ico')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        flash('Přihlášení se nezdařilo - zkontrolujte email a heslo', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route('/account', methods=['GET', 'POST'])
# def account():
#     form = UpdateaccForm()
#     if form.validate_on_submit():
#         print(form)
#         if form.pp.data:
#             randomName = secrets.token_hex(10)
#             _, extension = os.path.splitext(form.pp.data.filename)
#             imageName = randomName + extension
#             imagePath = os.path.join(app.root_path, 'static/pp', imageName)
#             imageSize = (125, 125)
#             newImage = Image.open(form.pp.data)
#             newImage.thumbnail(imageSize)
#             newImage.save(imagePath)
#             current_user.pp = imageName

#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Account updated successfully', 'success')
#         redirect(url_for('account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     pp = url_for('static', filename='pp/' + current_user.pp)
#     return render_template('account.html', pp=pp, form=form)



# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)