<script setup>
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import visitDetails from '@/components/magnit/forms/visitDetailsEditable';
import { incNetto, lessEffectInc } from '@/scripts/weight_corrector'
import { Modal } from 'bootstrap';

//flatpickr
import flatpickr from 'flatpickr';
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import '@/assets/sass/forms/custom-flatpickr.css';

import { Russian } from "flatpickr/dist/l10n/ru.js"
import { integer } from '@vuelidate/validators';

import { utils, writeFile } from 'xlsx';

flatpickr.localize(Russian); // default locale is now Russian

const store = useStore();
useMeta({ title: 'Мусоровозы' });

const columns = ref([
    'permit',
    'lot',
    'carrier',
    'reg_number',
    // 'truck_model',
    'polygon',
    'checked_out',
    'brutto',
    'tara',
    'netto',
    'invoice_num',
    'print'
]);

if (store.state.AuthModule.credentials.user_role === 'Супервайзер') {
    columns.value = [
        'permit',
        'lot',
        'carrier',
        'reg_number',
        // 'truck_model',
        'polygon',
        'checked_out',
        'brutto',
        'tara',
        'netto',
        'invoice_num',
        'actions'
    ]
}

const isOpen = ref(false);
const item = ref(
    {
        id: '',
        permit: '',
        lot: '',
        contragent_id: '',
        garbage_truck: '',
        carrier: '',
        invoice_num: '',
        truck_model: '',
        truck_type: '',
        tara: '',
        netto: '',
        brutto: '',
        max_weight: '',
        reg_number: '',
        weighing_in: '',
        checked_in: '',
        weighing_out: '',
        checked_out: '',
        driver_name: '',
        destination: '',
        status: ''
    }
);
const table = ref(null);
const carrierFilter = ref([]);
const polygonFilter = ref([]);
const lotFilter = ref([]);
const table_option = ref({
    perPage: 10000000,
    perPageValues: [10000000,],
    skin: 'table table-hover',
    headings: {
        garbage_truck: '',
        invoice_num: 'Номер акта',
        permit: 'Пропуск',
        lot: 'Лот',
        reg_number: 'Номер',
        carrier: 'Контрагент',
        polygon: 'Полигон',
        truck_model: 'Марка ТС',
        truck_type: 'Тип ТС',
        checked_in: 'Въезд',
        checked_out: 'Время выезда',
        weight_in: 'Вес въезда, кг',
        status: 'Статус',
        brutto: 'Брутто',
        tara: 'Тара',
        netto: 'Нетто',
        destination: 'Направление',
        driver_name: 'Водитель',
        actions: '',
        print: '',
    },
    columnsClasses: { actions: 'actions text-center' },
    sortable: [
        'checked_out',
        'brutto',
        'tara',
        'netto',
    ],
    sortIcon: {
        base: 'sort-icon-none',
        up: 'sort-icon-asc',
        down: 'sort-icon-desc',
    },
    pagination: { nav: 'scroll', chunk: 5 },
    texts: {
        count: 'С {from} по {to} из {count}',
        filter: '',
        filterPlaceholder: 'Поиск...',
        limit: 'Показать:',
        noResults: "Нет данных",
        filterBy: "Фильтр",
        defaultOption: "Все", //{column}",
    },
    resizableColumns: false,
    filterByColumn: true,
    filterable: [
        'permit',
        // 'lot',
        'carrier',
        'reg_number',
        'polygon',
        'invoice_num',
    ],
    listColumns: {
        carrier: carrierFilter,
        lot: lotFilter,
        polygon: polygonFilter,
    },
});
const statuses = {
    0: `<span class="badge inv-status badge-warning">На полигоне</span>`,
    1: `<span class="badge inv-status badge-success">Выехал</span>`,
    2: `<span class="badge inv-status badge-dark">Удален</span>`,
};
const garbage_truck = {
    true: `<span class="badge inv-status outline-badge-warning">Tонар</span>`,
    false: '',
};
const openDetails = (i) => {
    console.log(i)
    item.value = i;
    isOpen.value = true;
};
const closeDetails = () => {
    isOpen.value = false;
};
const deleteItem = (id, reason) => {
    store.dispatch('VisitsModule/delete', {
        visit_id: id,
        reason: reason,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Удалено!', 'Данные помечены как удаленные.', 'success');
            store.dispatch('VisitsModule/update');
        }
    }).catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};
const printAkt = (visit_id) => {
    let winPrint = window.open(
        '/akt_with_lot?print=true&visit_id=' + visit_id,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
};

const excel_columns = () => {
    return {
        'Пропуск': 'permit',
        'Лот': 'lot',
        'Контрагент': 'carrier',
        'Рег.номер': 'reg_number',
        'Марка ТС': 'truck_model',
        'Полигон': 'polygon',
        'Дата заезда': 'checked_in',
        'Брутто': 'brutto',
        'Тара': 'tara',
        'Нетто': 'netto',
        'Номер акта': 'invoice_num',
    };
};
const excel_items = () => {
    let items = []
    for (var row of table.value.filteredData) {
        items.push({
            'Пропуск': row.permit,
            'Лот': row.lot ? row.lot.number : null,
            'Контрагент': row.carrier,
            'Рег.номер': row.reg_number,
            'Марка ТС': row.truck_model,
            'Полигон': row.polygon,
            'Время выезда': row.checked_out.toLocaleString('ru'),
            'Брутто': row.brutto,
            'Тара': row.tara,
            'Нетто': row.netto,
            'Номер акта': row.invoice_num,
        })
    }
    return items;
};

const change = (x) => {
    if (x.length == 2) {
        after = x[0].setHours(0, 0, 0, 0)
        before = x[1].setHours(23, 59, 59, 0)
        resetData();
    }
};
const bulkPrintAkt = () => {
    store.dispatch('VisitsModule/setAkts', table.value.filteredData);
    let winPrint = window.open(
        '/doc/bulk_akt?print=true', 'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
}
const journalMSK = () => {
    store.dispatch('VisitsModule/setAkts', table.value.filteredData);
    let winPrint = window.open(
        '/doc/journal_msk?print=true', 'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
}

let detailModal = null;
const visitDetailsModal = ref(null)
const initDetailsModal = () => {
    detailModal = new Modal(visitDetailsModal.value)
    // visitDetailsModal.value.addEventListener("hidden.bs.modal", onHidden)
};
const updateVisitsModal = ref(null)
const updateVisits = ref([]);
let exportModal = null;
const fileXlsx = ref(null);
const initupdateVisitsModal = () => {
    exportModal = new Modal(updateVisitsModal.value)
    updateVisitsModal.value.addEventListener("hidden.bs.modal", () => fileXlsx.value = null)
};
const analyticMethod = ref("minEffect");
const updatedCount = ref(0);
const totalWeight = ref();
const changed_visits = ref(null);
const visitsStat = ref({
    count: 0,
    weight: {
        before: {
            min: '',
            avg: '',
            max: '',
            total: '',
        },
        after: {
            min: '',
            avg: '',
            max: '',
            total: '',
        },
    },
    loading: {
        before: {
            min: '',
            avg: '',
            max: '',
        },
        after: {
            min: '',
            avg: '',
            max: '',
        },
    }
})
const calculateBeforeData = () => {
    let loadings = []
    let totalNettos = []
    for (var visit of table.value.filteredData) {
        loadings.push(visit.brutto / visit.max_weight * 100)
        totalNettos.push(parseInt(visit.netto))
    }
    visitsStat.value.count = table.value.filteredData.length
    visitsStat.value.weight.before.min = Math.min(...totalNettos)
    visitsStat.value.weight.before.max = Math.max(...totalNettos)
    visitsStat.value.weight.before.total = totalNettos.reduce((a, b) => a + b, 0)
    visitsStat.value.weight.before.avg = Math.trunc(visitsStat.value.weight.before.total / totalNettos.length * 100) / 100;

    visitsStat.value.loading.before.min = Math.trunc(Math.min(...loadings) * 100) / 100;
    visitsStat.value.loading.before.max = Math.trunc(Math.max(...loadings) * 100) / 100;
    visitsStat.value.loading.before.avg = Math.trunc(loadings.reduce((a, b) => a + b, 0) / loadings.length * 100) / 100;
}
const calculateAfterData = () => {
    let loadings = []
    let totalNettos = []
    for (let visit of table.value.filteredData) {
        loadings.push(visit.brutto / visit.max_weight * 100)
        totalNettos.push(parseInt(visit.netto))
    }
    visitsStat.value.weight.after.min = Math.min(...totalNettos)
    visitsStat.value.weight.after.max = Math.max(...totalNettos)
    visitsStat.value.weight.after.total = totalNettos.reduce((a, b) => a + b, 0)
    visitsStat.value.weight.after.avg = Math.trunc(visitsStat.value.weight.after.total / totalNettos.length * 100) / 100;

    visitsStat.value.loading.after.min = Math.trunc(Math.min(...loadings) * 100) / 100;
    visitsStat.value.loading.after.max = Math.trunc(Math.max(...loadings) * 100) / 100;
    visitsStat.value.loading.after.avg = Math.trunc(loadings.reduce((a, b) => a + b, 0) / loadings.length * 100) / 100;
}
const updateNetto = () => {
    calculateBeforeData();
    exportModal.show();
};
const applyMethod = () => {
    if (analyticMethod.value === 'max') {
        let v = incNetto(table.value.filteredData)
        updatedCount.value = v.count
        changed_visits.value = v.visits
    } else if (analyticMethod.value === 'def') {
        let v = incNetto(table.value.filteredData, totalWeight.value)
        updatedCount.value = v.count
        changed_visits.value = v.visits
    } else if (analyticMethod.value === 'minEffect') {
        let v = lessEffectInc(table.value.filteredData, totalWeight.value)
        updatedCount.value = v.count
        changed_visits.value = v.visits

        // console.log(`changed_visits.value = ${changed_visits.value}`)
        // console.log(`updatedCount.value = ${updatedCount.value}`)
    };
    for (let visit of changed_visits.value) {
        let i = store.state.VisitsModule.garbage_truck_visits.findIndex((v) => v.id === visit.id);
        if (i === -1) continue;
        store.state.VisitsModule.garbage_truck_visits[i] = visit;
    };
    calculateAfterData();
}
const saveData = () => {
    let data = []
    for (let visit of changed_visits.value) {
        data.push({
            id: visit.id,
            weight_in: visit.weight_in,
            // weight_out: visit.weight_out,
        })
    };
    store.dispatch('VisitsModule/bulk_update', data)
        .then((res) => {
            if (res.data.success) {
                exportModal.hide()
                new window.Swal('Сохранено!', 'Данные успешно сохранены.', 'success');
                resetData();
            }
        })
        .catch((error) => {
            new window.Swal('Ошибка!', error.message, 'error')
        });
};




let after = null;
let before = null;
const resetData = () => {
    store.dispatch('VisitsModule/update_garbage_trucks', { after, before })
        .then(() => {
            if (store.state.VisitsModule.garbage_truck_visits == 0) return;
            carrierFilter.value = [...new Set(store.state.VisitsModule.garbage_truck_visits.map(item => item.carrier))].map(item => ({ text: item }));
            polygonFilter.value = [...new Set(store.state.VisitsModule.garbage_truck_visits.map(item => item.polygon))].map(item => ({ text: item }));
            lotFilter.value = [...new Set(store.state.VisitsModule.garbage_truck_visits.map(item => item.lot))].map(item => ({ text: item }));
        });
    changed_visits.value = null;
    updatedCount.value = 0;

    visitsStat.value.weight.after.min = ''
    visitsStat.value.weight.after.max = ''
    visitsStat.value.weight.after.total = ''
    visitsStat.value.weight.after.avg = ''

    visitsStat.value.loading.after.min = ''
    visitsStat.value.loading.after.max = ''
    visitsStat.value.loading.after.avg = ''
};

const interval = ref([]);
const bind_data = async () => {
    if (store.state.VisitsModule.garbage_truck_visits.length != 0) {
        interval.value = [
            Math.min(...store.state.VisitsModule.garbage_truck_visits.map(o => o.checked_out)),
            Math.max(...store.state.VisitsModule.garbage_truck_visits.map(o => o.checked_out))
        ]
        return;
    };

    after = (new Date()).setHours(0, 0, 0, 0);
    before = (new Date()).setHours(23, 59, 59, 0);
    interval.value = [after, before]
    // resetData();
};
const download = () => {
    const data = utils.json_to_sheet(excel_items())
    const wb = utils.book_new()
    utils.book_append_sheet(wb, data, 'Визиты мусоровозов')
    writeFile(wb, 'Визиты мусоровозов.xlsx')
};
onMounted(
    () => {
        bind_data();
        initupdateVisitsModal();
        initDetailsModal();

        store.dispatch('TrucksModule/get_lots');
    }
);
const polygons = [
    'Кировский',
    'Ленинский',
    'Калачинский',
]

const updateVisit = (visit) => {
    store.dispatch('VisitsModule/update_visit', {
        weight_in: visit.weight_in,
        weight_out: visit.weight_out,
        visit_id: visit.id,
        driver_id: visit.driver_id,
        contract_id: visit.contract_id,
        lot_id: visit.lot_id,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Успешно!', 'Данные сохранены.', 'success');
            detailModal.hide();
            store.dispatch('VisitsModule/update_garbage_trucks', { after, before });
        }
    }).catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};
</script>
<style>
.table .actions .print:hover {
    color: #1abc9c;
}

.w-stat-sum {
    color: #f8538d;
    font-size: 14px;
    letter-spacing: 1px;
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
                                <li class="breadcrumb-item active" aria-current="page">
                                    <span>{{ $t('garbage_trucks') }}</span>
                                </li>
                            </ol>
                        </nav>
                    </div>
                </li>
            </ul>
            <div class="navbar-nav d-flex justify-content-end align-items-center">
                <!-- <h6 class="mb-0 me-2">Данные&nbspза:</h6> -->
                <flat-pickr v-model="interval" :config="{ dateFormat: 'd.m.Y', mode: 'range' }"
                    class="form-control flatpickr active me-4 width-100 text-center" style="width: 18em; height: 2.5em;"
                    @on-change="change"></flat-pickr>
                <button type="button" class="btn btn-primary me-4"
                    v-on:click="download">Выгрузить&nbspв&nbspExcel</button>
            </div>
        </teleport>

        <div class="row layout-top-spacing">
            <div v-show="store.state.VisitsModule.garbage_truck_visits.length > 0"
                class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12 layout-spacing pb-4">
                <div class="widget widget-statistics">
                    <div class="widget-heading pb-0">
                        <h5>Статистика</h5>
                        <div class="task-action">
                            <div class="mb-4 me-2 custom-dropdown btn-group">
                                <a class="btn dropdown-toggle btn-icon-only" href="#" role="button" id="pendingTask"
                                    data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <svg xmlns="http://www.w3.org/2000/svg" style="width: 24px; height: 24px" width="24"
                                        height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                        class="feather feather-more-horizontal"
                                        :class="changed_visits ? 'text-danger' : ''">
                                        <circle cx="12" cy="12" r="1"></circle>
                                        <circle cx="19" cy="12" r="1"></circle>
                                        <circle cx="5" cy="12" r="1"></circle>
                                    </svg>
                                </a>
                                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="pendingTask">
                                    <li v-show="['Супервайзер'].includes(store.state.AuthModule.credentials.user_role)">
                                        <a href="javascript:void(0);" class="dropdown-item" @click="updateNetto()">
                                            Изменить
                                        </a>
                                    </li>
                                    <li v-show="changed_visits">
                                        <a href="javascript:void(0);" class="dropdown-item" @click="saveNettoChanges()">
                                            Сохранить
                                        </a>
                                    </li>
                                    <li>
                                        <a href="javascript:void(0);" class="dropdown-item" @click="bulkPrintAkt()">
                                            Печать актов
                                        </a>
                                    </li>
                                    <li class="mt-3 text-danger" v-show="changed_visits">
                                        <a href="javascript:void(0);" class="dropdown-item text-danger"
                                            @click="resetData()">
                                            Сбросить
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="widget-content pt-0">
                        <table role="table" aria-busy="false" aria-colcount="5" class="w-detail table b-table my-4">
                            <thead role="rowgroup" class="w-title">
                                <tr role="row">
                                    <th role="columnheader" scope="col" aria-colindex="1">
                                        <p class="w-title">Полигон</p>
                                    </th>
                                    <th role="columnheader" scope="col" aria-colindex="3">
                                        <p class="w-title">Визитов</p>
                                    </th>
                                    <th role="columnheader" scope="col" aria-colindex="3">
                                        <p class="w-title">Сум. нетто</p>
                                    </th>
                                    <th role="columnheader" scope="col" aria-colindex="3">
                                        <p class="w-title">Мин. нетто</p>
                                    </th>
                                    <th role="columnheader" scope="col" aria-colindex="3">
                                        <p class="w-title">Среднее нетто</p>
                                    </th>
                                    <th role="columnheader" scope="col" aria-colindex="3">
                                        <p class="w-title">Макс. нетто</p>
                                    </th>
                                </tr>
                            </thead>
                            <tbody role="rowgroup" class="w-stats">
                                <tr v-for="polygon in polygons" :key="polygon.id">
                                    <td>{{ polygon }}</td>
                                    <td>{{ table ? table.filteredData.reduce(
                                        (acc, visit) => acc + (visit.polygon == polygon ? 1 : 0), 0
                                    ).toLocaleString('ru') : 0 }}</td>
                                    <td>{{ Math.round(table ? table.filteredData.reduce(
                                        (acc, visit) => acc + (visit.polygon == polygon ? visit.netto : 0), 0
                                    ) : 0).toLocaleString('ru') }}</td>
                                    <td>
                                        {{ Math.min(
                                        ...(table ? table.filteredData
                                            .filter(o => o.polygon == polygon)
                                            .map(o => o.netto) :
                                            [])).toLocaleString('ru') }}</td>
                                    <td>{{ Math.round(table ? table.filteredData
                                        .filter(o => o.polygon == polygon)
                                        .reduce(
                                            (acc, visit) => acc + visit.netto / table.filteredData
                                                .filter(o => o.polygon == polygon).length, 0) :
                                        0).toLocaleString('ru') }}
                                    </td>
                                    <td>{{ Math.max(
                                        ...(table ? table.filteredData
                                            .filter(o => o.polygon == polygon)
                                            .map(o => o.netto) :
                                            [])).toLocaleString('ru') }}</td>
                                </tr>
                            </tbody>
                            <tfoot class="mt-2">
                                <tr>
                                    <td class="fw-bold w-stat-sum">ОБЩЕЕ</td>
                                    <td class="fw-bold w-stat-sum">{{ table ?
                                        table.filteredData.length.toLocaleString('ru')
                                        : 0 }}</td>
                                    <td class="fw-bold w-stat-sum">{{ Math.round(table ? table.filteredData.reduce(
                                        (acc, visit) => acc + visit.netto, 0) : 0).toLocaleString('ru') }}</td>
                                    <td class="fw-bold w-stat-sum">{{ Math.min(...(table ? table.filteredData.map(o =>
                                        o.netto) :
                                        [])).toLocaleString('ru') }}</td>
                                    <td class="fw-bold w-stat-sum">{{ Math.round(table ? table.filteredData.reduce(
                                        (acc, visit) => acc + visit.netto / table.filteredData.length, 0) :
                                        0).toLocaleString('ru') }}</td>
                                    <td class="fw-bold w-stat-sum">{{ Math.max(...(table ? table.filteredData.map(o =>
                                        o.netto) :
                                        [])).toLocaleString('ru') }}</td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
            </div>
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="store.state.VisitsModule.garbage_truck_visits" :columns="columns"
                            :options="table_option" ref="table">
                            <template #checked_out="props">
                                <div :data_sort="props.row.checked_out">{{ props.row.checked_out.toLocaleString('ru') }}
                                </div>
                            </template>
                            <template #status="props">
                                <div v-html="statuses[props.row.status]"></div>
                            </template>
                            <template #lot="props">
                                <div>{{ props.row.lot ? props.row.lot.number : null }}</div>
                            </template>
                            <template #print="props">
                                <div class="actions text-center">
                                    <a href="javascript:;" class="print" @click="printAkt(props.row.id)">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                            stroke-linecap="round" stroke-linejoin="round"
                                            class="feather feather-printer me-3">
                                            <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                            <path
                                                d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2">
                                            </path>
                                            <rect x="6" y="14" width="12" height="8"></rect>
                                        </svg>
                                    </a>
                                </div>
                            </template>
                            <template #actions="props">
                                <div class="actions text-center">
                                    <a href="javascript:;" class="btn btn-primary btn-sm"
                                        @click="openDetails(props.row)">Открыть</a>
                                </div>
                            </template>
                        </v-client-table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" ref="visitDetailsModal" tabindex="-1" role="dialog" aria-labelledby="visitDetailsModalLable"
        aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="visitDetailsModalLable">{{ visitDetails.invoice_num }}</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="permit">Пропуск</label>
                            <input v-model="visitDetails.permit" type="text" readonly="true" class="form-control"
                                id="permit" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="reg_num">Рег. номер</label>
                            <input v-model="visitDetails.reg_number" type="text" readonly="true" class="form-control"
                                id="reg_num" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="polygon">Полигон</label>
                            <input v-model="visitDetails.polygon" type="text" readonly="true" class="form-control"
                                id="polygon" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="carrier">Компания-перевозчик</label>
                            <input v-model="visitDetails.carrier" type="text" readonly="true" class="form-control"
                                id="carrier" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="checked_in">Дата въезда</label>
                            <input :value="visitDetails.checked_in ? visitDetails.checked_in.toLocaleString('ru') : ''"
                                type="text" readonly="true" class="form-control" id="checked_in" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="checked_out">Дата выезда</label>
                            <input
                                :value="visitDetails.checked_out ? visitDetails.checked_out.toLocaleString('ru') : ''"
                                type="text" readonly="true" class="form-control" id="checked_out" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="weight_in">Вес въезда</label>
                            <input v-model="visitDetails.weight_in" type="number" class="form-control" id="weight_in" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="weight_out">Вес выезда</label>
                            <input v-model="visitDetails.weight_out" type="number" class="form-control"
                                id="weight_out" />
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button :disabled="item.is_deleted" type="button" class="btn btn-danger me-auto"
                        @click.prevent="deleteVisit">Удалить</button>
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Отмена</button>
                    <div class="btn-group custom-dropdown" role="group">
                        <button type="button" class="btn btn-outline-secondary dropdown-toggle"
                            data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-printer me-3">
                                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2">
                                </path>
                                <rect x="6" y="14" width="12" height="8"></rect>
                            </svg>
                            Печать
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-chevron-down">
                                <polyline points="6 9 12 15 18 9"></polyline>
                            </svg>
                        </button>
                        <ul class="dropdown-menu" aria-labelledby="btndefault">
                            <li>
                                <a @click="printAkt()" href="javascript:void(0);" class="dropdown-item"><i
                                        class="flaticon-gear-fill me-1"></i>
                                    Акт взвешивания
                                </a>
                            </li>
                        </ul>
                    </div>
                    <button type="button" class="btn btn-primary" @click.prevent="updateVisit">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>


    <div class="modal fade" ref="updateVisitsModal" tabindex="-1" role="dialog" aria-labelledby="updateVisitsModalLable"
        aria-hidden="true">
        <div class="modal-dialog modal-xl" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="updateVisitsModalLable">Аналитика</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <form class="row mb-3">
                        <div class="col-md-5">
                            <label class="col-form-label">Метод</label>
                            <select class="form-select form-select" v-model="analyticMethod">
                                <option selected value="minEffect">Мин. эффект</option>
                                <option value="max">К большему</option>
                                <option value="def">Точно</option>
                            </select>
                        </div>
                        <div class="col-md-5">
                            <label class="col-form-label" for="totalWeight">Вес, кг</label>
                            <input v-model="totalWeight" type="number" step=20 class="form-control"
                                :readonly="analyticMethod === 'max'" id="totalWeight" />
                        </div>
                        <div class="col-md-2 d-flex align-content-end flex-wrap">
                            <button type="button" class="btn btn-outline-primary btn-lg w-100" @click="applyMethod">
                                Применить
                            </button>
                        </div>
                    </form>
                    <table role="table" aria-busy="false" aria-colcount="5" class="table b-table my-4">
                        <thead role="rowgroup">
                            <tr role="row">
                                <th role="columnheader" scope="col" aria-colindex="1">
                                    <div></div>
                                </th>
                                <th role="columnheader" scope="col" aria-colindex="2">
                                    <div>Вес До, кг</div>
                                </th>
                                <th role="columnheader" scope="col" aria-colindex="3">
                                    <div>Вес После, кг</div>
                                </th>
                                <th role="columnheader" scope="col" aria-colindex="2">
                                    <div>Загрузка До, %</div>
                                </th>
                                <th role="columnheader" scope="col" aria-colindex="3">
                                    <div>Загрузка После, %</div>
                                </th>
                            </tr>
                        </thead>
                        <tbody role="rowgroup">
                            <tr>
                                <th>МИН</th>
                                <td>{{ visitsStat.weight.before.min.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.weight.after.min.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.loading.before.min.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.loading.after.min.toLocaleString('ru') }}</td>
                            </tr>
                            <tr>
                                <th>СРЕД</th>
                                <td>{{ visitsStat.weight.before.avg.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.weight.after.avg.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.loading.before.avg.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.loading.after.avg.toLocaleString('ru') }}</td>
                            </tr>
                            <tr>
                                <th>МАКС</th>
                                <td>{{ visitsStat.weight.before.max.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.weight.after.max.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.loading.before.max.toLocaleString('ru') }}</td>
                                <td>{{ visitsStat.loading.after.max.toLocaleString('ru') }}</td>
                            </tr>
                            <tr>
                                <th>ВСЕГО</th>
                                <td>
                                    {{ visitsStat.weight.before.total.toLocaleString('ru') }}
                                </td>
                                <td colspan="3">
                                    {{ visitsStat.weight.after.total.toLocaleString('ru') }}
                                </td>
                            </tr>
                            <tr>
                                <th>ИЗМЕНЕНО</th>
                                <td colspan="1">
                                </td>
                                <td colspan="3">
                                    {{ updatedCount }} из {{ visitsStat.count }} изменено - ( {{ (updatedCount * 100 /
                                        visitsStat.count).toLocaleString('ru') }}% )
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="modal-footer d-flex justify-content-between px-4">
                    <button type="button" class="btn btn-danger" @click.prevent="resetData">Сбросить</button>
                    <button type="button" class="btn ms-auto" data-dismiss="modal"
                        data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary ms-4" @click.prevent="saveData">Сохранить</button>
                </div>
            </div>
        </div>
    </div>

    <visitDetails :item="item" :isOpen="isOpen" @closed="closeDetails" @deleted="deleteItem"
        @print_akt="printAkt" @update_visit="updateVisit">
    </visitDetails>
</template>
