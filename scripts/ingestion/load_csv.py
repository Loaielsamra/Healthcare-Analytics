import pandas as pd
import requests
import random

appointments = pd.read_csv("data/raw/noshowappointments.csv")

resp = requests.get("https://randomuser.me/api/?results=50&nat=us")
doctors_raw = resp.json()["results"]

specializations = ["Cardiology", "Dermatology", "Neurology", "General", "Pediatrics"]
doctors = pd.DataFrame(
    [
        {
            "doctor_id": i + 1,
            "name": f"{d['name']['first']} {d['name']['last']}",
            "specialization": random.choice(specializations),
            "hospital": d["location"]["city"],
        }
        for i, d in enumerate(doctors_raw)
    ]
)

appointments["doctor_id"] = appointments.index.map(
    lambda x: random.choice(doctors["doctor_id"].tolist())
)

appointments["ScheduledDay"] = pd.to_datetime(appointments["ScheduledDay"])
appointments["AppointmentDay"] = pd.to_datetime(appointments["AppointmentDay"])
appointments = appointments[appointments["Age"] >= 0]

patients = appointments[
    [
        "PatientId",
        "Gender",
        "Age",
        "Neighbourhood",
        "Scholarship",
        "Hipertension",
        "Diabetes",
        "Alcoholism",
        "Handcap",
    ]
].drop_duplicates(subset=["PatientId"], keep="last")

patients.columns = patients.columns.str.lower()
appointments.columns = appointments.columns.str.lower()

patients = patients.rename(
    columns={
        "patientid": "patient_id",
        "hipertension": "hypertension",
        "handcap": "handicap",
        "neighbourhood": "neighborhood",
    }
)

appointments = appointments.rename(
    columns={
        "patientid": "patient_id",
        "appointmentid": "appointment_id",
        "scheduledday": "scheduled_day",
        "appointmentday": "appointment_day",
        "no-show": "no_show",
    }
)


def age_group(age):
    if age < 18:
        return "Child"
    elif age < 60:
        return "Adult"
    else:
        return "Senior"


patients = patients[patients["age"] >= 0]
patients["age_group"] = patients["age"].apply(age_group)

appointments["appointment_dayofweek"] = appointments["appointment_day"].dt.day_name()
appointments["appointment_duration_days"] = (
    appointments["appointment_day"] - appointments["scheduled_day"]
).dt.days
appointments = appointments[appointments["appointment_duration_days"] >= 0]

appointments["late_scheduling"] = appointments["appointment_duration_days"].apply(
    lambda x: 1 if x < 1 else 0
)

appointments["no_show"] = appointments["no_show"].map({"Yes": 1, "No": 0})
appointments["attended"] = appointments["no_show"].apply(lambda x: 0 if x == 1 else 1)

appointments["appointment_day"] = (
    pd.to_datetime(appointments["appointment_day"])
    .dt.tz_localize(None)
    .dt.strftime("%Y-%m-%d %H:%M:%S")
)

appointments["scheduled_day"] = (
    pd.to_datetime(appointments["scheduled_day"])
    .dt.tz_localize(None)
    .dt.strftime("%Y-%m-%d %H:%M:%S")
)

patients = patients[
    [
        "patient_id",
        "gender",
        "age",
        "age_group",
        "neighborhood",
        "scholarship",
        "hypertension",
        "diabetes",
        "alcoholism",
        "handicap",
    ]
]

doctors = doctors[["doctor_id", "name", "specialization", "hospital"]]

appointments = appointments[
    [
        "appointment_id",
        "patient_id",
        "doctor_id",
        "scheduled_day",
        "appointment_day",
        "appointment_duration_days",
        "appointment_dayofweek",
        "late_scheduling",
        "sms_received",
        "no_show",
        "attended",
    ]
]

patients.to_csv("data/clean/patients.csv", index=False)
appointments.to_csv("data/clean/appointments.csv", index=False)
doctors.to_csv("data/clean/doctors.csv", index=False)
