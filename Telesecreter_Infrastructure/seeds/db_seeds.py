import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from datetime import date, time
from Telesecreter_Infrastructure.data_access.configurations.common.base_model import Base
from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel
from Telesecreter_Domain.enums.user_role import UserRole
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Infrastructure.data_access.db.database import get_db
import uuid


def seed():
    with get_db() as conn:
        try:
            # 1. Departments
            departments = [
                {"id": str(uuid.uuid4()), "name": "General Practice"},
                {"id": str(uuid.uuid4()), "name": "Cardiology"},
                {"id": str(uuid.uuid4()), "name": "Neurology"},
                {"id": str(uuid.uuid4()), "name": "Orthopedics"},
            ]
            conn.executemany(
                "INSERT INTO departments (id, name, created_at, updated_at) VALUES (:id, :name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                departments
            )
            print("✅ Departments added")

            # 2. Doctors
            doctors = [
                {"id": str(uuid.uuid4()), "full_name": "Dr. John Smith",   "email": "john.smith@hospital.com",   "phone_number": "+1234567890", "department_id": departments[0]["id"], "specialty": "General Medicine", "is_available": 1, "rating": 4.5},
                {"id": str(uuid.uuid4()), "full_name": "Dr. Sarah Connor",  "email": "sarah.connor@hospital.com",  "phone_number": "+1234567891", "department_id": departments[1]["id"], "specialty": "Cardiology",       "is_available": 1, "rating": 4.9},
                {"id": str(uuid.uuid4()), "full_name": "Dr. Emily Davis",   "email": "emily.davis@hospital.com",   "phone_number": "+1234567892", "department_id": departments[2]["id"], "specialty": "Neurology",        "is_available": 1, "rating": 3.8},
                {"id": str(uuid.uuid4()), "full_name": "Dr. James Wilson",  "email": "james.wilson@hospital.com",  "phone_number": "+1234567893", "department_id": departments[3]["id"], "specialty": "Orthopedics",      "is_available": 1, "rating": 4.2},
            ]
            conn.executemany(
                """INSERT INTO doctors (id, full_name, email, phone_number, department_id, specialty, is_available, rating, created_at, updated_at)
                   VALUES (:id, :full_name, :email, :phone_number, :department_id, :specialty, :is_available, :rating, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                doctors
            )
            print("✅ Doctors added")

            # 3. Schedules (Mon-Fri, 09:00-17:00 for each doctor)
            schedules = [
                {"id": str(uuid.uuid4()), "doctor_id": doctor["id"], "day_of_week": day, "start_time": "09:00:00", "end_time": "17:00:00"}
                for doctor in doctors
                for day in range(0, 5)
            ]
            conn.executemany(
                """INSERT INTO doctor_schedules (id, doctor_id, day_of_week, start_time, end_time, created_at, updated_at)
                   VALUES (:id, :doctor_id, :day_of_week, :start_time, :end_time, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                schedules
            )
            print("✅ Schedules added")

            # 4. Users
            users = [
                {"id": str(uuid.uuid4()), "full_name": "Alice Johnson", "email": "alice@example.com", "phone_number": "+9876543210", "hashed_password": "hashed_password_here", "role": UserRole.PATIENT.value, "is_active": 1},
                {"id": str(uuid.uuid4()), "full_name": "Bob Williams",  "email": "bob@example.com",   "phone_number": "+9876543211", "hashed_password": "hashed_password_here", "role": UserRole.PATIENT.value, "is_active": 1},
            ]
            conn.executemany(
                """INSERT INTO users (id, full_name, email, phone_number, hashed_password, role, is_active, created_at, updated_at)
                   VALUES (:id, :full_name, :email, :phone_number, :hashed_password, :role, :is_active, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                users
            )
            print("✅ Users added")

            # 5. Appointments
            appointments = [
                {"id": str(uuid.uuid4()), "user_id": users[0]["id"], "doctor_id": doctors[0]["id"], "date": "2026-04-10", "start_time": "09:00:00", "end_time": "09:30:00", "status": AppointmentStatus.CONFIRMED.value},
                {"id": str(uuid.uuid4()), "user_id": users[0]["id"], "doctor_id": doctors[1]["id"], "date": "2026-04-14", "start_time": "10:00:00", "end_time": "10:30:00", "status": AppointmentStatus.PENDING.value},
                {"id": str(uuid.uuid4()), "user_id": users[1]["id"], "doctor_id": doctors[2]["id"], "date": "2026-04-11", "start_time": "11:00:00", "end_time": "11:30:00", "status": AppointmentStatus.PENDING.value},
                {"id": str(uuid.uuid4()), "user_id": users[1]["id"], "doctor_id": doctors[3]["id"], "date": "2026-04-15", "start_time": "14:00:00", "end_time": "14:30:00", "status": AppointmentStatus.CONFIRMED.value},
            ]
            conn.executemany(
                """INSERT INTO appointments (id, user_id, doctor_id, date, start_time, end_time, status, created_at, updated_at)
                   VALUES (:id, :user_id, :doctor_id, :date, :start_time, :end_time, :status, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                appointments
            )
            print("✅ Appointments added")

            print("🎉 All seed data inserted successfully")

        except Exception as e:
            print(f"❌ Error: {e}")
            raise


if __name__ == "__main__":
    seed()