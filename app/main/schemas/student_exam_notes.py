from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import List, Optional
from app.main.schemas.academic_year import AcademicYearSlim1
from app.main.schemas.courses import CoursesSlim1, CoursesSlim3
from app.main.schemas.group import GroupSlim
from app.main.schemas.programs import ProgramsSlim2
from app.main.schemas.semester import SemesterSlim1
from app.main.schemas.speciality import SpecialitySlim
from app.main.schemas.students import StudentSlim, StudentSlimData
from app.main.schemas.teacher import TeacherSlim, TeacherSlim1
from app.main.schemas.user import AddedBy

class StudentSlim(BaseModel):
    uuid:str
    matricule:str
    first_name: str
    last_name: str
    birthdate: date
    address:str
    program:Optional[ProgramsSlim2]=None
    speciality : Optional[SpecialitySlim]=None
    group:Optional[GroupSlim]=None
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
    
class StudentNoteInput(BaseModel):
    student_uuid: str
    note_cc: Optional[float] = None
    note_sn: Optional[float] = None

class StudentExamNoteCreateBulk(BaseModel):
    course_uuid: str
    semester_uuid: str
    notes: List[StudentNoteInput]

class StudentExamNoteOut(BaseModel):
    uuid: str
    student: StudentSlim
    course: CoursesSlim1
    semester: SemesterSlim1
    note_cc: Optional[float]
    note_sn: Optional[float]
    final_note: Optional[float]
    status: str
    model_config = ConfigDict(from_attributes=True)  

class StudentExamNoteOutSlim1(BaseModel):
    course: CoursesSlim3
    note_cc: Optional[float]
    note_sn: Optional[float]
    final_note: Optional[float]
    model_config = ConfigDict(from_attributes=True)

class StudentExamNoteData(BaseModel):
    uuid: str
    course: CoursesSlim1
    semester: SemesterSlim1
    student:StudentSlim
    user:AddedBy
    note_cc: Optional[float]
    note_sn: Optional[float]
    final_note: Optional[float]
    status: str
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)  


class PaginatedStudentExamNResponse(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[StudentExamNoteData]

class StudentReportResponse(BaseModel):
    student:StudentSlimData
    notes: List[StudentExamNoteOutSlim1]
    moyenne_generale: float
    mention: str
    model_config = ConfigDict(from_attributes=True)
class StudentReportPaginationResponse(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[StudentReportResponse]
    model_config = ConfigDict(from_attributes=True)