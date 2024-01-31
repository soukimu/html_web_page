from flask import render_template, request, redirect, url_for, jsonify, abort
from testapp.entity.db import db
from testapp.entity.employee import Employee
from testapp.entity.pairs import Pairing
from testapp.entity.users import User
from testapp.entity.has_sent import HasSent
from testapp import app
import random
from sqlalchemy import not_, exists, and_


@app.get('/')
def employee_list():
    employees = Employee.query.all()
    return render_template('testapp/employee_list.html', employees=employees)

@app.get('/add_employee')
def get_add_employee():
    if request.method == 'GET':
        return render_template('testapp/add_employee.html')

@app.post('/add_employee')
def post_add_employee():
    if request.method == 'POST':
        form_name = request.form.get('name')
        form_mail = request.form.get('mail')
        form_is_remote = request.form.get('is_remote', default=False, type=bool)
        form_department = request.form.get('department')
        form_year = request.form.get('year', default=0, type=int)
        
        employee = Employee(
            name=form_name,
            mail=form_mail,
            is_remote=form_is_remote,
            department=form_department,
            year=form_year
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('employee_list'))
    

@app.route('/employees/<int:id>')
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    return render_template('testapp/employee_detail.html', employee=employee)


@app.get('/employees/<int:id>/edit')
def employee_edit(id):
    # 編集ページ表示用
    employee = Employee.query.get(id)
    return render_template('testapp/employee_edit.html', employee=employee)

@app.post('/employees/<int:id>/update')
def employee_update(id):
    employee = Employee.query.get(id)  # 更新するデータをDBから取得
    employee.name = request.form.get('name')
    employee.mail = request.form.get('mail')
    employee.is_remote = request.form.get('is_remote', default=False, type=bool)
    employee.department = request.form.get('department')
    employee.year = request.form.get('year', default=0, type=int)

    db.session.merge(employee)
    db.session.commit()
    return redirect(url_for('employee_list'))

@app.route('/employees/<int:id>/delete', methods=['POST'])  
def employee_delete(id):  
    employee = Employee.query.get(id)   
    db.session.delete(employee)  
    db.session.commit()  
    return redirect(url_for('employee_list'))

@app.get('/login')
def get_login_page():
    return render_template('testapp/login.html')

@app.post('/login')
def post_user():
    name = request.form.get('name')
    mail = request.form.get('email')
    user_by_name = User.query.filter_by(name=name).first()
    user_by_mail = User.query.filter_by(mail=mail).first()
    print('----------------')
    print(f'input_name:{name}, input_mail:{mail}')
    print('----------------')
    is_mail_in_users = True if user_by_mail is not None else False
    is_name_in_users = True if user_by_name is not None else False
    if is_mail_in_users:
        current_user = user_by_mail
    elif is_name_in_users:
        current_user = user_by_name
        if user_by_name.mail:
            return render_template('testapp/login.html', error='メールアドレスが一致しません')
        current_user.mail = mail
        db.session.commit()
    else:
        return render_template('testapp/login.html', error='メールアドレスが一致しません')
    return redirect(url_for('get_status', current_user_id=current_user.id))

@app.route('/top/<current_user_id>')
def get_status(current_user_id):
    if current_user_id is not None:
        # Userテーブルからuser_idが一致するレコードを取得
        current_user = User.query.filter_by(id=current_user_id).first()
        print('--------check:get_status()--------')
        print(f'current_user:{current_user}')
        print('----------------')
        
        # HasSentテーブルからuser_idが一致するレコードを取得
        has_sent = HasSent.query.filter_by(user_id=current_user_id).first()
        # Pairingテーブルで、current_user_idがgiver_idカラムに存在するかどうかを確認
        has_target_user = Pairing.query.filter(Pairing.giver_id == current_user_id).first() is not None
        if current_user:
            # userデータとhas_sentデータをレスポンスとして返す
            response_data = {
                'current_user_id': current_user.id,
                'current_user_name': current_user.name,
                'has_target_user': has_target_user,
                'has_sent': has_sent is not None  # has_sentレコードが存在するかどうか
            }
            return render_template('testapp/top.html', response_data=response_data)
        

@app.route('/lottery/<int:current_user_id>')
def get_lottery_page(current_user_id):
    print('-------get_lottery_pageの確認---------')
    print(current_user_id)
    current_user_id = current_user_id
    print('----------------')
    has_target_user = Pairing.query.filter(Pairing.giver_id == current_user_id).first() is not None
    
    if has_target_user:
        return redirect(url_for('get_lottery_result', current_user_id=current_user_id))
    return render_template('testapp/lottery.html', current_user_id=current_user_id)


@app.post('/lottery/<int:current_user_id>')
def post_lottery_result(current_user_id):
    print('-------current_user_idの確認-------')
    print(current_user_id)
    print('----------------')
    
    current_user = User.query.filter_by(id=current_user_id).first()
    
    # ログインユーザーの性別に基づいて異性を探す
    target_gender = 'F' if current_user.gender == 'M' else 'M'
    # Pairingテーブルに存在するすべてのreceiverのidをサブクエリとして取得
    subquery = db.session.query(Pairing.receiver_id).subquery()

    # Userテーブルから、そのidが上記のサブクエリに含まれていないすべてのユーザーを取得
    possible_targets = User.query.filter(
        and_(
            not_(User.id.in_(subquery)),
            User.gender == target_gender
        )
    ).all()

    print(f'target_gender: {target_gender}')
    print(f'available_partners: {possible_targets}')
    
    # ランダムに異性を選ぶ
    partner = random.choice(possible_targets)
    
    # ペアをデータベースに保存
    new_pairing = Pairing(giver_id=current_user.id, receiver_id=partner.id)
    db.session.add(new_pairing)
    db.session.commit()

    # ペアをリザルトページに渡す
    return redirect(url_for('get_lottery_result', current_user_id=current_user.id))

@app.get('/result/<int:current_user_id>')
def get_lottery_result(current_user_id):
    # Pairingテーブルからcurrent_user_idをgiver_idとして持つレコードを検索
    pairing = Pairing.query.filter_by(giver_id=current_user_id).first()
    
    if not pairing:
        # ペアリングが見つからない場合
        return render_template('error.html', message='Pairing not found')

    # current_user_idがgiverならreceiverを取得、receiverならgiverを取得
    pair_user = User.query.get(pairing.receiver_id)
    
    if not pair_user:
        # 対応するペアのユーザーが見つからない場合
        return render_template('error.html', message='Pair user not found')
    
    # 対応するペアのユーザーのnameとlikeを返却
    return render_template('testapp/result.html', name=pair_user.name, like=pair_user.like, current_user_id=current_user_id)

@app.post('/congratulation/<int:current_user_id>')
def post_has_sent(current_user_id):
    has_sent = HasSent(user_id=current_user_id)
    db.session.add(has_sent)
    db.session.commit()
    return render_template('testapp/congratulation.html', current_user_id=current_user_id)

@app.post('/congratulation/<int:current_user_id>/delete')
def delete_has_sent(current_user_id):
    has_sent_records =  HasSent.query.filter_by(user_id=current_user_id).all()
    for has_sent_record in has_sent_records:
        db.session.delete(has_sent_record)
    db.session.commit()
    print('----------------')
    print('delete_has_sent')
    print('----------------')
    return redirect(url_for('get_status', current_user_id=current_user_id))

@app.get('/likes/<int:current_user_id>')
def get_likes(current_user_id):
    likes = User.query.get(current_user_id).like
    return render_template('testapp/like.html', current_user_id=current_user_id, likes=likes)

@app.post('/likes/<int:current_user_id>/put')
def post_likes(current_user_id):
    user = User.query.get(current_user_id)
    likes = request.form.get('likes')
    user.like = likes
    db.session.merge(user)
    db.session.commit()
    return redirect(url_for('get_status', current_user_id=current_user_id))