CREATE TABLE clinic.employees
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






CREATE TABLE clinic.patients
(
  id INT AUTO_INCREMENT,
  patient_no VARCHAR(50) NOT NULL UNIQUE,
  fname VARCHAR(50) NOT NULL,
  lname VARCHAR(50) NOT NULL,
  patient_name VARCHAR(101) GENERATED ALWAYS AS (concat(`lname`,_utf8mb4' ',`fname`)) STORED NOT NULL,
  sex VARCHAR(10) DEFAULT NULL,
  birth_date date NOT NULL,
  village VARCHAR(50) DEFAULT NULL,
  parish VARCHAR(50) DEFAULT NULL,
  patient_tel INT DEFAULT NULL,
  kin_name VARCHAR(101) NOT NULL,
  kin_tel INT NOT NULL,
  relation VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY(id, patient_no)
);



CREATE TABLE clinic.reports
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

ALTER TABLE clinic.reports ADD FOREIGN KEY (patient_no) REFERENCES clinic.patients (patient_no);
ALTER TABLE clinic.reports ADD FOREIGN KEY (emp_no) REFERENCES clinic.employees (emp_no);

-- CREATE TABLE clinic.medication
-- (
--   id INT AUTO_INCREMENT,
--   medicine_no VARCHAR(20) NOT NULL UNIQUE,
--   medicine_name VARCHAR(250) NOT NULL,
--   dosage VARCHAR(50) NOT NULL,
--   prescription VARCHAR(50) NOT NULL,
--   intervals INT NOT NULL,
--   time_period VARCHAR(50) NOT NULL,
--   quantity INT NOT NULL DEFAULT '1',
--   treatment_no VARCHAR(20) NOT NULL,
--   PRIMARY KEY (id, medicine_no)
-- );

-- CREATE TABLE clinic.tests
-- (
--   id INT AUTO_INCREMENT,
--   test_no VARCHAR(50) NOT NULL UNIQUE,
--   test_name VARCHAR(200) NOT NULL,
--   test_type VARCHAR(200) DEFAULT NULL,
--   testing_date datetime NOT NULL,
--   unit_price INT NOT NULL,
--   emp_no VARCHAR(50) NOT NULL,
--   PRIMARY KEY(id, test_no)
-- );


-- CREATE TABLE clinic.treatment
-- (
--   id INT AUTO_INCREMENT,
--   treatment_no VARCHAR(50) NOT NULL UNIQUE,
--   patient_no VARCHAR(50) NOT NULL,
--   emp_no VARCHAR(50) NOT NULL,
--   diagnosis VARCHAR(250) NOT NULL,
--   medication VARCHAR(3000) NOT NULL,
--   starting_date date NOT NULL,
--   comment VARCHAR(3000) DEFAULT NULL,
--   PRIMARY KEY(id, treatment_no)
-- );


