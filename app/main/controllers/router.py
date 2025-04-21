from fastapi import APIRouter
from .migration_controller import router as migration
from .authentification_controller import router as authentication
from .user_controller import router as user
from .storage_controller import router as storage
from .academic_year_controller import router as academic_year
from .semester_controller import router as semester
from .programs_controller import router as program
from .speciality_controller import router as department
from .group_controller import router as classes
from .students_controller import router as students
from .subjects_controller import router as subjects
from .examns_type_controller import router as type_exam
from .teacher_controller import router as teacher
from .courses_controller import router as courses
from .teacher_course_assignment_controller import router as assignment
from .teachers_authentification_controller import router as teachers_authentification
api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(teachers_authentification)
api_router.include_router(teacher)
api_router.include_router(courses)
api_router.include_router(assignment)
api_router.include_router(authentication)
api_router.include_router(user)
api_router.include_router(storage)
api_router.include_router(academic_year)
api_router.include_router(type_exam)
api_router.include_router(semester)
api_router.include_router(program)
api_router.include_router(department)
api_router.include_router(classes)
api_router.include_router(subjects)
api_router.include_router(students)
