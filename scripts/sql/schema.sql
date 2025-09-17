CREATE TABLE patients (
    patient_id BIGINT PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    age_group VARCHAR(10),             
    neighborhood VARCHAR(100),
    scholarship BOOLEAN,
    hypertension BOOLEAN,
    diabetes BOOLEAN,
    alcoholism BOOLEAN,
    handicap BOOLEAN,

    CHECK (age >= 0)                     
);

CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(50),
    hospital VARCHAR(100)
);

CREATE TABLE appointments (
    appointment_id BIGINT PRIMARY KEY,
    patient_id BIGINT NOT NULL,
    doctor_id INT NOT NULL,
    scheduled_day TIMESTAMP NOT NULL,
    appointment_day TIMESTAMP NOT NULL,
    appointment_duration_days INT,
    appointment_dayofweek VARCHAR(15),
    late_scheduling BOOLEAN,
    sms_received BOOLEAN,
    no_show BOOLEAN,
    attended BOOLEAN,
    
    -- Foreign Keys
    CONSTRAINT fk_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    CONSTRAINT fk_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    
    -- Logical Checks
    CHECK (appointment_day >= scheduled_day), -- appointment day must be on or after scheduled day
    CHECK (appointment_duration_days >= 0) -- no negative durations
);

--- Indexes for performance optimization
CREATE INDEX idx_patient_id ON appointments(patient_id);
CREATE INDEX idx_doctor_id ON appointments(doctor_id);
CREATE INDEX idx_attended ON appointments(attended);
CREATE INDEX idx_appointment_day ON appointments(appointment_day);