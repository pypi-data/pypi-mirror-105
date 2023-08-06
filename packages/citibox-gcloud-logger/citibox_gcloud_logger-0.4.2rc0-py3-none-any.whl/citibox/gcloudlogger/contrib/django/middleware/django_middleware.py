from citibox.gcloudlogger.contrib import Middleware
from citibox.gcloudlogger.contrib.django.django_base_record_factory import DjangoBaseRecordFactory


class DjangoMiddleware(Middleware):

    def __init__(self, get_response):
        super().__init__()
        self._get_response = get_response
        self._cached_request_body = None
        self._url_fingerprint = ""
        self.log = None

        self.response = None

    def __call__(self, request):
        self.response = self._get_response(request)
        return self.response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.log = DjangoBaseRecordFactory(
            logger=self.logger,
            response=self.response,
            request=request,
            view_kwargs=view_kwargs)\
            .build()

        try:
            self.logger.info(
                f'{request.method} {self.response.status_code} {request.path}',
                extra=self.log.to_dict()
            )
        except Exception:  # pragma: no cover
            pass

        # self.log.url_fingerprint = self._get_url_fingerprint(request.path, view_kwargs)
