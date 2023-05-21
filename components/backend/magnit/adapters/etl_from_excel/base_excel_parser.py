import logging
from io import BytesIO
from typing import Optional

from classic.components import component
from falcon import media
from openpyxl import Workbook, load_workbook


@component
class ExcelParser:
    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def _get_workbook(self, file: media.multipart.BodyPart) -> Workbook:
        self.logger.info('Parsing %s', file.filename)
        file_data = self._read_file_data(file)
        return load_workbook(file_data)

    def _read_file_data(  # noqa
        self,
        file: media.multipart.BodyPart,
    ) -> Optional[BytesIO]:
        file_data = BytesIO()
        while True:
            chunk = file.stream.read(8192)
            if not chunk:
                break
            file_data.write(chunk)

        return file_data
