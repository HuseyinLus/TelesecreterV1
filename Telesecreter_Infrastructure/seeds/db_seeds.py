import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from Telesecreter_Infrastructure.data_access.configurations.models.department_model import DepartmentModel
from Telesecreter_Infrastructure.data_access.configurations.models.doctor_model import DoctorModel
from Telesecreter_Infrastructure.data_access.configurations.models.user_model import UserModel
from Telesecreter_Infrastructure.data_access.configurations.models.schedual_model import DoctorScheduleModel
from Telesecreter_Infrastructure.data_access.configurations.models.appintment import AppointmentModel
from Telesecreter_Domain.enums.user_role import UserRole
from Telesecreter_Domain.enums.appointment_status import AppointmentStatus
from Telesecreter_Infrastructure.data_access.db.database import get_db
import uuid
import random
from datetime import datetime, time, date, timezone, timedelta

now = datetime.now(timezone.utc)


def seed():
    with get_db() as session:
        # 1. Departments
        dept_ids = [str(uuid.uuid4()) for _ in range(4)]
        departments = [
            DepartmentModel(id=dept_ids[0], name="General Practice", created_at=now, updated_at=now),
            DepartmentModel(id=dept_ids[1], name="Cardiology",       created_at=now, updated_at=now),
            DepartmentModel(id=dept_ids[2], name="Neurology",        created_at=now, updated_at=now),
            DepartmentModel(id=dept_ids[3], name="Orthopedics",      created_at=now, updated_at=now),
        ]
        session.add_all(departments)
        session.flush()
        print("✅ Departments added")

        # 2. Doctors (4 original + 20 new = 24 total)
        doctor_data = [
            ("Dr. John Smith",       "john.smith@hospital.com",       "+1234567890", 0, "General Medicine", 4.5),
            ("Dr. Sarah Connor",     "sarah.connor@hospital.com",     "+1234567891", 1, "Cardiology",       4.9),
            ("Dr. Emily Davis",      "emily.davis@hospital.com",      "+1234567892", 2, "Neurology",        3.8),
            ("Dr. James Wilson",     "james.wilson@hospital.com",     "+1234567893", 3, "Orthopedics",      4.2),
            ("Dr. Michael Torres",   "m.torres@hospital.com",         "+1234567894", 0, "General Medicine", 4.1),
            ("Dr. Laura Bennett",    "l.bennett@hospital.com",        "+1234567895", 1, "Cardiology",       4.7),
            ("Dr. David Park",       "d.park@hospital.com",           "+1234567896", 2, "Neurology",        4.3),
            ("Dr. Anna Müller",      "a.muller@hospital.com",         "+1234567897", 3, "Orthopedics",      3.9),
            ("Dr. Carlos Rivera",    "c.rivera@hospital.com",         "+1234567898", 1, "Cardiology",       4.6),
            ("Dr. Nina Patel",       "n.patel@hospital.com",          "+1234567899", 0, "General Medicine", 4.8),
            ("Dr. Thomas Hughes",    "t.hughes@hospital.com",         "+1234567900", 2, "Neurology",        4.0),
            ("Dr. Yuki Tanaka",      "y.tanaka@hospital.com",         "+1234567901", 3, "Orthopedics",      4.4),
            ("Dr. Sofia Rossi",      "s.rossi@hospital.com",          "+1234567902", 0, "General Medicine", 3.7),
            ("Dr. Omar Hassan",      "o.hassan@hospital.com",         "+1234567903", 1, "Cardiology",       4.5),
            ("Dr. Elena Popescu",    "e.popescu@hospital.com",        "+1234567904", 2, "Neurology",        4.2),
            ("Dr. Lucas Martin",     "l.martin@hospital.com",         "+1234567905", 3, "Orthopedics",      4.6),
            ("Dr. Fatima Al-Rashid", "f.alrashid@hospital.com",       "+1234567906", 0, "General Medicine", 4.9),
            ("Dr. Ivan Petrov",      "i.petrov@hospital.com",         "+1234567907", 1, "Cardiology",       3.6),
            ("Dr. Mei Lin",          "m.lin@hospital.com",            "+1234567908", 2, "Neurology",        4.7),
            ("Dr. Samuel Okafor",    "s.okafor@hospital.com",         "+1234567909", 3, "Orthopedics",      4.1),
            ("Dr. Isabelle Dupont",  "i.dupont@hospital.com",         "+1234567910", 0, "General Medicine", 4.3),
            ("Dr. Arjun Sharma",     "a.sharma@hospital.com",         "+1234567911", 1, "Cardiology",       4.8),
            ("Dr. Klara Novak",      "k.novak@hospital.com",          "+1234567912", 2, "Neurology",        3.5),
            ("Dr. Marcus Webb",      "m.webb@hospital.com",           "+1234567913", 3, "Orthopedics",      4.4),
        ]
        doctor_ids = [str(uuid.uuid4()) for _ in doctor_data]
        doctors = [
            DoctorModel(
                id=doctor_ids[i], full_name=name, email=email, phone_number=phone,
                department_id=dept_ids[dept_idx], specialty=specialty,
                is_available=True, rating=rating, created_at=now, updated_at=now,
            )
            for i, (name, email, phone, dept_idx, specialty, rating) in enumerate(doctor_data)
        ]
        session.add_all(doctors)
        session.flush()
        print("✅ Doctors added")

        # 3. Schedules (Mon-Fri, 09:00-17:00 for each doctor)
        schedules = [
            DoctorScheduleModel(
                id=str(uuid.uuid4()), doctor_id=did, day_of_week=day,
                start_time=time(9, 0), end_time=time(17, 0), created_at=now, updated_at=now,
            )
            for did in doctor_ids
            for day in range(0, 5)
        ]
        session.add_all(schedules)
        session.flush()
        print("✅ Schedules added")

        # 4. Users (2 original + 20 new = 22 total)
        user_data = [
            ("Alice Johnson",    "alice@example.com",    "+9876543210"),
            ("Bob Williams",     "bob@example.com",      "+9876543211"),
            ("Clara Nguyen",     "c.nguyen@example.com", "+9876543212"),
            ("Daniel Ferreira",  "d.ferreira@example.com","+9876543213"),
            ("Emma Svensson",    "e.svensson@example.com","+9876543214"),
            ("Frank Müller",     "f.muller@example.com", "+9876543215"),
            ("Grace Kim",        "g.kim@example.com",    "+9876543216"),
            ("Henry Owusu",      "h.owusu@example.com",  "+9876543217"),
            ("Irina Volkov",     "i.volkov@example.com", "+9876543218"),
            ("Jack Huang",       "j.huang@example.com",  "+9876543219"),
            ("Karin Larsson",    "k.larsson@example.com","+9876543220"),
            ("Liam O'Brien",     "l.obrien@example.com", "+9876543221"),
            ("Maya Patel",       "m.patel@example.com",  "+9876543222"),
            ("Niko Mäkinen",     "n.makinen@example.com","+9876543223"),
            ("Olivia Santos",    "o.santos@example.com", "+9876543224"),
            ("Pedro Alves",      "p.alves@example.com",  "+9876543225"),
            ("Quinn Baker",      "q.baker@example.com",  "+9876543226"),
            ("Rosa Esposito",    "r.esposito@example.com","+9876543227"),
            ("Stefan Kozłowski", "s.kozlowski@example.com","+9876543228"),
            ("Tina Yamamoto",    "t.yamamoto@example.com","+9876543229"),
            ("Umar Diallo",      "u.diallo@example.com", "+9876543230"),
            ("Vera Christodoulou","v.christo@example.com","+9876543231"),
        ]
        user_ids = [str(uuid.uuid4()) for _ in user_data]
        users = [
            UserModel(
                id=user_ids[i], full_name=name, email=email, phone_number=phone,
                hashed_password="hashed_password_here", role=UserRole.PATIENT,
                is_active=True, created_at=now, updated_at=now,
            )
            for i, (name, email, phone) in enumerate(user_data)
        ]
        session.add_all(users)
        session.flush()
        print("✅ Users added")

        # 5. Appointments — spread across April & May 2026, varied times
        slots = [
            (time(9, 0),  time(9, 30)),
            (time(10, 0), time(10, 30)),
            (time(11, 0), time(11, 30)),
            (time(12, 0), time(12, 30)),
            (time(13, 0), time(13, 30)),
            (time(14, 0), time(14, 30)),
            (time(15, 0), time(15, 30)),
            (time(16, 0), time(16, 30)),
        ]
        statuses = [
            AppointmentStatus.CONFIRMED,
            AppointmentStatus.CONFIRMED,
            AppointmentStatus.CONFIRMED,
            AppointmentStatus.PENDING,
            AppointmentStatus.PENDING,
            AppointmentStatus.CANCELLED,
        ]
        base_date = date(2026, 4, 7)
        seen_slots = set()
        appointments = []
        random.seed(42)

        for i in range(24):
            user_id   = user_ids[i % len(user_ids)]
            doctor_id = doctor_ids[i % len(doctor_ids)]
            appt_date = base_date + timedelta(days=(i * 2) % 50)
            start, end = slots[i % len(slots)]
            status     = statuses[i % len(statuses)]

            key = (doctor_id, appt_date, start)
            if key in seen_slots:
                start, end = slots[(i + 1) % len(slots)]
                key = (doctor_id, appt_date, start)
            seen_slots.add(key)

            appointments.append(AppointmentModel(
                id=str(uuid.uuid4()), user_id=user_id, doctor_id=doctor_id,
                date=appt_date, start_time=start, end_time=end,
                status=status, created_at=now, updated_at=now,
            ))

        session.add_all(appointments)
        print("✅ Appointments added")

        print("🎉 All seed data inserted successfully")


if __name__ == "__main__":
    seed()
