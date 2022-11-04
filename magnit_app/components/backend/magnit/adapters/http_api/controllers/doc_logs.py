from classic.components import component

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class DocLogs:
    service: services.DocLog

    @join_point
    def on_get_get_by_id(self, request, response):
        doc_log = self.service.get_by_id(**request.params)
        response.media = doc_log

    @join_point
    def on_get_get_all(self, request, response):
        docs_log = self.service.get_all(**request.params)
        response.media = docs_log

    @join_point
    def on_post_add(self, request, response):
        self.service.add_doc_log(**request.media)
        response.media = constants.SUCCESS_TRUE
