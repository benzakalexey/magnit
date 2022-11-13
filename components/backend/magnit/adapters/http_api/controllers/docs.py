from classic.components import component
import falcon

from magnit.adapters.http_api import constants
from magnit.adapters.http_api.join_points import join_point
from magnit.application import services


@component
class Docs:
    service: services.Doc

    @join_point
    def on_get_weighing_act(self, request, response):
        filename = self.service.get_weighing_act(**request.params)
        response.downloadable_as = filename
        response.content_type = 'application/xlsx'
        response.stream = open(filename, 'rb')

    @join_point
    def on_get_transport_invoice(self, request, response):
        self.service.get_transport_invoice(**request.params)
        response.media = constants.SUCCESS_TRUE

    @join_point
    def on_get_xlsx_to_pdf(self, request, response):
        self.service.get_xlsx_to_pdf(**request.params)
        response.media = constants.SUCCESS_TRUE

    # def on_get(self, request, response):
    #     filename = "./evaluation.pdf"
    #     resp.downloadable_as = filename
    #     resp.content_type = 'application/pdf'
    #
    #     resp.stream = open(filename, 'rb')
    #     resp.status = falcon.HTTP_200



# class ThingsResource:
#     def on_get(self, request, response):
#         """Handles GET requests"""
#         response.status = falcon.HTTP_200  # This is the default status
#         response.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
#         response.text = (
#             '\nTwo things awe me most, the starry sky '
#             'above me and the moral law within me.\n'
#             '\n'
#             '    ~ Immanuel Kant\n\n'
#         )
#
#
# app = falcon.App()