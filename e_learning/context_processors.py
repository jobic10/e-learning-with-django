from .functions import get_session
from django.conf import settings


def SESSION(request):
    session = get_session()
    context = {'ACADEMIC_SESSION': session, 'APP_NAME': settings.APP_NAME}
    return context
