from django.conf import settings


def site_globals(request):
    return {
        "SITE_NAME": "Velora Motors",
        "SITE_TAGLINE": "Drive Your Dream. Anywhere.",
        "SUPPORT_PHONE": settings.VELORA_SUPPORT_PHONE,
        "SUPPORT_HOURS": settings.VELORA_SUPPORT_HOURS,
        "SUPPORT_EMAIL": settings.VELORA_SUPPORT_EMAIL,
    }
