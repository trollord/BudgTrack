from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
# from . import db
from models import User, Note
from sqlalchemy.inspection import inspect
# columns = [column.name for column in inspect(User).c['password'].columns]
# email = "mandaar@gmail.com"
# user = User.query.filter_by(email=email).first()


user = User.query.all()
for i in user:
    print(i.first_name)
    print(i.email)
    print(i.password)
    print(i.id)
user2 = Note.query.all()
for i in user2:
    print(i.data)
    print(i.data_amt)
    print(i.date)
    print(i.user_id)
print(User.query.all())
print(Note.query.all())
