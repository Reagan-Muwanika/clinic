from flask import (Blueprint, render_template, g, redirect, session, url_for, flash, request)
from jbm.authentications import login_required
from jbm.config import connect_to_database
from jbm.comfunc import date_func, age_func


bp = Blueprint('reports', __name__, url_prefix = '/reports')


def report_number():
    '''
        Generating the employee number for the employee table
    '''
    query = '''
        SELECT
            id
        FROM
            clinic.reports
    '''
    try:
        cursor = connect_to_database().cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        raise e

    starting_date = date_func()
    report_id = len(result) + 1
    report_no = f'REP\\{starting_date[1]}\\{report_id}'
    return report_no




@bp.route('/medical_reports', methods = ('GET', 'POST'))
@login_required
def medical_reports(patient_name = None):
	'''
		Function retrieves the reports from the database
	'''
	if request.method == 'POST':
		patient_name = request.form['patient_name']

		if patient_name:
			query = '''
				SELECT 
					rep.id,
					rep.report_date,
					rep.report_no,
					pat.patient_name,
					pat.sex,
					emp.fname
				FROM
					clinic.reports rep
				INNER JOIN
					clinic.patients pat
				ON
					rep.patient_no = pat.patient_no
				INNER JOIN
					clinic.employees emp
				ON
					emp.emp_no = rep.emp_no
				WHERE
					pat.fname = %s
				OR
					pat.lname = %s
				OR
					pat.patient_name = %s
			'''
			try:
				cursor = connect_to_database().cursor()
				cursor.execute(query, [patient_name, patient_name, patient_name])
				results = cursor.fetchall()
				return render_template('reports/report.html', results = results)
			except Exception as e:
				raise e
		
	if patient_name is None:
		query = '''
			SELECT 
				rep.id,
				rep.report_date,
				rep.report_no,
				pat.patient_name,
				pat.sex,
				emp.fname
			FROM
				clinic.reports rep
			INNER JOIN
				clinic.patients pat
			ON
				rep.patient_no = pat.patient_no
			INNER JOIN
				clinic.employees emp
			ON
				emp.emp_no = rep.emp_no
		'''
		try:
			cursor = connect_to_database().cursor()
			cursor.execute(query)
			results = cursor.fetchall()
			return render_template('reports/report.html', results = results)
		except Exception as e:
			raise e
	return render_template('reports/report.html')




@bp.route('/<report_id>/view_report', methods = ['GET'])
@login_required
def view_patient_report(report_id):
	'''
		Function to enable the user to see the patient's medical report
	'''
	query = '''
		SELECT 
			rep.report_date,
			rep.report_no,
			rep.tests_suggest,
			rep.complaints,
			rep.temperature,
			rep.pressure,
			rep.diagnosis,
			rep.new_treat,
			pat.patient_name,
			pat.sex,
			pat.patient_tel,
			pat.birth_date,
			emp.fname
		FROM
			clinic.reports rep
		INNER JOIN
			clinic.patients pat
		ON
			rep.patient_no = pat.patient_no
		INNER JOIN
			clinic.employees emp
		ON
			emp.emp_no = rep.emp_no
		WHERE
			rep.id = %s
	'''
	try:
		cursor = connect_to_database().cursor()
		cursor.execute(query, [report_id])
		report = cursor.fetchone()
		# age = str(report[11])
		age = age_func(report[11])
		return render_template('reports/view.html', report = report, age = age)
	except Exception as e:
		raise e
	return render_template('reports/view.html')



@bp.route('/generate_report', methods = ('GET', 'POST'))
@login_required
def generate_report(patient_name = None):
	'''
		Function to generate a medical report for the patient
	'''
	if request.method == 'POST':
		patient_no = request.form['pat_no']
		weight = float(request.form['weight'])
		temp = float(request.form['temperature'])
		pressure = float(request.form['blood-pressure'])
		complaints = request.form['complaints']
		sugg_tests = request.form['sugg_tests']
		on_treat = request.form['ongoing_treat']
		diagnosis = request.form['diagnosis']
		new_treat = request.form['new_treat']
		date = date_func()
		date = date[0]
		report_type = g.user
		report_type = report_type[2]
		report_no = report_number()
		emp_no = g.user[5]


		error = None

		if not patient_no:
			error = 'Patient number is required'
		elif not weight:
			weight = 'N/A'
		elif not temp:
			temp = 'N/A'
		elif not pressure:
			pressure = 'N/A'
		elif not complaints:
			error = 'Patient complaints required'
		elif not sugg_tests:
			sugg_tests = 'N/A'
		elif not on_treat:
			on_treat = 'N/A'
		elif not diagnosis:
			error = 'Diagnosis is required'
		elif not new_treat:
			error = "Patient's treatment is required"

		if error is None:
			query = '''
				SELECT 
					id,
					fname
				FROM
					clinic.patients 
				WHERE
					patient_no = %s
			'''
			try:
				cursor = connect_to_database().cursor()
				cursor.execute(query, [patient_no])
				result = cursor.fetchall()
			except Exception as e:
				raise e

			if result:
				inserting = '''
					INSERT INTO clinic.reports
						(patient_no, weight, temperature, pressure, complaints, tests_suggest, curr_treat, diagnosis, new_treat, report_date, report_type, report_no, emp_no)
					VALUES
						(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

				'''
				try:
					cursor = connect_to_database().cursor()
					cursor.execute(inserting, [patient_no, weight, temp, pressure, complaints, sugg_tests, on_treat, diagnosis, new_treat, date, report_type, report_no, emp_no])
					connect_to_database().commit()
					error = 'Report generated successfully'
				except Exception as e:
					raise e
	return render_template('reports/generate.html', )