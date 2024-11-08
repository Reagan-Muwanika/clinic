CREATE TABLE IF NOT EXISTS clinic.patients
(
  id INT AUTO_INCREMENT,
  patient_no VARCHAR(50) NOT NULL UNIQUE,
  fname VARCHAR(50) NOT NULL,
  lname VARCHAR(50) NOT NULL,
  patient_name VARCHAR(65) GENERATED ALWAYS AS (CONCAT(lname, ' ', fname)) STORED,
  sex VARCHAR(10) NULL DEFAULT NULL,
  birth_date date NOT NULL,
  village VARCHAR(50) NULL DEFAULT NULL,
  parish VARCHAR(50) NULL DEFAULT NULL,
  patient_tel INT NULL DEFAULT 0,
  kin_name VARCHAR(101) NOT NULL DEFAULT NULL,
  kin_tel INT NOT NULL DEFAULT 0,
  relation VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY(id, patient_no)
);

CREATE TABLE IF NOT EXISTS clinic.reports
(
  id INT AUTO_INCREMENT,
  report_date datetime NOT NULL,
  report_type VARCHAR(50) NOT NULL,
  report_no VARCHAR(50) NOT NULL UNIQUE,
  emp_no VARCHAR(50) NOT NULL,
  patient_no VARCHAR(50) NOT NULL,
  tests_suggest VARCHAR(2500) DEFAULT NULL,
  complaints VARCHAR(2500) NOT NULL,
  weight VARCHAR(5) DEFAULT NULL,
  temperature INT DEFAULT NULL,
  pressure INT DEFAULT NULL,
  curr_treat VARCHAR(2500) DEFAULT NULL,
  new_treat VARCHAR(2500) DEFAULT NULL,
  diagnosis VARCHAR(2500) DEFAULT NULL,
  PRIMARY KEY(id, report_no)
);

CREATE TABLE IF NOT EXISTS clinic.employees
(
  id INT AUTO_INCREMENT,
  emp_no VARCHAR(50) NOT NULL UNIQUE,
  fname VARCHAR(50) NOT NULL,
  lname VARCHAR(50) NOT NULL,
  sex VARCHAR(10) DEFAULT NULL,
  birth_date date NOT NULL,
  village VARCHAR(50) DEFAULT NULL,
  parish VARCHAR(50) DEFAULT NULL,
  emp_tel INT NOT NULL,
  department VARCHAR(50) NOT NULL,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(5000) NOT NULL, 
  PRIMARY KEY (id, emp_no)
);


ALTER TABLE clinic.reports ADD FOREIGN KEY (patient_no) REFERENCES clinic.patients (patient_no);
ALTER TABLE clinic.reports ADD FOREIGN KEY (emp_no) REFERENCES clinic.employees (emp_no);

