from falcon import Request, Response

from citibox.gcloudlogger.contrib import Middleware
from citibox.gcloudlogger.contrib.falcon.falcon_base_record_factory import FalconBaseRecordFactory


class FalconMiddleware(Middleware):

    def __init__(self):
        super().__init__()
        self.params = None

    def process_resource(self, request: Request, response: Response, resource, params: dict):
        self.params = params

    def process_response(self, request: Request, response: Response, resource, req_succeeded: bool):
        """
        :param req: falcon.Request
        :param resp: falcon.Response
        :param resource: Resource object
        :param req_succeeded: bool
        :return:
        """
        log = FalconBaseRecordFactory(request=request, response=response, params=self.params).build()

        try:
            self.logger.info(
                log.message,
                extra=log.to_dict()
            )
        except Exception as e:  # pragma nocover
            pass
