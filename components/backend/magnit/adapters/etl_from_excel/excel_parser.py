from typing import Any, Dict, List

from classic.components import component
from falcon import media
from openpyxl.worksheet.worksheet import Worksheet

from magnit.application import dto
from magnit.application import interfaces
from .base_excel_parser import ExcelParser


@component
class TonarsExcelParser(ExcelParser, interfaces.ExcelParser):
    def get_data(
        self,
        file: media.multipart.BodyPart,
    ) -> List[dto.TonarXls]:
        wb = self._get_workbook(file)
        data = self._get_data_from_worksheets(wb.worksheets)
        return [
            dto.TonarXls(
                weight_out=int(row.get('Брутто')),
                invoice_num=row.get('Номер ТН'),
                driver=row.get('Водитель'),
                destination=row.get('Направление'),
            ) for row in data
        ]

    def _get_data_from_worksheets(
        self,
        worksheets: List[Worksheet],
    ) -> List[Dict[str, Any]]:
        worksheets_data = []
        for ws in worksheets:
            worksheets_data.extend(self._get_data_from_worksheet(ws))

        return worksheets_data

    def _get_data_from_worksheet(
        self,
        ws: Worksheet,
    ) -> List[Dict[Any, Any]]:
        column_names = [
            'Пропуск',
            'Контрагент',
            'Рег.номер',
            'Марка ТС',
            'Полигон',
            'Время выезда',
            'Брутто',
            'Тара',
            'Нетто',
            'Номер ТН',
            'Направление',
            'Водитель'
        ]

        data = []
        for row in ws.values:
            row_data = dict(zip(column_names, row))
            data.append(row_data)

        return data[1:]
