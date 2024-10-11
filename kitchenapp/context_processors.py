from .models import Resident


def residents_processor(request):
    residents = Resident.objects.all()
    return {'residents': residents}
