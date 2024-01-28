from testapp import app
from flask import render_template, request, redirect, url_for
from random import randint
from testapp import db
from testapp.models.employee import Employee


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
