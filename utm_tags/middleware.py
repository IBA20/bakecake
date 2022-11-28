from utm_tags.models import UTMVisit


class UTMMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        utm_keys = [
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'utm_term',
            'utm_content',
        ]
        utm_parameters = {
            str(key).lower(): str(value).lower()
            for key, value in request.GET.items()
            if key in utm_keys and value != ''
        }
        if 'utm_source' in utm_parameters.keys():
            UTMVisit.objects.create(
                source=utm_parameters.get('utm_source', ''),
                medium=utm_parameters.get('utm_medium', ''),
                campaign=utm_parameters.get('utm_campaign', ''),
                term=utm_parameters.get('utm_term', ''),
                content=utm_parameters.get('utm_content', ''),
            )

        response = self.get_response(request)
        return response
