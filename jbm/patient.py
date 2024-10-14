from flask import (Blueprint, render_template, jsonify, g, redirect, session, url_for, flash, request)
from jbm.comfunc import (mr, gr, rs, years, days, months, date_func, dob_func)
from jbm.authentications import login_required
from jbm.config import connect_to_database
from werkzeug.exceptions import abort

bp = Blueprint('patient', __name__, url_prefix = '/staff')

starting_date = date_func()

def patient_number():
    '''
        Generating the employee number for the employee table
    '''
    query = '''
        SELECT
            id
        FROM
            clinic.patients
    '''
    try:
        cursor = connect_to_database().cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        raise e

    patient_id = len(result) + 1
    patient_no = f'PAT\\{starting_date[1]}\\{patient_id}'
    return patient_no

@bp.route('/patient_register', methods = ('POST', 'GET'))
@login_required
def register():
	if request.method == 'POST':
		fname = request.form['fname']
		lname = request.form['lname']
		gender = request.form['sex']
		patient_no = patient_number()
		yrs = request.form['year']
		mth = request.form['month']
		day = request.form['day']
		birth_date = f'{yrs}-{mth}-{day}'
		patient_tel = request.form['pat_tel']
		village = request.form['village']
		parish = request.form['parish']
		kin_name = request.form['kin_name']
		kin_tel = request.form['kin_tel']
		relationship = request.form['relationship']
		error = None

		if not fname:
			error = 'Firstname is required'
		elif not lname:
			error = 'Lastname is required'
		elif not gender:
			error = 'Gender is required'
		elif gender == 'Gender':
			error = 'Choose a valid gender'
		elif not yrs:
			error = 'Year of birth is required'
		elif yrs == 'Year':
			error = 'Choose a valid year of birth'
		elif not mth:
			error = 'Month of birth is required'
		elif mth == 'Month':
			error = 'Choose a valid month of birth'
		elif not day:
			error = 'Day of birth is required'
		elif day == 'Day':
			error = 'Choose a valid day of birth'
		elif not kin_name:
			error = 'Next of kin is required'
		elif not kin_tel:
			error = 'Phone number of next of kin is required'
		elif not kin_tel.isnumeric():
			error = 'Next of kin tel should be numeric'
		elif len(kin_tel) < 9 or len(kin_tel) > 10:
			error = 'Next of kin tel should have atleast 9 and atmost 10 characters'
		elif not patient_tel:
			error = 'Phone number is required'
		elif not patient_tel.isnumeric():
			error = 'Patient phone number should be numeric'
		elif len(patient_tel) < 9 or len(patient_tel) > 10:
			error = 'Patient phone number should have atleast 9 and atmost 10 characters'
		elif yrs == 'Year' or mth == 'Month' or day == 'Day':
			error = 'Choose a valid date of birth of birth'
		elif gender == 'Gender':
			error = 'Choose a valid gender'
		elif relationship == 'Relationship':
			error = 'Choose a valid relationship'

		if error is None:
			# Checking if patient already exists in the system
			mth = dob_func(mth)
			print(f'\n{mth}\n')
			query = '''
				SELECT
					fname,
					lname,
					birth_date,
					patient_tel
				FROM
					clinic.patients
				WHERE
					fname = %s
				AND
					lname = %s
				AND
					birth_date = %s
				AND
					patient_tel = %s 
			'''
			try:
				cursor = connect_to_database().cursor()
				cursor.execute(query, [fname, lname, birth_date, patient_tel])
				result = cursor.fetchall()
			except Exception as e:
				raise e
				

			if not result:
				inserting = '''
					INSERT INTO clinic.patients
						(fname, lname, sex, birth_date, patient_tel, parish, village, kin_name, kin_tel, relation, patient_no)
					VALUES
						(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
				'''
				try:
					cursor = connect_to_database().cursor()
					cursor.execute(inserting, [fname, lname, gender, birth_date, patient_tel, parish, village, kin_name, kin_tel, relationship, patient_no])
					connect_to_database().commit()
					error = f'Patient successfully registered'
				except Exception as e:
					raise e
				
		flash(error)
	return render_template('patient/register.html', mr = mr, gr = gr, years = years, rs = rs, days = days, months = months)

@bp.route('/patient_data', methods = ('GET', 'POST'))
@login_required
def search_for_patient_details(patient_name = None):
	'''
		Function check for the details of patients or a specific patient
	'''
	if request.method == 'POST':
		patient_name = request.form['patient_name']

		if patient_name:
			query = '''
				SELECT
					id,
					patient_no,
					patient_name,
					patient_tel,
					sex,
					birth_date
				FROM
					clinic.patients
				WHERE
					fname = %s
				OR 
					lname = %s
				OR
					patient_name = %s
			'''
			try:
				cursor = connect_to_database().cursor()
				cursor.execute(query, [patient_name, patient_name, patient_name])
				patients = cursor.fetchall()
				return render_template('patient/patient.html', patients = patients)
			except Exception as e:
				raise e
				
	if patient_name is None:
			query = '''
				SELECT
					id,
					patient_no,
					patient_name,
					patient_tel,
					sex,
					birth_date
				FROM
					clinic.patients
			'''
			try:
				cursor = connect_to_database().cursor()
				cursor.execute(query)
				patients = cursor.fetchall()
				return render_template('patient/patient.html', patients = patients, mr = mr, gr = gr, years = years, rs = rs, days = days, months = months)
			except Exception as e:
				raise e		
	return render_template('patient/patient.html')



@bp.route('/<int:patient_id>/update', methods = ('GET', 'POST'))
@login_required
def update_patient_details(patient_id):
	'''
		Funtion to enable the user update the patient's details
	'''
	if request.method == 'POST':
		fname = request.form['fname']
		lname = request.form['lname']
		patient_tel = request.form['pat_tel']
		village = request.form['village']
		parish = request.form['parish']
		kin_name = request.form['kin_name']
		kin_tel = request.form['kin_tel']
		relationship = request.form['relationship']
		error = None

		if not fname:
			error = 'Firstname is required'
		elif not lname:
			error = 'Lastname is required'
		elif not kin_name:
			error = 'Next of kin is required'
		elif not kin_tel:
			error = 'Phone number of next of kin is required'
		elif not kin_tel.isnumeric():
			error = 'Next of kin tel should be numeric'
		elif len(kin_tel) < 9 or len(kin_tel) > 10:
			error = 'Next of kin tel should have atleast 9 and atmost 10 characters'
		elif not village:
			error = 'Village is required'
		elif not parish:
			error = 'Parish is required'
		elif not relationship:
			error = 'Relationship with the next of kin is required'
		elif relationship == 'Relationship':
			relationship = 'N/A'
		elif not patient_tel:
			error = "Patient's phone number is required"

		my_updates = [fname, lname, kin_name, kin_tel, village, parish, patient_tel, relationship, patient_id]
		

		query = '''
			UPDATE 
				clinic.patients
			SET
				fname = %s, lname = %s, kin_name = %s, kin_tel = %s, village = %s, parish = %s, patient_tel = %s, relation = %s
			WHERE
				id = %s
		'''
		try:
			cursor = connect_to_database().cursor()
			cursor = cursor.execute(query, my_updates)
			connect_to_database().commit()
			error = 'Patient data updated successfully'
			return redirect(url_for('patient.search_for_patient_details'))
		except Exception as e:
			raise e

	if patient_id:
		query = '''
			SELECT 
				fname,
				lname,
				sex, 
				birth_date,
				village,
				parish,
				patient_tel,
				kin_name,
				kin_tel
			FROM
				clinic.patients
			WHERE
				id = %s
		'''
		try:
			cursor = connect_to_database().cursor()
			cursor.execute(query, [patient_id])
			patient = cursor.fetchone()
			return render_template('patient/update.html', patient = patient, rs = rs)
		except Exception as e:
			raise e



@bp.route('/tests', methods = ('GET', 'POST'))
@login_required
def test_details(test_name = None):
	return render_template('patient/test.html')