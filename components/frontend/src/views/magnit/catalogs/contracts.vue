<script setup>
import '@/assets/sass/widgets/widgets.scss';
import { onMounted, ref, computed } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { Modal } from 'bootstrap';
import { PolygonsAPI } from '@/api/polygonsAPI';
import { DriversAPI } from '@/api/driversAPI';
import { set_netto } from '@/scripts/weight_corrector'

import { EventBus } from 'v-tables-3';

import Multiselect from '@suadelabs/vue3-multiselect';
import '@suadelabs/vue3-multiselect/dist/vue3-multiselect.css';

import { utils, writeFile } from 'xlsx';

//flatpickr
import flatpickr from 'flatpickr';
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import '@/assets/sass/forms/custom-flatpickr.css';

import { Russian } from "flatpickr/dist/l10n/ru.js"

import finishVisit from '@/components/magnit/forms/finishVisit';

flatpickr.localize(Russian); // default locale is now Russian

const store = useStore();
useMeta({ title: 'Визиты' });

const columns = ref([
    'permit',
    'carrier',
    'polygon',
    'reg_number',
    'checked_in',
    'netto',
    'tonar',
    'invoice_num',
    'status',
    'actions'
]);
const table = ref(null)
const isOpen = ref(null);
const item = ref(
    {
        id: '',
        permit: '',
        contragent_id: '',
        tonar: '',
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
const polygons = ref([]);
const carriers = ref([]);
const driver_names = ref([]);
const destinations = ref([]);
const table_option = ref({
    perPage: 10000000,
    perPageValues: [10000000,],
    skin: 'table table-hover',
    headings: {
        tonar: '',
        invoice_num: 'Номер ТН',
        permit: 'Пропуск',
        reg_number: 'Рег. номер',
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
    },
    columnsClasses: { actions: 'actions text-center' },
    sortable: [
        'checked_out',
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
        'carrier',
        'reg_number',
        'polygon',
        'netto',
        'invoice_num',
        // 'destination',
        // 'driver_name',
        'tonar',
        'status',
    ],
    listColumns: {
        polygon: polygons,
        carrier: carriers,
        // driver_name: driver_names,
        // destination: destinations,
        status: [
            { id: 0, text: 'На полигоне' },
            { id: 1, text: 'Выехал' },
            { id: 2, text: 'Удален' },
        ],
        tonar: [
            { id: true, text: 'Да' },
            { id: false, text: 'Нет' },
        ],
    },
    customFilters: [
        {
            name: 'polygon',
            callback: (row, polygon) => row.polygon == polygon,
        },
        {
            name: 'clearPolygon',
            callback: (row, polygon) => row.polygon == polygon || row.polygon != polygon,
        },
    ],
});
const polygonFilter = ref(null)
const filterByPolygon = (polygon, _) => {
    EventBus.emit('vue-tables.filter::polygon', polygon)
    // }
    // else {
    //     showTable.value = !showTable.value;

    //     nextTick(() => showTable.value = !showTable.value)
    // }
};
const removeFilterByPolygon = (polygon, _) => {
    console.log(polygon)
    table.value.refresh()
    // EventBus.emit('vue-tables.remove-filter::clearPolygon', polygon)
    // }
    // else {
    //     showTable.value = !showTable.value;

    //     nextTick(() => showTable.value = !showTable.value)
    // }
};

const statuses = {
    0: `<span class="badge inv-status badge-warning">На полигоне</span>`,
    1: `<span class="badge inv-status badge-success">Выехал</span>`,
    2: `<span class="badge inv-status badge-dark">Удален</span>`,
};
const tonar = {
    true: `<span class="badge inv-status outline-badge-warning">Tонар</span>`,
    false: '',
};

const printTonarPack = (visit_id = visitDetails.value.id) => {
    let winPrint = window.open(
        '/doc/tonar_pack?print=true&visit_id=' + visit_id,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
};
const printInvoice = (visit_id = visitDetails.value.id) => {
    let winPrint = window.open(
        '/invoice?print=true&visit_id=' + visit_id,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
};
const printAkt = (visit_id = visitDetails.value.id) => {
    let winPrint = window.open(
        '/akt?print=true&visit_id=' + visit_id,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
};
let after = null;
let before = null;
const updateVisit = () => {
    store.dispatch('VisitsModule/update_visit', {
        weight_in: visitDetails.value.weight_in,
        weight_out: visitDetails.value.weight_out,
        visit_id: visitDetails.value.id,
        driver_id: visitDetails.value.driver_id,
        contract_id: visitDetails.value.contract_id,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Успешно!', 'Данные сохранены.', 'success');
            detailModal.hide();
            store.dispatch('VisitsModule/get_visits', { after, before });
        }
    }).catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};

const interval = ref([]);
const bind_data = () => {
    if (store.state.VisitsModule.visits.length != 0) {
        interval.value = [
            Math.min(...store.state.VisitsModule.visits.map(o => o.checked_out)),
            Math.max(...store.state.VisitsModule.visits.map(o => o.checked_out))
        ]
        return
    };

    // before = new Date();
    // after = new Date();
    after = (new Date()).setHours(0, 0, 0, 0);
    before = (new Date()).setHours(23, 59, 59, 0);
    interval.value = [after, before]
    // resetData();
};
const excel_items = () => {
    const rows = table.value ? table.value.filteredData : store.state.VisitsModule.visits
    let items = []
    for (var row of rows) {
        items.push({
            'Пропуск': row.permit,
            'Контрагент': row.carrier,
            'Рег.номер': row.reg_number,
            'Марка ТС': row.truck_model,
            'Полигон': row.polygon,
            'Время выезда': row.checked_out.toLocaleString('ru'),
            'Брутто': row.brutto,
            'Тара': row.tara,
            'Нетто': row.netto,
            'Номер ТН': row.invoice_num,
            'Направление': row.destination,
            'Водитель': row.driver_name,
        })
    }
    return items;
};


// Details Modal

let detailModal = null;

const visitDetails = ref(
    {
        id: '',
        truck_model: '',
        reg_number: '',
        truck_type: '',
        tara: '',
        max_weight: '',
        permit: '',
        permission_owner: '',
        started_at: '',
        expired_at: '',
        days_before_exp: '',
        body_volume: '',
        driver_id: '',
        contract_id: '',
    }
);
const visitDetailsModal = ref(null)
const drivers = ref([]);
const directions = ref([]);
const initDetailsModal = () => {
    detailModal = new Modal(visitDetailsModal.value)
    visitDetailsModal.value.addEventListener("hidden.bs.modal", onHidden)
};

const finishModal = ref(false)
const openDetails = (i) => {
    DriversAPI.get(i.contragent_id).then((ref) => (drivers.value = ref.data));
    PolygonsAPI.get_directions(i.polygon_id, i.contragent_id).then((ref) => (directions.value = ref.data));
    visitDetails.value = i;
    finishModal.value = false;
    detailModal.show();
};
const onHidden = () => {
    drivers.value = [];
    directions.value = [];
};
const change = (x) => {
    if (x.length == 2) {
        after = x[0].setHours(0, 0, 0, 0)
        before = x[1].setHours(23, 59, 59, 0)
        resetData();
    }
};

const deleteVisit = async () => {
    detailModal.hide();
    const deleteReasonQ = window.Swal.mixin({
        confirmButtonText: 'Удалить',
        showCancelButton: true,
        input: 'text',
        inputAttributes: {
            required: true,
        },
        validationMessage: 'Обязательно для заполнения!',
        padding: '2em',
    });
    let delete_reason;
    for (let step = 0; step < 2; step++) {
        if (step === 0) {
            const result = await deleteReasonQ.fire({
                title: 'Удаление визита',
                text: 'Укажите причину удаления',
                showCancelButton: true,
                cancelButtonText: 'Отменить',
                currentProgressStep: step,
            });
            if (result.dismiss === window.Swal.DismissReason.cancel) {
                break;
            };
            if (result.dismiss === window.Swal.DismissReason.backdrop) {
                break;
            };
            delete_reason = result.value;
            if (result.value) {
                deleteItem(visitDetails.value.id, delete_reason)
            };
            continue;
        };

    };
};
const changed_visits = ref(null);
const updateNetto = async () => {
    const targetNetto = window.Swal.mixin({
        confirmButtonText: 'Изменить',
        showCancelButton: true,
        input: 'number',
        inputAttributes: {
            required: true,
        },
        validationMessage: 'Обязательно для заполнения!',
        padding: '2em',
    });
    for (let step = 0; step < 2; step++) {
        if (step === 0) {
            const result = await targetNetto.fire({
                title: 'Изменить общее нетто',
                html: 'Введите нетто для выбранной группы.<br>В килограммах, кратно 20.',
                showCancelButton: true,
                cancelButtonText: 'Отменить',
                currentProgressStep: step,
            });
            if (result.dismiss === window.Swal.DismissReason.cancel) {
                break;
            };
            if (result.dismiss === window.Swal.DismissReason.backdrop) {
                break;
            };
            if (result.value) {
                console.log('HERE')
                changed_visits.value = set_netto(table.value.filteredData, result.value)
                for (let visit of changed_visits.value) {
                    let i = store.state.VisitsModule.visits.findIndex((v) => v.id === visit.id)

                    if (i === -1) continue

                    store.state.VisitsModule.visits[i] = visit
                }
            };
            continue;
        };

    };
};
const finishModalShow = () => {
    detailModal.hide();
    finishModal.value = true;

}

const getOut = (data) => {
    store.dispatch('VisitsModule/finish', {
        visit_id: data.visit_id,
        weight_out: data.out_weight,
        driver_id: data.driver,
        contract_id: data.direction,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Успешно!', 'Автомобиль выехал.', 'success');
            resetData();
        }
    })
        .catch((error) => new window.Swal('Ошибка!', error.data, 'error'))
};
const resetData = () => {
    store.dispatch('VisitsModule/get_visits', { after, before })
        .then(() => {
            polygons.value = [...new Set(store.state.VisitsModule.visits.map(item => item.polygon))].map(item => ({ text: item }));
            carriers.value = [...new Set(store.state.VisitsModule.visits.map(item => item.carrier))].map(item => ({ text: item }));
            driver_names.value = [...new Set(store.state.VisitsModule.visits.map(item => item.driver_name))].map(item => ({ text: item }));
            destinations.value = [...new Set(store.state.VisitsModule.visits.map(item => item.destination))].map(item => ({ text: item }));
        });
};

const bulkPrintAkt = () => {
    store.dispatch('VisitsModule/setAkts', table.value.filteredData);
    let winPrint = window.open(
        '/doc/bulk_akt?print=true', 'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
}
const bulkPrintInvoice = () => {
    store.dispatch('VisitsModule/setAkts', table.value.filteredData);
    let winPrint = window.open(
        '/doc/bulk_invoice?print=true', 'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
}
const bulkPrintPack = () => {
    store.dispatch('VisitsModule/setAkts', table.value.filteredData);
    let winPrint = window.open(
        '/doc/bulk_pack?print=true', 'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
}
const deleteItem = (id, reason) => {
    store.dispatch('VisitsModule/delete', {
        visit_id: id,
        reason: reason,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Удалено!', 'Данные помечены как удаленные.', 'success');
            resetData();
        }
    }).catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};
const fileXlsx = ref(null);
const exportErrorModal = ref(null);
const exportErrors = ref([]);
let exportModal = null;
const initExportErrorModal = () => {
    exportModal = new Modal(exportErrorModal.value)
    exportErrorModal.value.addEventListener("hidden.bs.modal", () => fileXlsx.value = null)
};
const fileInputKey = ref(0)
const save = () => {
    showMessage('Settings saved successfully.');
};

const showMessage = (msg = '', type = 'success') => {
    const toast = window.Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        padding: '2em'
    });
    toast.fire({
        icon: type,
        title: msg,
        padding: '2em'
    });
};
const download = () => {
    const data = utils.json_to_sheet(excel_items())
    const wb = utils.book_new()
    utils.book_append_sheet(wb, data, `Все визиты`)
    writeFile(wb, 'Все визиты.xlsx')
};

onMounted(
    () => {
        bind_data();
        initDetailsModal();
        initExportErrorModal();
    }
);
</script>
<style>
.multiselect__option--highlight {
    background: #fff;
    color: #4361ee;
}

.multiselect__option--selected {
    background-color: rgba(27, 85, 226, 0.23921568627450981);
    color: #4361ee;
    font-weight: normal;
}

.multiselect__option--disabled {
    background: inherit !important;
}

.multiselect__tags {
    width: 18em;
    height: 2.5em;
}

.multiselect__tag {
    color: #000;
    background: #e4e4e4;
}

.multiselect__tag-icon:after {
    color: #000 !important;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
    background: inherit;
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
                                    <span>{{ $t('visits') }}</span>
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
                <button type="button" class="btn btn-primary me-4" v-on:click="download">Выгрузить&nbspв&nbspExcel</button>
            </div>
        </teleport>
        <div class="row layout-top-spacing">
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="store.state.VisitsModule.visits" :columns="columns" :options="table_option"
                            ref="table">
                            <template #checked_in="props">
                                <div :data_sort="props.row.checked_in">{{ props.row.checked_in.toLocaleString('ru') }}
                                </div>
                            </template>
                            <template #status="props">
                                <div v-html="statuses[props.row.status]"></div>
                            </template>
                            <template #tonar="props">
                                <div :data_sort="props.row.tonar" v-html="tonar[props.row.tonar]"></div>
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
                            <input :value="visitDetails.checked_out ? visitDetails.checked_out.toLocaleString('ru') : ''"
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
                            <input v-model="visitDetails.weight_out" type="number" class="form-control" id="weight_out" />
                        </div>
                    </div>
                    <div v-show="visitDetails.tonar" class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="direction">Направление</label>
                            <select class="form-select form-select" v-model="visitDetails.contract_id">
                                <option selected disabled>Выберите значение</option>
                                <option v-for="t in directions" :value="t.id">{{ t.name }}
                                </option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="driver">Водитель</label>
                            <select class="form-select form-select" v-model="visitDetails.driver_id">
                                <option selected disabled>Выберите значение</option>
                                <option v-for="t in drivers" :value="t.id">{{ t.name }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-show="visitDetails.is_deleted" class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="delete_reason">Причина удаления</label>
                            <input v-model="visitDetails.delete_reason" type="text" readonly="true" class="form-control"
                                id="delete_reason" />
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button :disabled="visitDetails.is_deleted" type="button" class="btn btn-danger me-auto"
                        @click.prevent="deleteVisit">Удалить</button>
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Отмена</button>
                    <div class="btn-group custom-dropdown" role="group">
                        <button :disabled="visitDetails.is_deleted || !visitDetails.checked_out" type="button"
                            class="btn btn-outline-info dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true"
                            aria-expanded="false">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-printer me-3">
                                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                                <rect x="6" y="14" width="12" height="8"></rect>
                            </svg>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-chevron-down">
                                <polyline points="6 9 12 15 18 9"></polyline>
                            </svg>
                        </button>
                        <ul class="dropdown-menu" aria-labelledby="btndefault">
                            <li>
                                <a @click="printTonarPack()" href="javascript:void(0);" class="dropdown-item"><i
                                        class="flaticon-home-fill-1 me-1"></i>
                                    Пакет документов
                                </a>
                            </li>
                            <li>
                                <a @click="printAkt()" href="javascript:void(0);" class="dropdown-item"><i
                                        class="flaticon-gear-fill me-1"></i>
                                    Акт взвешивания
                                </a>
                            </li>
                            <li>
                                <a @click="printInvoice()" href="javascript:void(0);" class="dropdown-item"><i
                                        class="flaticon-bell-fill-2 me-1"></i>
                                    Транспортная накладная
                                </a>
                            </li>
                        </ul>
                    </div>
                    <button type="button" :disabled="visitDetails.is_deleted" class="btn btn-outline-success"
                        @click.prevent="updateVisit">
                        <!-- Сохранить -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="feather feather-save" data-v-5522efca="">
                            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                            <polyline points="17 21 17 13 7 13 7 21"></polyline>
                            <polyline points="7 3 7 8 15 8"></polyline>
                        </svg>
                    </button>
                    <button v-if="visitDetails.status == 0" type="button" class="btn btn-primary" @click="finishModalShow">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="feather feather-arrow-up-right">
                            <line x1="7" y1="17" x2="17" y2="7"></line>
                            <polyline points="7 7 17 7 17 17"></polyline>
                        </svg>
                        <!-- Выпустить -->
                    </button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" ref="exportErrorModal" tabindex="-1" role="dialog" aria-labelledby="exportErrorModalLable"
        aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title text-danger" id="exportErrorModalLable">Ошибки в файле экспорта</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <table role="table" aria-busy="false" aria-colcount="5" class="table b-table">
                        <thead role="rowgroup">
                            <tr role="row">
                                <th role="columnheader" scope="col" aria-colindex="1">
                                    <div>Строка</div>
                                </th>
                                <th role="columnheader" scope="col" aria-colindex="2">
                                    <div>Столбец</div>
                                </th>
                                <th role="columnheader" scope="col" aria-colindex="3">
                                    <div>Значение</div>
                                </th>
                                <th role="columnheader" scope="col" aria-colindex="4">
                                    <div>Комментарий</div>
                                </th>
                            </tr>
                        </thead>
                        <tbody role="rowgroup">
                            <tr v-for="item in exportErrors" :key="item.name" role="row">
                                <td aria-colindex="1" role="cell">{{ item.row }}</td>
                                <td aria-colindex="2" role="cell">{{ item.field }}</td>
                                <td aria-colindex="3" role="cell">{{ item.value }}</td>
                                <td aria-colindex="4" role="cell">{{ item.comment }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Закрыть</button>
                </div>
            </div>
        </div>
    </div>

    <finishVisit :item="visitDetails" :isOpen="finishModal" @closed="closeFinish" @get_out="getOut"></finishVisit>
</template>
