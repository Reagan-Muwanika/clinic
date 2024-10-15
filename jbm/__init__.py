from flask import Flask



def create_app(test_config = None):
	app = Flask(__name__, instance_relative_config = True)
	app.config.from_mapping(SECRET_KEY = 'reagan')

	if test_config is None:
		app.config.from_pyfile('config.py', silent = True)
	else:
		app.config.from_mapping(test_config)

	from . import authentications
	app.register_blueprint(authentications.bp)
	
	from . import patient
	app.register_blueprint(patient.bp)

	from . import reports
	app.register_blueprint(reports.bp)

	from . import config
	config.initialize_app(app)


	return app