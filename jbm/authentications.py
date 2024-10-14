from flask import (Blueprint, flash, redirect, g, render_template, request, session, url_for)
from jbm.config import connect_to_database
from werkzeug.security import (check_password_hash, generate_password_hash)
from functools import wraps
from jbm.comfunc import (mr, gr, rs, years, days, months, depart, date_func, dob_func)

bp = Blueprint('authentications', __name__, url_prefix = '/staff')

starting_date = date_func()

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    '''
        Enabling the user to log into the system
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        query = '''
            SELECT
                id,
                password, 
                department
            FROM
                clinic.employees  
            WHERE
                username = %s 
        '''
        try:
            cursor = connect_to_database().cursor()
            cursor.execute(query, [username])
            user = cursor.fetchall()
        except Exception as e:
            raise e
        
        if not user:
            error = 'Incorrect username'
        elif not check_password_hash(user[0][1], password):
            error = 'Incorrect password'
            
        if error is None:
            session.clear()
            session['user_id'] = user[0][0]
            if user[0][2] == 'Doctor' or user[0][2] == 'Laboratory' or user[0][2] == 'Nurse' or user[0][2] == 'Dispenser' or user[0][2] == 'demo' or user[0][2] == 'dev' or user[0][2] == 'admin':
                # redirect the user to the doctors home page
                return redirect(url_for('patient.search_for_patient_details'))
        # displaying the errors that occured
        flash(error)
    # redirect user to login page
    return render_template('authentications/login.html')

@bp.before_app_request
def logged_in_user_info():
    '''
        Extracting details of the logged in user
    '''
    user_id = session.get('user_id')
    

    if user_id is None:
        g.user = None
    else:
        try:
            query = '''
                SELECT
                    id,
                    fname,
                    department,
                    username,
                    password,
                    emp_no
                FROM
                    clinic.employees
                WHERE
                    id = %s
            '''
            cursor = connect_to_database().cursor()
            cursor.execute(query, [user_id])
            g.user = cursor.fetchone()
        except Exception as e:
            raise e

def employee_number():
    '''
        Generating the employee number for the employee table
    '''
    query = '''
        SELECT
            id
        FROM
            clinic.employees
    '''
    try:
        cursor = connect_to_database().cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        raise e

    emp_id = len(result) + 1
    emp_no = f'EMP\\{starting_date[1]}\\{emp_id}'
    return emp_no

def login_required(view):
    '''
        Checking if user is logged in and if not asked to log in
    '''
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # redirecting user back to login page incase they are not logged in
            return redirect(url_for('authentications.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
@login_required
def logout():
    '''
        Allowing the user to log out of the system
    '''
    session.clear()
    return redirect(url_for('authentications.login'))

@bp.route('/register_staff', methods = ('GET', 'POST'))
@login_required
def register():
    '''
        Registering new staff members of the clinic
    '''
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['sex']
        tel = request.form['tel']
        password = request.form['password']
        confirm = request.form['confirm']
        username = request.form['username']
        department = request.form['depart']
        parish = request.form['parish']
        village = request.form['village']
        yrs = request.form['year']
        mth = request.form['month']
        mth = dob_func(mth)
        day = request.form['day']
        birth_date = f'{yrs}-{mth}-{day}'
        emp_no = employee_number()
        
        error = None
        
        if not fname:
            error = 'Firstname is required'
        elif not lname:
            error = 'Lastname is required'
        elif not password:
            error = 'Password is required'
        elif len(password) < 8:
            error = 'Password should contain atleast 8 character including letters, numbers and symbols'
        elif not confirm:
            error = 'Re-enter password to comfirm'
        elif password != confirm:
            error = 'Passwords do not match'
        elif not username:
            error = 'Username is required'
        elif username.isnumeric():
            error = 'Username shouldnot be numeric'
        elif not department or  department == 'Department':
            error = 'Choose a valid department'
        elif yrs == 'Year' or mth == 'Month' or day == 'Day':
            error = 'Choose a valid date of birth of birth'
        elif gender == 'Gender':
            error = 'Choose a valid gender'

        if error is None:
            query = '''
                SELECT
                    username
                FROM
                    clinic.employees
                WHERE
                    username = %s
            '''
            try:
                cursor = connect_to_database().cursor()
                cursor.execute(query, [username])
                result = cursor.fetchall()
            except Exception as e:
                raise e

            if not result:
                inserting = '''
                    INSERT INTO clinic.employees
                        (fname, lname, sex, emp_tel, password, username, department, birth_date, emp_no, village, parish)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                try: 
                    cursor = connect_to_database().cursor()
                    cursor.execute(inserting, [fname, lname, gender, tel, generate_password_hash(password), username, department, birth_date, emp_no, village, parish])
                    connect_to_database().commit()
                    return redirect(url_for('authentications.login'))
                except Exception as e:
                    raise e
                                    
        flash(error)
    return render_template('authentications/register.html', mr = mr, gr = gr, years = years, rs = rs, days = days, months = months, depart = depart)

@bp.route('/change_password', methods = ('GET', 'POST'))
@login_required
def change_user_password():
    '''
        Changing user's password
    '''
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm = request.form['confirm']
        error = None
        
        if not old_password:
            error = f'Old password is required'
        elif not new_password:
            error = f'New password is required'
        elif not confirm:
            error = f'Re-enter new password to confirm'
        elif new_password != confirm:
            error = f'New password and confirmed password do not match'
        elif len(new_password) < 8:
            error = f'Passwords should contain atleast eight(8) characters. Including capital letters, symbols'
        elif not check_password_hash(g.user[4], old_password):
            error = f'Incorrect old password'

        if error is None:
            query = '''
                UPDATE
                    clinic.employees
                SET 
                    password = %s 
                WHERE
                    username = %s
            '''
            try:
                cursor = connect_to_database().cursor()
                cursor.execute(query, [generate_password_hash(new_password), g.user[2]])
                connect_to_database().commit()
                return redirect(url_for('authentications.login'))
            except Exception as e:
                raise e
        flash(error)
    return render_template('authentications/password.html')