from administrator.models import Settings
from .functions import get_session


def SESSION(request):
    session = get_session()
    context = {'ACADEMIC_SESSION': session}
    return context
