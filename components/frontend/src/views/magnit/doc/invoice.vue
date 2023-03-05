<script setup>
// import '@/assets/sass/invoice.css';
import '@/assets/sass/apps/invoice-preview.scss';
import { onMounted, ref } from 'vue';

//pdf export
import jsPDF from 'jspdf';
import 'jspdf-autotable';

import { useMeta } from '@/composables/use-meta';
useMeta({ title: 'Export Table' });

const columns = ref(['profile', 'name', 'position', 'office', 'age', 'start_date', 'salary', 'action']);
const items = ref([]);
const table_option = ref({
    perPage: 10,
    perPageValues: [5, 10, 20, 50],
    skin: 'table table-hover',
    columnsClasses: { action: 'actions text-center' },
    pagination: { nav: 'scroll', chunk: 5 },
    texts: {
        count: 'Showing {from} to {to} of {count}',
        filter: '',
        filterPlaceholder: 'Search...',
        limit: 'Results:',
    },
    sortable: ['name', 'position', 'office', 'age', 'start_date', 'salary'],
    sortIcon: {
        base: 'sort-icon-none',
        up: 'sort-icon-asc',
        down: 'sort-icon-desc',
    },
    resizableColumns: false,
});

onMounted(() => {
    bind_data();
});

const bind_data = () => {
    items.value = [
        { id: 1, thumb: 'boy-1.png', name: 'Tiger Nixon', position: 'System Architect', office: 'Edinburgh', age: 61, start_date: '2011/04/25', salary: '320,800' },
        { id: 2, thumb: 'boy-1.png', name: 'Garrett Winters', position: 'Accountant', office: 'Tokyo', age: 63, start_date: '2011/07/25', salary: '170,750' },
        { id: 3, thumb: 'boy.png', name: 'Ashton Cox', position: 'Junior Technical Author', office: 'San Francisco', age: 66, start_date: '2009/01/12', salary: '86,000' },
        { id: 4, thumb: 'boy-1.png', name: 'Cedric Kelly', position: 'Senior Javascript Developer', office: 'Edinburgh', age: 22, start_date: '2012/03/29', salary: '433,060' },
        { id: 5, thumb: 'girl-1.png', name: 'Airi Satou', position: 'Accountant', office: 'Tokyo', age: 33, start_date: '2008/11/28', salary: '162,700' },
        { id: 6, thumb: 'girl-4.png', name: 'Brielle Williamson', position: 'Integration Specialist', office: 'New York', age: 61, start_date: '2012/12/02', salary: '372,000' },
        { id: 7, thumb: 'boy.png', name: 'Herrod Chandler', position: 'Sales Assistant', office: 'San Francisco', age: 59, start_date: '2012/08/06', salary: '137,500' },
        { id: 8, thumb: 'girl-4.png', name: 'Rhona Davidson', position: 'Integration Specialist', office: 'Tokyo', age: 55, start_date: '2010/10/14', salary: '327,900' },
        { id: 9, thumb: 'girl-1.png', name: 'Colleen Hurst', position: 'Javascript Developer', office: 'San Francisco', age: 39, start_date: '2009/09/15', salary: '205,500' },
        { id: 10, thumb: 'girl-1.png', name: 'Sonya Frost', position: 'Software Engineer', office: 'Edinburgh', age: 23, start_date: '2008/12/13', salary: '103,600' },
        { id: 11, thumb: 'girl-2.png', name: 'Jena Gaines', position: 'Office Manager', office: 'London', age: 30, start_date: '2008/12/19', salary: '90,560' },
        { id: 12, thumb: 'girl-3.png', name: 'Quinn Flynn', position: 'Support Lead', office: 'Edinburgh', age: 22, start_date: '2013/03/03', salary: '342,000' },
        { id: 13, thumb: 'boy.png', name: 'Charde Marshall', position: 'Regional Director', office: 'San Francisco', age: 36, start_date: '2008/10/16', salary: '470,600' },
        { id: 14, thumb: 'girl-4.png', name: 'Haley Kennedy', position: 'Senior Marketing Designer', office: 'London', age: 43, start_date: '2012/12/18', salary: '313,500' },
        { id: 15, thumb: 'girl-2.png', name: 'Tatyana Fitzpatrick', position: 'Regional Director', office: 'London', age: 19, start_date: '2010/03/17', salary: '385,750' },
        { id: 16, thumb: 'boy.png', name: 'Michael Silva', position: 'Marketing Designer', office: 'London', age: 66, start_date: '2012/11/27', salary: '198,500' },
        { id: 17, thumb: 'boy-2.png', name: 'Paul Byrd', position: 'Chief Financial Officer (CFO)', office: 'New York', age: 64, start_date: '2010/06/09', salary: '725,000' },
        { id: 18, thumb: 'girl-2.png', name: 'Gloria Little', position: 'Systems Administrator', office: 'New York', age: 59, start_date: '2009/04/10', salary: '237,500' },
        { id: 19, thumb: 'girl-3.png', name: 'Bradley Greer', position: 'Software Engineer', office: 'London', age: 41, start_date: '2012/10/13', salary: '132,000' },
        { id: 20, thumb: 'girl-4.png', name: 'Dai Rios', position: 'Personnel Lead', office: 'Edinburgh', age: 35, start_date: '2012/09/26', salary: '217,500' },
        { id: 21, thumb: 'girl-1.png', name: 'Jenette Caldwell', position: 'Development Lead', office: 'New York', age: 61, start_date: '2011/09/03', salary: '345,000' },
        { id: 22, thumb: 'boy.png', name: 'Yuri Berry', position: 'Chief Marketing Officer (CMO)', office: 'New York', age: 40, start_date: '2009/06/25', salary: '675,000' },
        { id: 23, thumb: 'boy-2.png', name: 'Caesar Vance', position: 'Pre-Sales Support', office: 'New York', age: 21, start_date: '2011/12/12', salary: '106,450' },
        { id: 24, thumb: 'boy.png', name: 'Doris Wilder', position: 'Sales Assistant', office: 'Sidney', age: 23, start_date: '2010/09/20', salary: '85,600' },
        { id: 25, thumb: 'girl-2.png', name: 'Angelica Ramos', position: 'Chief Executive Officer (CEO)', office: 'London', age: 47, start_date: '2009/10/09', salary: '1,200,000' },
        { id: 26, thumb: 'boy-2.png', name: 'Gavin Joyce', position: 'Developer', office: 'Edinburgh', age: 42, start_date: '2010/12/22', salary: '92,575' },
        { id: 27, thumb: 'girl-3.png', name: 'Jennifer Chang', position: 'Regional Director', office: 'Singapore', age: 28, start_date: '2010/11/14', salary: '57,650' },
    ];
};

const export_table = (type) => {
    let cols = columns.value.filter((d) => d != 'profile' && d != 'action');
    let records = items.value;
    let filename = 'table';

    if (type == 'csv') {
        let coldelimiter = ',';
        let linedelimiter = '\n';
        let result = cols
            .map((d) => {
                return capitalize(d);
            })
            .join(coldelimiter);
        result += linedelimiter;
        records.map((item) => {
            cols.map((d, index) => {
                if (index > 0) {
                    result += coldelimiter;
                }
                let val = item[d] ? item[d] : '';
                result += val;
            });
            result += linedelimiter;
        });

        if (result == null) return;
        if (!result.match(/^data:text\/csv/i) && !window.navigator.msSaveOrOpenBlob) {
            var data = 'data:application/csv;charset=utf-8,' + encodeURIComponent(result);
            var link = document.createElement('a');
            link.setAttribute('href', data);
            link.setAttribute('download', filename + '.csv');
            link.click();
        } else {
            var blob = new Blob([result]);
            if (window.navigator.msSaveOrOpenBlob) {
                window.navigator.msSaveBlob(blob, filename + '.csv');
            }
        }
    } else if (type == 'print') {
        var rowhtml = '<p>' + filename + '</p>';
        rowhtml +=
            '<table style="width: 100%; " cellpadding="0" cellcpacing="0"><thead><tr style="color: #515365; background: #eff5ff; -webkit-print-color-adjust: exact; print-color-adjust: exact; "> ';
        cols.map((d) => {
            rowhtml += '<th>' + capitalize(d) + '</th>';
        });
        rowhtml += '</tr></thead>';
        rowhtml += '<tbody>';

        records.map((item) => {
            rowhtml += '<tr>';
            cols.map((d) => {
                let val = item[d] ? item[d] : '';
                rowhtml += '<td>' + val + '</td>';
            });
            rowhtml += '</tr>';
        });
        rowhtml +=
            '<style>body {font-family:Arial; color:#495057;}p{text-align:center;font-size:18px;font-weight:bold;margin:15px;}table{ border-collapse: collapse; border-spacing: 0; }th,td{font-size:12px;text-align:left;padding: 4px;}th{padding:8px 4px;}tr:nth-child(2n-1){background:#f7f7f7; }</style>';
        rowhtml += '</tbody></table>';
        var winPrint = window.open('', '', 'left=0,top=0,width=1000,height=600,toolbar=0,scrollbars=0,status=0');
        winPrint.document.write('<title>Print</title>' + rowhtml);
        winPrint.document.close();
        winPrint.focus();
        winPrint.print();
        // winPrint.close();
    } else if (type == 'pdf') {
        cols = cols.map((d) => {
            return { header: capitalize(d), dataKey: d };
        });
        const doc = new jsPDF('l', 'pt', cols.length > 10 ? 'a3' : 'a4');
        doc.autoTable({
            headStyles: { fillColor: '#eff5ff', textColor: '#515365' },
            columns: cols,
            body: records,
            styles: { overflow: 'linebreak' },
            pageBreak: 'auto',
            margin: { top: 45 },
            didDrawPage: () => {
                doc.text('Export Table', cols.length > 10 ? 535 : 365, 30);
            },
        });
        doc.save(filename + '.pdf');
    }
};
const print = () => {
    window.print();
};
const excel_columns = () => {
    return {
        Name: 'name',
        Position: 'position',
        Office: 'office',
        Age: 'age',
        'Start Date': 'start_date',
        Salary: 'salary',
    };
};
const excel_items = () => {
    return items.value;
};
const capitalize = (text) => {
    return text
        .replace('_', ' ')
        .replace('-', ' ')
        .toLowerCase()
        .split(' ')
        .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
        .join(' ');
};
</script>

<style type="text/css">
.table>tbody>tr>td {
    font-size: 10px;
    padding: 0rem 0rem;
    border: 0px;
    letter-spacing: 0px;
    color: #000000;
}

.table .bordered {
    border: 1px solid #000000
}

.table .underrow {
    font-size: 6px;
    text-align: center;
    vertical-align: text-top;
    padding-inline: 2em;
}

.table .header {
    font-weight: bold;
    text-align: center;
}

.table .sign {
    font-weight: 600;
    text-align: right;
    padding-inline: 2em;
    vertical-align: bottom;
}
</style>

<template>
    <div class="layout-px-spacing">
        <teleport to="#breadcrumb">
            <ul class="navbar-nav flex-row">
                <li>
                    <div class="page-header">
                        <nav class="breadcrumb-one" aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><a href="javascript:;">Apps</a></li>
                                <li class="breadcrumb-item active" aria-current="page"><span>Invoice Preview</span></li>
                            </ol>
                        </nav>
                    </div>
                </li>
            </ul>
        </teleport>

        <div class="row invoice layout-top-spacing layout-spacing apps-invoice">
            <div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12">
                <div class="doc-container">
                    <div class="row">
                        <div class="col-xl-7">
                            <div class="invoice-container">
                                <div class="invoice-inbox">
                                    <div id="ct" class="">
                                        <div class="invoice-00001">
                                            <div class="content-section">
                                                <div class="table-responsive">
                                                    <table class="table" cellspacing="0" cellpadding="0">
                                                        <tbody>
                                                            <tr>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                                <td style="width:7px"></td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td colspan="67"></td>
                                                                <td colspan="44">Приложение № 4</td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td colspan="67"></td>
                                                                <td colspan="44">к Правилам перевозок грузов
                                                                    автомобильным транспортом</td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td colspan="67"></td>
                                                                <td colspan="44">
                                                                    (в ред. Постановления Правительства РФ от 30.11.2021 №
                                                                    2116)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header" colspan="111">Транспортная накладная</td>
                                                            </tr>
                                                            <tr class="bordered" style="height: 20px">
                                                                <td class="header bordered" colspan="67">Транспортная
                                                                    накладная</td>
                                                                <td class="header bordered" colspan="44">Заказ (заявка)</td>
                                                            </tr>
                                                            <tr class="bordered" style="height: 20px">
                                                                <td class="ps-2" colspan="10">Дата</td>
                                                                <td class="bordered ps-2" colspan="24">07.04.2022</td>
                                                                <td class="ps-2" colspan="10">№</td>
                                                                <td class="ps-2" colspan="23">К-АПР.22-474-Т</td>
                                                                <td class="bordered ps-2" colspan="10">Дата</td>
                                                                <td class="ps-2" colspan="12">-</td>
                                                                <td class="bordered ps-2" colspan="10">№</td>
                                                                <td class="ps-2" colspan="12">-</td>
                                                            </tr>
                                                            <tr class="bordered" style="height: 20px">
                                                                <td class="ps-2" colspan="10">Экземпляр №</td>
                                                                <td class="bordered ps-2" colspan="57"></td>
                                                                <td class="bordered header ps-2" colspan="44">-</td>
                                                            </tr>
                                                            <tr class="bordered" style="height: 20px">
                                                                <td class="px-2 text-center" colspan="67">
                                                                    Общество с ограниченной
                                                                    ответственностью &quot;Магнит&quot;, ИНН
                                                                    5401381810, Адрес: 644024, Омская область, г. Омск, ул.
                                                                    Декабристов, дом 45, корп. 1, пом. 19, тел.
                                                                    8 (3812) 35-25-25
                                                                </td>
                                                                <td class="bordered header" colspan="44">-</td>
                                                            </tr>
                                                            <tr class="bordered" style="height: 12px">
                                                                <td class="underrow" colspan="67">
                                                                    (реквизиты, позволяющие идентифицировать
                                                                    Грузоотправителя)
                                                                </td>
                                                                <td class="underrow" colspan="44">
                                                                    (реквизиты, позволяющие
                                                                    идентифицировать Заказчика услуг по организации
                                                                    перевозки груза)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered header" colspan="67">-</td>
                                                                <td class="bordered header" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="bordered underrow" colspan="67">реквизиты
                                                                    документа,
                                                                    определяющего основания осуществления расчетов по
                                                                    договору перевозки иным лицом, отличным от
                                                                    грузоотправителя (при наличии)</td>
                                                                <td class="bordered underrow" colspan="44">(реквизиты
                                                                    договора на
                                                                    выполнение услуг по организации перевозки груза)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    2. Грузополучатель
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="111">
                                                                    Общество с ограниченной ответственностью
                                                                    &quot;Экосервис&quot;
                                                                    ИНН: 5507278919 Адрес: 644070, Омская область, г. Омск,
                                                                    ул. Куйбышева, д. 29, к 2 помещение 19П-308
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (реквизиты, позволяющие идентифицировать
                                                                    Грузополучателя)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="111">
                                                                    Омская область, Нововаршавский район, земельный участок
                                                                    расположен в северной части кадастрового квартала
                                                                    55:17:260501. Кадастровый номер земельного участка
                                                                    - 55:17:260501:665
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (адрес места доставки груза)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    3. Груз
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered text-center px-2" colspan="67">
                                                                    Остатки сортировки ТКО
                                                                </td>
                                                                <td class="bordered text-center px-2" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (отгрузочное наименование груза
                                                                    (для опасных грузов - в соответствии с
                                                                    ДОПОГ), его состояние и другая необходимая информация о
                                                                    грузе)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">(количество
                                                                    грузовых мест,
                                                                    маркировка, вид тары и способ упаковки)</td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    Объем груза - 34 м³, масса согласно акту
                                                                    взвешивания К-АПР.22-474-Т от 07.04.2022
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (масса груза брутто в
                                                                    килограммах, масса груза нетто в килограммах (при
                                                                    возможности ее определения), размеры (высота, ширина,
                                                                    длина) в метрах (при перевозке
                                                                    крупногабаритного груза), объем груза в кубических
                                                                    метрах и плотность груза в соответствии с
                                                                    документацией на груз (при необходимости),
                                                                    дополнительные характеристики груза, учитывающие
                                                                    отраслевые особенности (при необходимости)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (в случае перевозки опасного
                                                                    груза - информация по каждому опасному
                                                                    веществу, материалу или изделию в соответствии с пунктом
                                                                    5.4.1 ДОПОГ)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (объявленная стоимость
                                                                    (ценность) груза (при необходимости)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    4. Сопроводительные документы на груз (при наличии)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (перечень прилагаемых к транспортной накладной
                                                                    документов,
                                                                    предусмотренных ДОПОГ, санитарными, таможенными (при
                                                                    наличии),
                                                                    карантинными, иными правилами в соответствии с
                                                                    законодательством Российской Федерации, либо
                                                                    регистрационные номера указанных документов, если такие
                                                                    документы (сведения о таких документах) содержатся
                                                                    в государственных информационных системах)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (перечень прилагаемых к грузу
                                                                    сертификатов, паспортов качества,
                                                                    удостоверений и других документов, наличие которых
                                                                    установлено законодательством Российской
                                                                    Федерации, либо регистрационные номера указанных
                                                                    документов, если такие документы (сведения о таких
                                                                    документах) содержатся в государственных
                                                                    информационных системах)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    К-АПР.22-474-Т от 07.04.2022
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (реквизиты, позволяющие
                                                                    идентифицировать документ(-ы), подтверждающий(-ие)
                                                                    отгрузку товаров) (при наличии), реквизиты
                                                                    сопроводительной ведомости (при перевозке груженых
                                                                    контейнеров или порожних контейнеров)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    5. Указания грузоотправителя по
                                                                    особым условиям перевозки
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (маршрут перевозки, дата и
                                                                    время/сроки доставки груза (при необходимости)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (контактная информация о лицах,
                                                                    по указанию которых может осуществляться
                                                                    переадресовка)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (указания, необходимые для
                                                                    выполнения фитосанитарных, санитарных,
                                                                    карантинных, таможенных и прочих требований,
                                                                    установленных законодательством Российской
                                                                    Федерации)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (температурный режим перевозки
                                                                    груза (при необходимости), сведения о
                                                                    запорно-пломбировочных устройствах (в случае их
                                                                    предоставления грузоотправителем), запрещение
                                                                    перегрузки груза)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    6. Перевозчик
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="67">
                                                                    Общество с ограниченной ответственностью
                                                                    &quot;Монолит&quot; ИНН:
                                                                    7719457783 Адрес: 125466, город Москва, улица
                                                                    Родионовская, дом 2, квартира 96
                                                                </td>
                                                                <td class="bordered px-2 text-center" colspan="44">
                                                                    Шингарев Сергей Викторович ВУ - 99 24 315947, 01.02.2022
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (реквизиты, позволяющие
                                                                    идентифицировать Перевозчика)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (реквизиты, позволяющие
                                                                    идентифицировать водителя(-ей)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    7. Транспортное средство
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="67">
                                                                    Тягач SCANIA , Прицеп
                                                                    9453-0000010-50 34 м³, 25,39 т.
                                                                </td>
                                                                <td class="bordered px-2 text-center" colspan="44">
                                                                    К849ЕТ186, Прицеп: ВА686686
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (тип, марка, грузоподъемность
                                                                    (в тоннах), вместимость (в кубических метрах)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (регистрационный номер
                                                                    транспортного средства)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    Тип владения: 3 - аренда
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    Тип владения:
                                                                    1 - собственность;
                                                                    2 - совместная собственность супругов;
                                                                    3 - аренда;
                                                                    4 - лизинг;
                                                                    5 - безвозмездное пользование;
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="67">
                                                                    Договор № 05-11/2020-ЭА
                                                                </td>
                                                                <td class="bordered px-2 text-center" colspan="44">
                                                                    -
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (реквизиты документа(-ов),
                                                                    подтверждающего(-их) основание владения
                                                                    грузовым автомобилем (тягачом, а также прицепом
                                                                    (полуприцепом) (для типов владения 3, 4, 5)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (номер, дата и срок действия
                                                                    специального разрешения, установленный маршрут
                                                                    движения тяжеловесного и (или) крупногабаритного
                                                                    транспортного средства или транспортного
                                                                    средства, перевозящего опасный груз) (при наличии)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    8. Прием груза
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="111">
                                                                    Общество с ограниченной
                                                                    ответственностью &quot;Магнит&quot;
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (реквизиты лица, осуществляющего погрузку
                                                                    груза в транспортное средство)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="111">
                                                                    Общество с ограниченной
                                                                    ответственностью &quot;Магнит&quot;
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (наименование (ИНН) владельца
                                                                    объекта инфраструктуры пункта погрузки)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="67">
                                                                    Мусоросортировочный
                                                                    комплекс, расположенный по адресу:
                                                                    местоположение установлено относительно ориентира,
                                                                    расположенного в границах участка. Ориентир
                                                                    местоположения установлено примерно в 260 метрах
                                                                    западнее относительно ориентира, расположенного за
                                                                    пределами участка, с почтовым адресом: Омская область,
                                                                    г. Омск, Кировский АО, ул. Казахстанская 18.
                                                                    Кадастровый номер земельного участка – 55:36:190110:344
                                                                </td>
                                                                <td class="bordered px-2 text-center" colspan="44">
                                                                    07.04.2022 19:49
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (адрес места погрузки)</td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (заявленные дата и время подачи
                                                                    транспортного средства под погрузку)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="67">
                                                                    07.04.2022 19:49
                                                                </td>
                                                                <td class="bordered px-2 text-center" colspan="44">
                                                                    07.04.2022 20:11
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (фактические дата и время прибытия под погрузку)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (фактические дата и время убытия)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="111">
                                                                    Масса согласно акту взвешивания К-АПР.22-474-Т от
                                                                    07.04.2022
                                                                    способ - разница между массой ТС перед погрузкой и после
                                                                    погрузки
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (масса груза брутто в
                                                                    килограммах и метод ее определения (определение
                                                                    разницы между массой транспортного средства после
                                                                    погрузки и перед погрузкой по общей массе или
                                                                    взвешиванием поосно или расчетная масса груза)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (количество грузовых мест)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (тара, упаковка (при наличии)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (оговорки и замечания
                                                                    перевозчика (при наличии) о дате и времени
                                                                    прибытия/убытия, о состоянии, креплении груза, тары,
                                                                    упаковки, маркировки, опломбирования, о
                                                                    массе груза и количестве грузовых мест, о проведении
                                                                    погрузочных работ)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 37px">
                                                                <td class="bordered sign" colspan="67">
                                                                    Приказ ООО &quot;Магнит&quot; №168 от 31.12.20
                                                                </td>
                                                                <td class="bordered sign" colspan="44">
                                                                    Шингарев Сергей Викторович
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (подпись, расшифровка подписи
                                                                    лица, осуществившего погрузку груза, с
                                                                    указанием реквизитов документа, подтверждающего
                                                                    полномочия лица на погрузку груза)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (подпись, расшифровка подписи
                                                                    водителя, принявшего груз для перевозки)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    9. Переадресовка (при наличии)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (дата, вид переадресовки на
                                                                    бумажном носителе или в электронном виде (с
                                                                    указанием вида доставки документа)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (адрес нового пункта выгрузки,
                                                                    новые дата и время подачи транспортного
                                                                    средства под выгрузку)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (реквизиты лица, от которого
                                                                    получено указание на переадресовку)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (при изменении получателя груза
                                                                    - реквизиты нового получателя)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    10. Выдача груза
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="67">
                                                                    Омская область,
                                                                    Нововаршавский район, земельный участок расположен
                                                                    в северной части кадастрового квартала 55:17:260501.
                                                                    Кадастровый номер земельного участка -
                                                                    55:17:260501:665
                                                                </td>
                                                                <td class="bordered px-2 text-center" colspan="44"></td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (адрес места выгрузки)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (заявленные дата и время подачи
                                                                    транспортного средства под выгрузку)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67"></td>
                                                                <td class="header bordered" colspan="44"></td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (фактические дата и время прибытия)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (фактические дата и время убытия)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (фактическое состояние груза,
                                                                    тары, упаковки, маркировки, опломбирования)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (количество грузовых мест)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="bordered px-2 text-center" colspan="67">
                                                                    масса согласно акту взвешивания К-АПР.22-474-Т от
                                                                    07.04.2022
                                                                </td>
                                                                <td class="bordered px-2 text-center" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (масса груза брутто в
                                                                    килограммах, масса груза нетто в килограммах
                                                                    (при возможности ее определения), плотность груза в
                                                                    соответствии с документацией на груз (при
                                                                    необходимости)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (оговорки и замечания
                                                                    перевозчика (при наличии) о дате и времени
                                                                    прибытия/убытия, о состоянии груза, тары, упаковки,
                                                                    маркировки, опломбирования, о массе груза и
                                                                    количестве грузовых мест)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 37px">
                                                                <td class="bordered sign" colspan="67">
                                                                </td>
                                                                <td class="bordered sign" colspan="44">
                                                                    Шингарев Сергей Викторович
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (должность, подпись,
                                                                    расшифровка подписи грузополучателя или
                                                                    уполномоченного грузоотправителем лица)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (подпись, расшифровка подписи
                                                                    водителя, сдавшего груз грузополучателю
                                                                    или уполномоченному грузополучателем лицу)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    11. Отметки грузоотправителей,
                                                                    грузополучателей, перевозчиков (при
                                                                    необходимости)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="76">-</td>
                                                                <td class="header bordered" colspan="16">-</td>
                                                                <td class="header bordered" colspan="19">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="76">
                                                                    (краткое описание обстоятельств, послуживших основанием
                                                                    для отметки,
                                                                    сведения о коммерческих и иных актах, в том числе о
                                                                    погрузке/выгрузке груза)
                                                                </td>
                                                                <td class="underrow bordered" colspan="16">(расчет и размер
                                                                    штрафа)</td>
                                                                <td class="underrow bordered" colspan="19">(подпись, дата)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">
                                                                    12. Стоимость перевозки груза
                                                                    (установленная плата) в рублях (при
                                                                    необходимости)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="29">-</td>
                                                                <td class="header bordered" colspan="28">-</td>
                                                                <td class="header bordered" colspan="27">-</td>
                                                                <td class="header bordered" colspan="27">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="29">
                                                                    (стоимость перевозки без налога - всего)
                                                                </td>
                                                                <td class="underrow bordered" colspan="28">
                                                                    (налоговая ставка)
                                                                </td>
                                                                <td class="underrow bordered" colspan="27">
                                                                    (сумма налога, предъявляемая покупателю)
                                                                </td>
                                                                <td class="underrow bordered" colspan="27">
                                                                    (стоимость перевозки с налогом - всего)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="111">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="111">
                                                                    (порядок (механизм) расчета (исчислений) платы)
                                                                    (при наличии порядка (механизма)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (реквизиты, позволяющие
                                                                    идентифицировать Экономического субъекта,
                                                                    составляющего первичный учетный документ о факте
                                                                    хозяйственной жизни со стороны Перевозчика)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (реквизиты, позволяющие
                                                                    идентифицировать Экономического субъекта,
                                                                    составляющего первичный учетный документ о факте
                                                                    хозяйственной жизни со стороны
                                                                    Грузоотправителя)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (основание, по которому
                                                                    Экономический субъект является составителем <br>
                                                                    документа о факте хозяйственной жизни)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (основание, по которому
                                                                    Экономический субъект является составителем <br>
                                                                    документа о факте хозяйственной жизни)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">-</td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (реквизиты, позволяющие
                                                                    идентифицировать лицо, от которого будут поступать
                                                                    денежные средства)</td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="14">-</td>
                                                                <td class="header bordered" colspan="43">-</td>
                                                                <td class="header bordered" colspan="14">-</td>
                                                                <td class="header bordered" colspan="40">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (подпись, расшифровка подписи
                                                                    лица, ответственного за оформление факта
                                                                    хозяйственной жизни со стороны Перевозчика
                                                                    (уполномоченного лица)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (подпись, расшифровка подписи
                                                                    лица, ответственного за оформление факта
                                                                    хозяйственной жизни со стороны Грузоотправителя
                                                                    (уполномоченного лица)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="20">-</td>
                                                                <td class="header bordered" colspan="26">-</td>
                                                                <td class="header bordered" colspan="11">-</td>
                                                                <td class="header bordered" colspan="18">-</td>
                                                                <td class="header bordered" colspan="25">-</td>
                                                                <td class="header bordered" colspan="11">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (должность, основание
                                                                    полномочий физического лица, уполномоченного
                                                                    Перевозчиком (уполномоченным лицом), дата подписания)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (должность, основание
                                                                    полномочий физического лица, уполномоченного
                                                                    Грузоотправителем (уполномоченным лицом), дата
                                                                    подписания)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="67">-</td>
                                                                <td class="header bordered" colspan="44">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (подпись, расшифровка
                                                                    подписи
                                                                    лица, ответственного за оформление факта
                                                                    хозяйственной жизни со стороны Перевозчика
                                                                    (уполномоченного лица)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (подпись, расшифровка
                                                                    подписи
                                                                    лица, ответственного за оформление факта
                                                                    хозяйственной жизни со стороны Грузоотправителя
                                                                    (уполномоченного лица)
                                                                </td>
                                                            </tr>
                                                            <tr style="height: 20px">
                                                                <td class="header bordered" colspan="20">-</td>
                                                                <td class="header bordered" colspan="26">-</td>
                                                                <td class="header bordered" colspan="11">-</td>
                                                                <td class="header bordered" colspan="18">-</td>
                                                                <td class="header bordered" colspan="25">-</td>
                                                                <td class="header bordered" colspan="11">-</td>
                                                            </tr>
                                                            <tr style="height: 12px">
                                                                <td class="underrow bordered" colspan="67">
                                                                    (должность, основание
                                                                    полномочий физического лица, уполномоченного
                                                                    Перевозчиком (уполномоченным лицом), дата подписания)
                                                                </td>
                                                                <td class="underrow bordered" colspan="44">
                                                                    (должность, основание
                                                                    полномочий физического лица, уполномоченного
                                                                    Грузоотправителем (уполномоченным лицом), дата
                                                                    подписания)
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>

                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="col-xl-3">
                            <div class="invoice-actions-btn">
                                <div class="invoice-action-btn">
                                    <div class="row">
                                        <div class="col-xl-12 col-md-3 col-sm-6">
                                            <a href="javascript:;" class="btn btn-primary btn-send">Send Invoice</a>
                                        </div>
                                        <div class="col-xl-12 col-md-3 col-sm-6">
                                            <a href="javascript:;" class="btn btn-secondary btn-print action-print"
                                                @click="print()">Print</a>
                                        </div>
                                        <div class="col-xl-12 col-md-3 col-sm-6">
                                            <a href="javascript:;" class="btn btn-success btn-download">Download</a>
                                        </div>
                                        <div class="col-xl-12 col-md-3 col-sm-6">
                                            <router-link to="/apps/invoice/edit"
                                                class="btn btn-dark btn-edit">Edit</router-link>
                                        </div>
                                    </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div></template>
