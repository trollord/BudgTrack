import email
import random
import sqlite3
import imp
from unicodedata import name
from fastapi import Query
from flask import Blueprint, render_template, request, redirect, url_for, flash
from matplotlib.style import use
import pyautogui as py
from .models import User, Note
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from .py_ocr import ocr as image_to_text
from .webcam import theft_detection as cam
from .Pyt_mailer import send_mail,forgot_password
auth = Blueprint('auth', __name__)
import json

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def forgetpassword(email):
#     # py.alert(text='', title='', button='OK')
#     pas_key=random.randint(1, 1000000)
#     email_id=email
      
#     forgot_password(email_id,pas_key)  
    # key=py.prompt(text='', title='Enter the Access key sent to your Email/phone', default='')
    
    # if key==str(pas_key):
    #     py.alert(text='Password reset successful', title='', button='OK')
    # print(key)
    # use tkinter or pyqt insted of pyautogui
    # email verification using the same access key
    # gui for entering email and keyy
    # enter the key and validate if validated
    #
    # redirect to login page


@auth.route('/login', methods=['GET', 'POST'])
def login():

    # py.alert(text='', title='', button='OK')
    # data = request.form
    # print(data)

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if request.form.get('action1') == 'Login':
            email = request.form.get('email')
            password = request.form.get('password')                      
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash(f"{user.first_name} has been logged In Succesfully!!",
                          category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    cam()
                    send_mail(email, 'Intruder Alert!')
                    flash('Invalid Password.', category='error')

            else:
                flash('User Does not exist.', category='error')
        elif request.form.get('action2') == 'Forget Password':
            if user:
                # forgetpassword(email)
                pass
            else:
                flash('User Does not exist.', category='error')    
    return render_template('test.html', user=current_user)


@ auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.landing_main_page'))


@ auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # data = request.form
    # print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        # password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        max_spend=request.form.get('maxspend')
        if user:
            flash('Email aldready exists.', category='error')
        if len(email) < 4:
            flash('Email must be greater than 4 charecters.', category='error')
            pass
        elif len(password1) < 6:
            flash('Password must be greater than 6 charecters.', category='error')
            pass
        # elif password1 != password2:
        #     flash('Passwords do not match', category='error')
        #     pass
        elif len(first_name) < 2:
            flash('Name cannot be less than 2 charecters', category='error')
            pass
        elif max_spend.isdigit() == False:
            flash('Max spend must be a number', category='error')
            pass
        else:            
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'),max_spend=max_spend)
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

            # db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("test.html", user=current_user)

@auth.route('/reports', methods=['GET', 'POST'])
@login_required
def landing():
    user=current_user
    data = {"Label":"Amount"}
    for note in user.notes:
        label = note.label
        if note.label not in list(data.keys()):
            data[label] = note.data_amt
        else:
            data[label] = data[label] + note.data_amt
                
    final_data = []
    for label, amt in data.items():
        final_data.append([label, amt]) 
        
    final_data2=[['Month'],[]]     
    
    for i in final_data:
        final_data2[0].append(i[0]) 
         
    # get total spend monthwise
    def calculate_month(data):
        total_spend=0
        for i in data:
            total_spend=total_spend+i[1]
        return total_spend
    
    # a=[
    #     ['Month', 'Food', 'Education', 'Labour', 'Stationary', 'Clothes', 'xyz'],
    #                     ['2018/05', 165, 938, 522, 998, 450, 614],
    #                     ['2018/06', 135, 1120, 599, 1268, 288, 682],
    #                     ['2018/07', 157, 1167, 587, 807, 397, 623],
    #                     ['2019/08', 139, 1110, 615, 968, 215, 609],
    #                     ['2020/09', 136, 691, 629, 1026, 366, 569]
    #                 ]     

    final_data2=[]
    return render_template('reports_new.html', user=current_user,dt=json.dumps(final_data))    

@auth.route('/Ocr', methods=['GET', 'POST'])
@login_required
def ocr():
    return render_template('Ocr_nidhi.html', user=current_user)


@auth.route('/upload', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading', category='error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(
            f"C:/Users/mskas/OneDrive/Desktop/py4e/.vscode/ML/New folder/flask Web app/website/test_ocr/{filename}")
        #print('upload_image filename: ' + filename)
        image_to_text(
            f"C:/Users/mskas/OneDrive/Desktop/py4e/.vscode/ML/New folder/flask Web app/website/test_ocr/{filename}")
        # flash('Image successfully uploaded and displayed below', category='success')
        return redirect(url_for('views.home'))
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)
