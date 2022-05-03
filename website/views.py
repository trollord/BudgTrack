from django import views
from flask import Blueprint, flash, render_template
from flask import request as rq
from flask_login import login_user, logout_user, login_required, current_user
from httpx import request
from .models import Note, db , User
from .Pyt_mailer import send_text

views = Blueprint('views', __name__)
c = 0
# sum of the data_amt


def remaining(user):
    sum = 0
    intake=0
    sum=sum_data_amt(user)
    for j in user.notes:
        try:
            intake=intake+int(j.in_take)
        except:
            intake=0        
    lim=User.query.filter_by(id=current_user.id).first()
    limit=lim.max_spend
    remaining=limit+intake-sum
    return remaining    
      
def sum_data_amt(user):
    sum = 0
    for note in user.notes:
        if note.data_amt>0:
            sum += int(note.data_amt)           
    return sum

@views.route('/')
def landing_main_page():
    return render_template('index.html')



@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if rq.method == 'POST':
        note = rq.form.get('note')
        amt = rq.form.get('amt')
        label = rq.form.get('drop-down')
        print(label, amt, note, list(rq.form.items()))
        in_take=0
        try:
            int(amt)
            it_is = True
        except ValueError:
            it_is = False
        if label == 'Cash_in':
            in_take=amt
            amt=0
        if len(note) < 1:
            flash('Description too short!', category='error')
        elif it_is == False:
            flash('Amount must be a number!', category='error')        
        else:                   
            new_note = Note(data=note, user_id=current_user.id,
                            data_amt=amt, label=label,in_take=in_take)
            db.session.add(new_note)
            db.session.commit()
            flash("Expense added succesfully ! ", category='success')
            balence=remaining(current_user)
            if balence<=0:
                flash('You have exceeded your limit', category='error')
                mesg=f"You have exceeded your limit for Maxium spend by : {abs(balence)}"
                send_text(current_user.email,mesg)

    return render_template("home.html", user=current_user, sum=sum_data_amt(current_user),remaining=remaining(current_user))



@views.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_note():
    if rq.method == 'POST':
        note_id = rq.form.get('note_id')
        note = Note.query.filter_by(id=note_id).first()
        db.session.delete(note)
        db.session.commit()
        flash('Expense deleted succesfully!', category='success')
    return render_template("home.html", user=current_user, sum=sum_data_amt(current_user) ,remaining=remaining(current_user))
