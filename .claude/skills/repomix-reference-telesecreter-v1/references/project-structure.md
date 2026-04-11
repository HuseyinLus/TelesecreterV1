# Directory Structure

```
Telesecreter_API/
  dependencies/
    dependency_injection.py (31 lines)
  routers/
    appointment_controller.py (12 lines)
    department_controller.py (12 lines)
    doctor_controller.py (12 lines)
    scheduale_controller.py (12 lines)
    user_controller.py (13 lines)
  main.py (30 lines)
Telesecreter_Application/
  appointment/
    dtos/
      appointment_dto.py (31 lines)
    queries/
      get_all_appointmens_query.py (11 lines)
    __init__.py (0 lines)
  department/
    dtos/
      department_dto.py (19 lines)
    queries/
      get_all_departments_query.py (12 lines)
    __init__.py (0 lines)
  doctor/
    dtos/
      doctor_dto.py (27 lines)
    queries/
      get_all_doctors_query.py (11 lines)
    __init__.py (0 lines)
  scheduale/
    dtos/
      scheduale_dto.py (25 lines)
    queries/
      get_all_scheduales_query.py (11 lines)
    __init__.py (0 lines)
  user/
    dtos/
      user_dto.py (28 lines)
    queries/
      get_all_users_query.py (12 lines)
    __init__.py (0 lines)
  __init__.py (0 lines)
Telesecreter_Domain/
  common/
    base_entity.py (20 lines)
  entities/
    appointments.py (30 lines)
    department.py (12 lines)
    doctor.py (27 lines)
    scheduale.py (19 lines)
    user.py (22 lines)
  enums/
    appointment_status.py (9 lines)
    user_role.py (6 lines)
  interfaces/
    __init__.py (0 lines)
    i_appointment_repository.py (25 lines)
    i_base_repository.py (28 lines)
    i_department_repository.py (11 lines)
    i_doctor_repository.py (20 lines)
    i_scheduale_repository.py (15 lines)
    i_user_repository.py (20 lines)
  __init__.py (0 lines)
Telesecreter_Infrastructure/
  data_access/
    configurations/
      common/
        __init__.py (0 lines)
        base_model.py (23 lines)
      models/
        __init__.py (0 lines)
        appintment.py (26 lines)
        department_model.py (19 lines)
        doctor_model.py (19 lines)
        schedual_model.py (18 lines)
        user_model.py (17 lines)
      __init__.py (0 lines)
    db/
      database.py (80 lines)
    migrations/
      versions/
        3eaebeceed60_add_department_id_to_doctors.py (29 lines)
        c2a7cdd538a3_initial_tables.py (113 lines)
      env.py (58 lines)
      README (1 lines)
      script.py.mako (28 lines)
    repositories/
      appointment_repository.py (52 lines)
      department_repository.py (24 lines)
      doctor_repository.py (41 lines)
      repository.py (63 lines)
      scheduale_repository.py (35 lines)
      user_repository.py (41 lines)
    __init__.py (0 lines)
  seeds/
    db_seeds.py (96 lines)
  __init__.py (0 lines)
.gitignore (49 lines)
alembic.ini (37 lines)
CLAUDE.md (70 lines)
context.txt (1939 lines)
requirements.txt (20 lines)
todo.txt (38 lines)
```