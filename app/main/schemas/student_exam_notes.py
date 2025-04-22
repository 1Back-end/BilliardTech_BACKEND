from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import List, Optional
from app.main.schemas.academic_year import AcademicYearSlim1
from app.main.schemas.courses import CoursesSlim1
from app.main.schemas.semester import SemesterSlim1
from app.main.schemas.students import StudentSlim
from app.main.schemas.teacher import TeacherSlim, TeacherSlim1
from app.main.schemas.user import AddedBy

class StudentNoteInput(BaseModel):
    student_uuid: str
    note_cc: Optional[float] = None
    note_sn: Optional[float] = None

class StudentExamNoteCreateBulk(BaseModel):
    course_uuid: str
    semester_uuid: str
    academic_year_uuid: str
    notes: List[StudentNoteInput]

class StudentExamNoteOut(BaseModel):
    uuid: str
    student: StudentSlim
    course: CoursesSlim1
    semester: SemesterSlim1
    academic_year: AcademicYearSlim1
    note_cc: Optional[float]
    note_sn: Optional[float]
    final_note: Optional[float]
    status: str
    model_config = ConfigDict(from_attributes=True)  


class StudentExamNoteData(BaseModel):
    uuid: str
    course: CoursesSlim1
    semester: SemesterSlim1
    academic_year: AcademicYearSlim1
    teacher:TeacherSlim1
    note_cc: Optional[float]
    note_sn: Optional[float]
    final_note: Optional[float]
    status: str
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)  