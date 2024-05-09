from django.conf import settings


def get_version_number(request):
    # return the version value as a dictionary
    # you may add other values here as well
    return {'APP_VERSION_NUMBER': settings.APP_VERSION_NUMBER}