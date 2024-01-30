from flask import render_template, request, redirect, url_for
from testapp.models.db import db
from testapp.models.employee import Employee
from testapp.models.participants import Pairing, Participant
from testapp import app
import random
from json import jsonify



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


@app.get('/lottery')
def get_lottery():
    return render_template('testapp/lottery.html')

@app.post('/lottery')
def post_result():
    current_user_id = request.form.get('user_id')  # フォームデータからログインユーザーのIDを取得
    current_user = Participant.query.get(current_user_id)
    
    # ログインユーザーが存在しない、またはすでにペアがいる場合、indexページにリダイレクト
    if not current_user or current_user.has_pair:
        return redirect(url_for('index'))
    
    # ログインユーザーの性別に基づいて異性を探す
    target_gender = 'F' if current_user.gender == 'M' else 'M'
    available_partners = Participant.query.filter_by(gender=target_gender, has_pair=False).all()
    
    # 異性がいない場合、エラーを返す
    if not available_partners:
        return jsonify({'error': 'No available partners'}), 400
    
    # ランダムに異性を選ぶ
    partner = random.choice(available_partners)
    
    # ペアをデータベースに保存
    new_pairing = Pairing(giver_id=current_user.id, taker_id=partner.id)
    db.session.add(new_pairing)
    
    # 選ばれた参加者の has_pair を更新
    current_user.has_pair = True
    partner.has_pair = True
    db.session.commit()

    # ペアをリザルトページに渡す
    return redirect(url_for('result', partner_name=partner.name))

@app.route('/result')
def result():
    current_user_id = request.form.get('user_id')  # フォームデータからログインユーザーのIDを取得
    current_user = Participant.query.get(current_user_id)
    
    if not current_user.has_pair:
        return redirect(url_for('lottery'))
        
    # セッションからペア情報を取得
    pair_info = session.pop('pair_info', None)
    if pair_info:
        return render_template('result.html', male=pair_info['male'], female=pair_info['female'])
    else:
        return redirect(url_for('index'))  # ペア情報がない場合、indexにリダイレクト
