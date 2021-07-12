import cryptocode
from django.conf import settings


def get_session():
    from administrator.models import Settings
    session = None
    try:
        settings = Settings.objects.all()[0]
        session = settings.current_academic_session
    except Exception as e:
        pass
    return session


def encrypt(string):
    return cryptocode.encrypt(str(string), settings.SECRET_KEY)


def decrypt(string):
    return cryptocode.decrypt(string, settings.SECRET_KEY)


def validate(token):
    token = str(token).replace('?', '/')
    course_id = decrypt(token)
    course_id = int(course_id)
    return course_id


def validate_access(token, request, user_type='student'):
    is_error = False
    value = None
    try:
        course_id = validate(token)
        if course_id == False or course_id < 1 or not course_id:
            is_error = True
        else:
            session = get_session()
            if user_type == 'student':
                student = request.user.student
                from student.models import CourseRegistration
                value = CourseRegistration.objects.get(
                    student=student, course_id=course_id, session=session, approved=True)
                is_error = False
            elif user_type == 'staff':
                from staff.models import CourseAllocation
                staff = request.user.staff
                value = CourseAllocation.objects.get(
                    staff=staff, course_id=course_id, session=session, approved=True)
                is_error = False
            else:
                return False
    except:
        is_error = True
    if is_error:
        raise Exception("Access Denied")
    else:
        return value
