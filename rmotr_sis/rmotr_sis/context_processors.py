from django.conf import settings


def mixpanel_settings(request):
    return {
        'MIXPANEL_TOKEN': settings.MIXPANEL_TOKEN,
        'MIXPANEL_TRACKING_ENABLED': settings.MIXPANEL_TRACKING_ENABLED
    }
