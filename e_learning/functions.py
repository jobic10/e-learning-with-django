from administrator.models import Settings


def get_session():
    session = None
    try:
        settings = Settings.objects.all()[0]
        session = settings.current_academic_session
    except Exception as e:
        pass
    return session
