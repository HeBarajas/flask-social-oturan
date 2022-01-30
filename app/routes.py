from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, CreatePost, LoginForm
from app.models import Post, User


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)
    

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get the data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data
       
        #Check if either the username or email is alrady in db
        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
        
        #if it is, return back to register
        if user_exists:
            return redirect(url_for('register'))

        #Create a new user instance using form data
        User(username=username, email=email, password = password)


        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = CreatePost()
    if form.validate_on_submit():
        print('FORM HAS BEEN CREATED')
        title = form.title.data
        text = form.text.data
        Post(title=title, text=text)
        print(title, text)
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)

@app.route('/login', methods=['GET', 'POST'] )
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #grab the data from the form
        username = form.username.data
        password = form.password.data

        #Query user table for user with username
        user = User.query.filter_by(username=username).first()

        #if the user does not exist or the user has an incorrect password
        if not user or not user.check_password(password):
            #redirect to login page
            print('That username and password is incorrect')
            return redirect(url_for('login'))

    #if user does exist and correct password, log user in
        login_user(user)
        print('User has been logged in')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/edit_post/<int:p_id>/edit', methods=["GET", "POST"])
def edit_post(p_id): 
    posts = Post.query.get_or_404(p_id)
    form = CreatePost()
    if form.validate_on_submit():
        # Get data from form
        title = form.title.data
        text = form.text.data
        # Update the product with the new info
        posts.title = title
        posts.text = text

        posts.save()

        # flash message
        flash(f"{posts.title} has been updated", "primary")
        return redirect(url_for('index', p_id=posts.id))

    return render_template('edit_post.html', posts=posts, form=form)

@app.route('/edit_post/<int:p_id>/delete')
def delete_post(p_id):
    posts = Post.query.get_or_404(p_id)
    posts.delete()
    flash(f'{posts.title} has been deleted', 'danger')
    return redirect(url_for('index'))