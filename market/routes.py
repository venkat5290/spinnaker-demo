from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User, Faculty, TestUpload, Emp
from market.forms import *
from market import db
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')

        #selling item logic
        selling_item = request.form.get('sell_item')
        print(selling_item)
        s_item_object = Item.query.filter_by(name=selling_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items,
                               purchase_form=purchase_form, sell_form=sell_form, owned_items=owned_items)


@app.route('/register',methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email_address=form.email_address.data,
                        password=form.password1.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Success! Account created Successfully! you are now logged in as {new_user.username}', category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('username and passowrd is incorrect',category='danger')
    return render_template('login_page.html', form=form)


@app.route('/logout_page')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))


@app.route('/add-item',methods=['GET', 'POST'])
def add_item_page():
    form = FacultyForm()
    if form.validate_on_submit():
        new_faculty = Faculty(name=form.name.data,
                              email_address=form.email_address.data,
                              designation=form.designation.data)
        db.session.add(new_faculty)
        db.session.commit()
        flash(f'Succes ! New faculty : {new_faculty.name}added succesfully', category='success')
        return redirect(url_for('add_item_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('add-item.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        print(f)
        filename = secure_filename(f.filename)
        f.save(os.path.join('market/static/uploads/' + filename))
        print(f.read())
        file_up = TestUpload(name=filename, data=f.read())
        db.session.add(file_up)
        db.session.commit()
        flash(f'Image Saved Succesfully', category='success')
        return redirect('/download/'+filename)
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with uploads: {err_msg}', category='danger')
    return render_template('upload.html', form=form)


@app.route("/download/<filename>", methods=["GET"])
def download_page(filename):
    return render_template('download.html', value=filename)


@app.route('/emp', methods=['GET', 'POST'])
def emppage():
    form = EmpForm()
    if form.validate_on_submit():
        f = form.photo.data
        print(f)
        filename = secure_filename(f.filename)
        f.save(os.path.join('market/static/uploads/' + filename))
        new_faculty = Emp(name=form.name.data,
                          email_address=form.email_address.data,
                          designation=form.designation.data,
                          file_name=filename
                              )
        db.session.add(new_faculty)
        db.session.commit()
        flash(f'Succes ! New faculty : {new_faculty.name}added succesfully', category='success')
        return redirect('/download/'+filename)
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('emp.html', form=form)
