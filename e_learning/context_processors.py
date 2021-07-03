from administrator.models import Settings


def SESSION(request):
    session = None
    try:
        settings = Settings.objects.all()[0]
        session = settings.current_academic_session
    except Exception as e:
        pass
    context = {'ACADEMIC_SESSION': session}
    return context
