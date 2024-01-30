from flask import render_template, request, redirect, url_for, jsonify, abort
from testapp.entity.db import db
from testapp.entity.employee import Employee
from testapp.entity.pairs import Pairing
from testapp.entity.users import User
from testapp.entity.has_sent import HasSent
from testapp import app
import random


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
    mail = request.form.get('mail')
    current_user = User.query.filter_by(name=name).first()
    if not current_user.mail:
        current_user.mail = mail
        db.session.commit()    
    elif current_user.mail != mail:
        return render_template('testapp/login.html', error='メールアドレスが一致しません')
    return redirect(url_for('get_status', current_user_id=current_user.id))

@app.get('/top')
def get_status():
    user_id = request.json.get('user_id')
    if user_id is not None:
        # Userテーブルからuser_idが一致するレコードを取得
        user = User.query.filter_by(id=user_id).first()
        
        # HasSentテーブルからuser_idが一致するレコードを取得
        has_sent = HasSent.query.filter_by(user_id=user_id).first()
        
        if user:
            # userデータとhas_sentデータをレスポンスとして返す
            response_data = {
                'user_id': user.id,
                'name': user.name,
                'has_pair': user.has_pair,
                'has_sent': has_sent is not None  # has_sentレコードが存在するかどうか
            }
            return render_template('testapp/top.html', response_data=response_data)
        

@app.get('/lottery')
def get_lottery_page():
    current_user_id = request.form.get('user_id')  # フォームデータからログインユーザーのIDを取得
    current_user = User.query.get(current_user_id)
    
    if current_user.has_pair:
        return redirect(url_for('get_lottery_result', current_user_id=current_user_id))
    return render_template('testapp/lottery.html', current_user_id=current_user_id)


@app.post('/lottery')
def post_lottery_result():
    current_user_id = request.form.get('user_id')  # フォームデータからログインユーザーのIDを取得
    current_user = User.query.get(current_user_id)
    
    # ログインユーザーの性別に基づいて異性を探す
    target_gender = 'F' if current_user.gender == 'M' else 'M'
    available_partners = User.query.filter_by(gender=target_gender, has_pair=False).all()
    
    # ランダムに異性を選ぶ
    partner = random.choice(available_partners)
    
    # ペアをデータベースに保存
    new_pairing = Pairing(giver_id=current_user.id, receiver_id=partner.id)
    db.session.add(new_pairing)
    
    # 選ばれた参加者の has_pair を更新
    current_user.has_pair = True
    partner.has_pair = True
    db.session.commit()

    # ペアをリザルトページに渡す
    return redirect(url_for('get_lottery_result', current_user_id=current_user.id))

@app.get('/result')
def get_lottery_result():
    current_user_id = request.args.get('current_user_id')  # URLのクエリパラメータからcurrent_user_idを取得
    # Pairingテーブルからcurrent_user_idをgiver_idとして持つレコードを検索
    pairing = Pairing.query.get(Pairing.giver_id == current_user_id)
    
    if not pairing:
        # ペアリングが見つからない場合
        return render_template('error.html', message='Pairing not found')

    # current_user_idがgiverならreceiverを取得、receiverならgiverを取得
    pair_user = User.query.get(pairing.receiver_id)
    
    if not pair_user:
        # 対応するペアのユーザーが見つからない場合
        return render_template('error.html', message='Pair user not found')
    
    # 対応するペアのユーザーのnameとlikeを返却
    return render_template('result.html', name=pair_user.name, like=pair_user.like)
