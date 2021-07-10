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
