import requests
from flask_login import login_user, logout_user, login_required, current_user
from .models import Note, db
from flask import flash


def ocr(imageFile):
    receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'
    # imageFile = "bill.jpg"
    r = requests.post(receiptOcrEndpoint, data={
        'client_id': 'TEST',
        'recognizer': 'auto',
        'ref_no': 'ocr_python_123',
    },
        files={"file": open(imageFile, "rb")})
    r = r.json()
    in_take=0
    # print(r)
    try:
        amt = int(r['receipts'][0]['total'])
    except:
        amt = 0
    try:
        note = r['receipts'][0]['merchant_name']
    except:
        note = "NULL"
    new_note = Note(data=note, user_id=current_user.id, data_amt=amt,in_take=in_take)
    db.session.add(new_note)
    db.session.commit()
    flash("Expense added succesfully ! ", category='success')
    return
