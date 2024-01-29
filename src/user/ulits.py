from .models import Profile
from django.db.models import Q


def searchProfile(request):
    search_query = ""

    if request.GET.get("text"):
        search_query = request.GET.get("text")

    projects = (
        Profile.objects.all()
        .filter(
            Q(username__icontains=search_query)
            | Q(bio__icontains=search_query)
            | Q(locations__icontains=search_query)
        )
        .distinct()
    )

    return projects
