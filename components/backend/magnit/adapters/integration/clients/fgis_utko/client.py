import json
import logging
import uuid

import requests as requests
from classic.components import component


@component
class FgisUtkoClient:
    url: str

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_data(self, data: dict):
        self.logger.info('Sending data started')
        boundary = str(uuid.uuid4())
        headers = {
            'accept': '*/*',
            'Content-Type': 'multipart/form-data; boundary=' + boundary
        }

        data = json.dumps(data, ensure_ascii=False)
        payload = (
            f'--{boundary}\r\nContent-Disposition: form-data; '
            f'name="file"; filename="report.json"\r\n'
            f'Content-Type: application/json\r\n\r\n'
            f'{data}\r\n'
            f'--{boundary}--')
        response = requests.post(
            self.url,
            headers=headers,
            data=payload,
        )
        if response.status_code == 200:
            self.logger.info('Sending data successfully')
            return True, response.status_code
        else:
            self.logger.error('Error sending data. code: %s, msg: %s' % (
                response.status_code, response.content,
            ))
            return False, response.status_code
