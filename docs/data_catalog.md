# Data Catalog – Healthcare DW

## Dimension Tables

### dim_patient
| Column       | Type         | Description                        |
| ------------ | ------------ | ---------------------------------- |
| patient\_key | INT (PK)     | Surrogate key (identity)           |
| patient\_id  | BIGINT       | Business key from source           |
| gender       | CHAR(1)      | M/F                                |
| age          | INT          | Patient’s age                      |
| age\_group   | VARCHAR(20)  | Derived: Child, Adult, Senior      |
| neighborhood | VARCHAR(100) | Patient neighborhood               |
| scholarship  | BIT          | 1 = has scholarship, 0 = none      |
| hypertension | BIT          | 1 = yes, 0 = no                    |
| diabetes     | BIT          | 1 = yes, 0 = no                    |
| alcoholism   | BIT          | 1 = yes, 0 = no                    |
| handicap     | INT          | Handicap level                     |
| start\_date  | DATETIME     | SCD2 start validity                |
| end\_date    | DATETIME     | SCD2 end validity (NULL = current) |
| is\_current  | TINYINT      | SCD2 flag (1 = active)             |

### dim_doctor
| Column         | Type         | Description           |
| -------------- | ------------ | --------------------- |
| doctor\_key    | INT (PK)     | Surrogate key         |
| doctor\_id     | INT          | Business key from API |
| name           | VARCHAR(100) | Doctor name           |
| specialization | VARCHAR(50)  | Doctor specialization |


### dim_date
| Column          | Type        | Description              |
| --------------- | ----------- | ------------------------ |
| date\_key       | INT (PK)    | Surrogate key (YYYYMMDD) |
| full\_date      | DATE        | Calendar date            |
| calendar\_year  | INT         | Year (e.g., 2016)        |
| calendar\_month | INT         | Month number (1–12)      |
| calendar\_day   | INT         | Day of month (1–31)      |
| day\_of\_week   | VARCHAR(20) | Monday–Sunday            |


### dim_hospital
| Column         | Type         | Description             |
| -------------- | ------------ | ----------------------- |
| hospital\_key  | INT (PK)     | Surrogate key           |
| hospital\_name | VARCHAR(100) | Hospital or clinic name |

## Fact Table

### fact_appointments
| Column                      | Type        | Description                             |
| --------------------------- | ----------- | --------------------------------------- |
| appointment\_id             | BIGINT (PK) | Natural appointment identifier          |
| patient\_key                | INT (FK)    | Link → dim\_patient                     |
| doctor\_key                 | INT (FK)    | Link → dim\_doctor                      |
| appointment\_date\_key      | INT (FK)    | Link → dim\_date (appointment date)     |
| scheduled\_date\_key        | INT (FK)    | Link → dim\_date (scheduled date)       |
| hospital\_key               | INT (FK)    | Link → dim\_hospital                    |
| appointment\_time           | TIME        | Appointment time                        |
| schedule\_time              | TIME        | Scheduling time                         |
| appointment\_duration\_days | INT         | Days between scheduling and appointment |
| late\_scheduling\_flag      | BIT         | 1 = scheduled <1 day before             |
| sms\_received\_flag         | BIT         | 1 = SMS reminder sent                   |
| no\_show\_flag              | BIT         | 1 = patient did not show                |
| attended\_flag              | BIT         | 1 = patient attended                    |

## Aggregate Table

### Monthly_NoShow_Rates
| Column                 | Type     | Description                    |
| ---------------------- | -------- | ------------------------------ |
| monthly\_no\_show\_key | INT (PK) | Surrogate key                  |
| month\_year\_date      | DATE     | First day of the month         |
| date\_key              | INT (FK) | Reference to dim\_date         |
| total\_appointments    | INT      | Total appointments that month  |
| no\_show\_rate         | FLOAT    | No-show percentage (0–1 float) |
