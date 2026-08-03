"""Site-wide church info context processor."""

from .models import ChurchInfo


def church_info(request):
    """Inject church information into all templates."""
    church = ChurchInfo.objects.first()
    return {'church': church}
