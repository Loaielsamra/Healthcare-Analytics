CREATE TABLE patients (
    patient_id BIGINT PRIMARY KEY,
    gender CHAR(1),
    age INT,
    age_group VARCHAR(20),
    neighborhood VARCHAR(100),
    scholarship BIT,
    hypertension BIT,
    diabetes BIT,
    alcoholism BIT,
    handicap INT
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(50),
    city VARCHAR(100)
);

CREATE TABLE appointments (
    appointment_id BIGINT PRIMARY KEY,
    patient_id BIGINT,
    doctor_id INT,
    scheduled_day DATETIME,
    appointment_day DATETIME,
    appointment_duration_days INT,
    appointment_dayofweek VARCHAR(20),
    late_scheduling BIT,
    sms_received BIT,
    no_show BIT,
    attended BIT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

--- Indexes for performance optimization
CREATE INDEX idx_patient_id ON appointments(patient_id);
CREATE INDEX idx_doctor_id ON appointments(doctor_id);
CREATE INDEX idx_attended ON appointments(attended);
CREATE INDEX idx_appointment_day ON appointments(appointment_day);