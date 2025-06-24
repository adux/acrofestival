from django.conf import settings


def google_maps(request):
    """Make Google Maps API key available in templates."""
    return {
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
    }