from flask import render_template, url_for, flash, redirect, request, abort
from pedalpowered.models import User, rides
from pedalpowered.forms import RegisterForm, LoginForm, UpdateAcctForm, NewRideForm, FilterByDateForm
from pedalpowered import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from pedalpowered.stats_calculator import get_user_stats, graph_money_saved, graph_distance_ridden
from datetime import datetime,timezone

@app.route("/home")
@login_required
def home():
    ridelog = rides.query.all()
    return render_template("home.html",posts= ridelog)

@app.route("/logride", methods = ['GET','POST'])
@login_required
def logride():
    form = NewRideForm()
    if form.validate_on_submit():
        ride_datetime = datetime.combine(
            form.ride_date.data, 
            datetime.now(timezone.utc).time()
        )
        new_ride = rides(title = form.title.data,ride_date=ride_datetime, distance = form.distance.data, gas_price = form.gas_price.data,
                         car_mpg = form.car_mpg.data, user_comment = form.comment.data, author = current_user)
        new_ride.calculate_money_saved()
        db.session.add(new_ride)
        db.session.commit()
        flash('Ride logged!', 'success')
        return redirect(url_for('home'))
    return render_template('logride.html', title='Log a new ride', form=form, legend = 'New ride')

@app.route("/stats", methods = ['GET','POST'])
@login_required
def stats():

    form = FilterByDateForm()
    
    start_date = None
    end_date = None
    
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

    statistics = get_user_stats(current_user.id, start_date, end_date)
    money_saved_graph = graph_money_saved(current_user.id, start_date, end_date)
    amount_biked_graph = graph_distance_ridden(current_user.id, start_date, end_date)
    return render_template("stats.html", title="Your Stats", cumulative_statistics=statistics, money_saved=money_saved_graph, amount_biked = amount_biked_graph, form = form)

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        #Hash the password so it can't be taken directly off the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created, please log in.','success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form = form)

@app.route("/", methods = ['GET','POST'])
@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {form.username.data}!','success')
            #Ternary conditional!
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login failed, please try again.','danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def set_profile_pic(form_picture):
    random_pic_name = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_file_name = random_pic_name + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics',picture_file_name)
    output_size = (100,100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    return  picture_file_name


@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAcctForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = set_profile_pic(form.picture.data)
            current_user.img_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info upates', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.img_file)
    return render_template("account.html", title="Login", image_file = image_file, form=form)

#python -m flask --app PedalPowered run

@app.route("/post/<int:post_id>")
def post(post_id):
    post = rides.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post = post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = rides.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewRideForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.distance = form.distance.data
        post.car_mpg = form.car_mpg.data
        post.gas_price = form.gas_price.data
        db.session.commit()
        flash('Ride updated!','success')
        return redirect(url_for('post', post_id=post.id))
    #Loads in data from old post
    elif request.method == 'GET':
        form.title.data = post.title
        form.distance.data = post.distance
        form.car_mpg.data = post.car_mpg
        form.gas_price.data = post.gas_price
    return render_template('logride.html', title='Update a ride',
                            form=form, legend = 'Update ride')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_ride(post_id):
    post = rides.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ride deleted!','success')
    return redirect(url_for('home'))


#View indvidual profle like with posts!!
@app.route("/user/<string:username>")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    is_friend = current_user.is_friend(user)
    return render_template('user_profile.html', user=user, is_friend=is_friend)

@app.route("/add_friend/<int:user_id>")
@login_required
def add_friend(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot add yourself as a friend!', 'warning')
    else:
        current_user.add_friend(user)
        db.session.commit()
        flash(f'You are now friends with {user.username}!', 'success')
    return redirect(url_for('user_profile', username=user.username))

@app.route("/remove_friend/<int:user_id>")
@login_required
def remove_friend(user_id):
    user = User.query.get_or_404(user_id)
    current_user.remove_friend(user)
    db.session.commit()
    flash(f'You removed {user.username} from your friends.', 'info')
    return redirect(url_for('user_profile', username=user.username))

@app.route("/friends")
@login_required
def friend_list():
    friends = current_user.friends.all()
    return render_template('friends.html', friends=friends)

@app.route("/users")
@login_required
def user_list():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('user_list.html', users=users)