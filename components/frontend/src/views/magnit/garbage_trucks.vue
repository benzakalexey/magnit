<script setup>
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import visitDetails from '@/components/magnit/forms/visitDetails';
import set_netto from '@/scripts/weight_corrector'

//flatpickr
import flatpickr from 'flatpickr';
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import '@/assets/sass/forms/custom-flatpickr.css';

import { Russian } from "flatpickr/dist/l10n/ru.js"

flatpickr.localize(Russian); // default locale is now Russian

const store = useStore();
useMeta({ title: 'Мусоровозы' });

const columns = ref([
    'permit',
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

const isOpen = ref(null);
const item = ref(
    {
        id: '',
        permit: '',
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
const table_option = ref({
    perPage: 10000000,
    perPageValues: [10000000,],
    skin: 'table table-hover',
    headings: {
        garbage_truck: '',
        invoice_num: 'Номер акта',
        permit: 'Пропуск',
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
        filterBy: 'Фильтр'
    },
    resizableColumns: false,
    filterByColumn: true,
    filterable: [
        'permit',
        'carrier',
        'reg_number',
        // 'truck_model',
        'polygon',
        // 'checked_in',
        'invoice_num',
    ]
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
        '/akt?print=true&visit_id=' + visit_id,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
};

let after = null;
let before = null;
const resetData = () => store.dispatch('VisitsModule/update_garbage_trucks', { after, before });

const interval = ref([]);
const bind_data = async () => {
    if (store.state.VisitsModule.garbage_truck_visits.length != 0) {
        interval.value = [
            Math.min(...store.state.VisitsModule.garbage_truck_visits.map(o => o.checked_out)),
            Math.max(...store.state.VisitsModule.garbage_truck_visits.map(o => o.checked_out))
        ]
        return
    };

    var now = new Date();
    now.setHours(0, 0, 0, 0);
    before = now.valueOf(); //(new Date(now.setDate(0))).setHours(23, 59, 59, 0);
    after = now.setHours(23, 59, 59, 0);
    interval.value = [after, before];
    resetData();
};

const excel_columns = () => {
    return {
        'Пропуск': 'permit',
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
    for (var row of store.state.VisitsModule.garbage_truck_visits) {
        items.push({
            permit: row.permit,
            carrier: row.carrier,
            reg_number: row.reg_number,
            truck_model: row.truck_model,
            polygon: row.polygon,
            checked_in: row.checked_in.toLocaleString('ru'),
            brutto: row.brutto,
            tara: row.tara,
            netto: row.netto,
            invoice_num: row.invoice_num,
            destination: row.destination,
            driver_name: row.driver_name,
        })
    }
    return items;
};

onMounted(
    bind_data(),
);
const change = (x) => {
    if (x.length == 2) {
        after = x[0].setHours(0, 0, 0, 0)
        before = x[1].setHours(23, 59, 59, 0)
        resetData();
    }
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
                changed_visits.value = set_netto(table.value.filteredData, result.value)
                for (let visit of changed_visits.value) {
                    let i = store.state.VisitsModule.garbage_truck_visits.findIndex((v) => v.id === visit.id)

                    if (i === -1) continue

                    store.state.VisitsModule.garbage_truck_visits[i] = visit
                }
            };
            continue;
        };

    };
};
const saveNettoChanges = () => {
    let data = []
    for (let visit of changed_visits.value) {
        data.push({
            id: visit.id,
            weight_in: visit.weight_in,
            weight_out: visit.weight_out,
        })
    };
    store.dispatch('VisitsModule/bulk_tonars_update', data)
        .then((res) => {
            if (res.data.success) {
                new window.Swal('Сохранено!', 'Данные успешно сохранены.', 'success');
                resetData();
            }
        })
        .catch((error) => new window.Swal('Ошибка!', error.message, 'error'));
};
const bulkPrintAkt = () => {
    store.dispatch('VisitsModule/setAkts', table.value.filteredData);
    let winPrint = window.open(
        '/doc/bulk_akt?print=true', 'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
}

</script>
<style>
.table .actions .print:hover {
    color: #1abc9c;
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
                <h6 class="mb-0 me-2">Данные&nbspза:</h6>
                <flat-pickr v-model="interval" :config="{ dateFormat: 'd.m.Y', mode: 'range' }"
                    class="form-control flatpickr active me-4 width-100 text-center" style="width: 18em; height: 2.5em;"
                    @on-change="change"></flat-pickr>
                <vue3-json-excel v-show="store.state.AuthModule.credentials.user_role === 'Супервайзер'"
                    class="btn btn-primary me-4" name="Визиты мусоровозов.xls" :fields="excel_columns()"
                    :json-data="excel_items()">Выгрузить&nbspв&nbspExcel</vue3-json-excel>
            </div>
        </teleport>

        <div class="row layout-top-spacing">
            <div v-show="store.state.VisitsModule.garbage_truck_visits.length > 0 && store.state.AuthModule.credentials.user_role === 'Супервайзер'"
                class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12 layout-spacing pb-4">
                <div class="widget widget-statistics">
                    <div class="widget-heading pb-0">
                        <h5>Статистика</h5>
                        <div class="task-action">
                            <div class="mb-4 me-2 custom-dropdown btn-group">
                                <a class="btn dropdown-toggle btn-icon-only" href="#" role="button" id="pendingTask"
                                    data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <svg xmlns="http://www.w3.org/2000/svg" style="width: 24px; height: 24px" width="24"
                                        height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                        stroke-linecap="round" stroke-linejoin="round"
                                        class="feather feather-more-horizontal">
                                        <circle cx="12" cy="12" r="1"></circle>
                                        <circle cx="19" cy="12" r="1"></circle>
                                        <circle cx="5" cy="12" r="1"></circle>
                                    </svg>
                                </a>
                                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="pendingTask">
                                    <li>
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
                                    <li class="mt-3 text-danger">
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
                        <div class="row">
                            <div class="col-3">
                                <div class="w-detail">
                                    <p class="w-title">Всего визитов (Кир. / Лен. / Калач.)</p>
                                    <p class="w-stats">{{ table ? table.filteredData.length.toLocaleString('ru') : 0 }} (
                                        {{ table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Кировский' ? 1 : 0), 0
                                        ).toLocaleString('ru') : 0 }} /
                                        {{ table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Ленинский' ? 1 : 0), 0
                                        ).toLocaleString('ru') : 0 }} /
                                        {{ table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Калачинский' ? 1 : 0), 0
                                        ).toLocaleString('ru') : 0 }}
                                        )
                                    </p>
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="w-detail">
                                    <p class="w-title">Общее нетто (Кир. / Лен. / Калач.), кг</p>
                                    <p class="w-stats">
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + visit.netto, 0) : 0).toLocaleString('ru') }} (
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Кировский' ? visit.netto : 0), 0
                                        ) : 0).toLocaleString('ru') }} /
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Ленинский' ? visit.netto : 0), 0
                                        ) : 0).toLocaleString('ru') }} /
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Калачинский' ? visit.netto : 0), 0
                                        ) : 0).toLocaleString('ru') }}
                                        )
                                    </p>
                                </div>
                            </div>
                            <div class="col-2">
                                <div class="w-detail">
                                    <p class="w-title">Мин. нетто, кг</p>
                                    <p class="w-stats">
                                        {{ Math.min(...(table ? table.filteredData.map(o => o.netto) :
                                            [])).toLocaleString('ru') }}
                                    </p>
                                </div>
                            </div>
                            <div class="col-2">
                                <div class="w-detail">
                                    <p class="w-title">Среднее нетто, кг</p>
                                    <p class="w-stats">
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + visit.netto / table.filteredData.length, 0) :
                                            0).toLocaleString('ru') }}
                                    </p>
                                </div>
                            </div>
                            <div class="col-2">
                                <div class="w-detail">
                                    <p class="w-title">Макс. нетто, кг</p>
                                    <p class="w-stats">
                                        {{ Math.max(...(table ? table.filteredData.map(o => o.netto) :
                                            [])).toLocaleString('ru') }}
                                    </p>
                                </div>
                            </div>
                        </div>
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
                            <template #print="props">
                                <div class="actions text-center">
                                    <a href="javascript:;" class="print" @click="printAkt(props.row.id)">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round" class="feather feather-printer me-3">
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
                    <div class="row mb-3">
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
                </div>
                <div class="modal-footer">
                    <button :disabled="item.is_deleted" type="button" class="btn btn-danger me-auto"
                        @click.prevent="deleteVisit">Удалить</button>
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Отмена</button>
                    <div class="btn-group custom-dropdown" role="group">
                        <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown"
                            aria-haspopup="true" aria-expanded="false">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-printer me-3">
                                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                                <rect x="6" y="14" width="12" height="8"></rect>
                            </svg>
                            Печать
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
                    <button type="button" class="btn btn-primary" @click.prevent="updateVisit">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>
    <visitDetails :item="item" :isOpen="isOpen" @closed="closeDetails" @deleted="deleteItem" @print_akt="printAkt">
    </visitDetails>
</template>
