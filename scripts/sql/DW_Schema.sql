USE healthcare_dw;

IF EXISTS (SELECT * FROM sys.foreign_keys WHERE NAME = 'fk_fact_appointments_dim_patient' AND parent_object_id = OBJECT_ID('fact_appointments'))
    ALTER TABLE fact_appointments DROP CONSTRAINT fk_fact_appointments_dim_patient;


IF EXISTS (SELECT * FROM sys.objects WHERE NAME = 'dim_patient' AND type = 'U')
    DROP TABLE dim_patient;

CREATE TABLE dim_patient (
    patient_key INT NOT NULL IDENTITY(1, 1),
    patient_id BIGINT NOT NULL,
    gender CHAR(1),
    age INT,
    age_group VARCHAR(20),
    neighborhood VARCHAR(100),
    scholarship BIT,
    hypertension BIT,
    diabetes BIT,
    alcoholism BIT,
    handicap INT,
    
    start_date DATETIME NOT NULL DEFAULT (GETDATE()),
    end_date DATETIME,
    is_current TINYINT NOT NULL DEFAULT (1),
    CONSTRAINT pk_dim_patient PRIMARY KEY CLUSTERED (patient_key)
);

CREATE INDEX dim_patient_patient_id ON dim_patient (patient_id);



IF EXISTS (SELECT * FROM sys.foreign_keys WHERE NAME = 'fk_fact_appointments_dim_doctor' AND parent_object_id = OBJECT_ID('fact_appointments'))
    ALTER TABLE fact_appointments DROP CONSTRAINT fk_fact_appointments_dim_doctor;


IF EXISTS (SELECT * FROM sys.objects WHERE NAME = 'dim_doctor' AND type = 'U')
    DROP TABLE dim_doctor;

CREATE TABLE dim_doctor (
    doctor_key INT NOT NULL IDENTITY(1, 1),
    doctor_id INT NOT NULL,
    name VARCHAR(100),
    specialization VARCHAR(50),
    CONSTRAINT pk_dim_doctor PRIMARY KEY CLUSTERED (doctor_key)
);
CREATE INDEX dim_doctor_doctor_id ON dim_doctor (doctor_id);



IF EXISTS (SELECT * FROM sys.foreign_keys WHERE NAME = 'fk_fact_appointments_dim_date' AND parent_object_id = OBJECT_ID('fact_appointments'))
    ALTER TABLE fact_appointments DROP CONSTRAINT fk_fact_appointments_dim_date;


IF EXISTS (SELECT * FROM sys.objects WHERE NAME = 'dim_date' AND type = 'U')
    DROP TABLE dim_date;

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    calendar_year INT,
    calendar_month INT,
    calendar_day INT,
    day_of_week VARCHAR(20)
);



IF EXISTS (SELECT * FROM sys.foreign_keys WHERE NAME = 'fk_fact_appointments_dim_hospital' AND parent_object_id = OBJECT_ID('fact_appointments'))
    ALTER TABLE fact_appointments DROP CONSTRAINT fk_fact_appointments_dim_hospital;


IF EXISTS (SELECT * FROM sys.objects WHERE NAME = 'dim_hospital' AND type = 'U')
    DROP TABLE dim_hospital;

CREATE TABLE dim_hospital (
    hospital_key INT NOT NULL IDENTITY(1, 1),
    hospital_name VARCHAR(100),
    CONSTRAINT pk_dim_hospital PRIMARY KEY CLUSTERED (hospital_key)
);

CREATE INDEX dim_hospital_name ON dim_hospital (hospital_name);


IF EXISTS (SELECT * FROM sys.objects WHERE NAME = 'fact_appointments' AND type = 'U')
    DROP TABLE fact_appointments;


CREATE TABLE fact_appointments (
    appointment_id BIGINT PRIMARY KEY,
    patient_key INT,
    doctor_key INT,
    appointment_date_key INT,
    scheduled_date_key INT,
    hospital_key INT,
    appointment_time TIME,
    schedule_time TIME,
    appointment_duration_days INT,
    late_scheduling_flag BIT,
    sms_received_flag BIT,
    no_show_flag BIT,
    attended_flag BIT
);


ALTER TABLE fact_appointments ADD CONSTRAINT fk_fact_appointments_dim_patient FOREIGN KEY (patient_key) REFERENCES dim_patient(patient_key);
ALTER TABLE fact_appointments ADD CONSTRAINT fk_fact_appointments_dim_doctor FOREIGN KEY (doctor_key) REFERENCES dim_doctor(doctor_key);
ALTER TABLE fact_appointments ADD CONSTRAINT fk_fact_appointments_dim_date FOREIGN KEY (appointment_date_key) REFERENCES dim_date(date_key);
ALTER TABLE fact_appointments ADD CONSTRAINT fk_fact_appointments_dim_hospital FOREIGN KEY (hospital_key) REFERENCES dim_hospital(hospital_key);


CREATE INDEX fact_appointments_appointment_id ON fact_appointments (AppointmentID);

CREATE INDEX fact_appointments_date_key ON fact_appointments (appointment_date_key);
CREATE INDEX fact_appointments_hospital_key ON fact_appointments (hospital_key);


IF EXISTS (SELECT * FROM sys.objects WHERE NAME = 'Monthly_NoShow_Rates' AND type = 'U')
    DROP TABLE Monthly_NoShow_Rates;

CREATE TABLE Monthly_NoShow_Rates (
    monthly_no_show_key INT IDENTITY(1,1) PRIMARY KEY,
    month_year_date DATE,
    date_key INT NOT NULL,
    total_appointments INT NOT NULL,
    no_show_rate FLOAT NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);