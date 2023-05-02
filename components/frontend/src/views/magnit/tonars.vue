<script setup>
import '@/assets/sass/widgets/widgets.scss';
import { onMounted, ref, computed } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { Modal } from 'bootstrap';
import { PolygonsAPI } from '@/api/polygonsAPI'
import { DriversAPI } from '@/api/driversAPI'
import ApexChart from 'vue3-apexcharts';

//flatpickr
import flatpickr from 'flatpickr';
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import '@/assets/sass/forms/custom-flatpickr.css';

import { Russian } from "flatpickr/dist/l10n/ru.js"

flatpickr.localize(Russian); // default locale is now Russian

const store = useStore();
useMeta({ title: 'Тонары' });

const columns = ref([
    'permit',
    'carrier',
    'reg_number',
    // 'truck_model',
    'polygon',
    'checked_in',
    'brutto',
    'tara',
    'netto',
    'invoice_num',
    'destination',
    'driver_name',
]);

if (store.state.AuthModule.credentials.user_role !== 'Аналитик тонаров') {
    columns.value.push('actions')
}
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
const table_option = ref({
    perPage: 50,
    perPageValues: [50, 500, 1000, 2000],
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
        'checked_in',
    ],
    sortIcon: {
        base: 'sort-icon-none',
        up: 'sort-icon-asc',
        down: 'sort-icon-desc',
    },
    filterable: [
        'permit',
        'carrier',
        'reg_number',
        'polygon',
        'invoice_num',
        'destination',
        'driver_name',
    ],
    filterByColumn: true,
    pagination: { nav: 'scroll', chunk: 5 },
    texts: {
        count: 'С {from} по {to} из {count}',
        filter: '',
        filterPlaceholder: 'Поиск...',
        limit: 'Показать:',
        noResults: "Нет данных",
        filterBy: "Фильтр по {column}",
    },
    resizableColumns: false,
});
const printTonarPack = (visit_id) => {
    let winPrint = window.open(
        '/doc/tonar_pack?print=true&visit_id=' + visit_id,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
};
const printInvoice = (visit_id) => {
    let winPrint = window.open(
        '/invoice?print=true&visit_id=' + visit_id,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
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
const updateVisit = () => {
    console.log(interval.value.length)
    store.dispatch('VisitsModule/update_tonar_visit', {
        weight_in: visitDetails.value.weight_in,
        weight_out: visitDetails.value.weight_out,
        visit_id: visitDetails.value.id,
        driver_id: visitDetails.value.driver_id,
        contract_id: visitDetails.value.contract_id,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Успешно!', 'Данные сохранены.', 'success');
            detailModal.hide();
            store.dispatch('VisitsModule/update_tonars', { after, before });
        }
    }).catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};

const interval = ref([]);
const bind_data = () => {
    if (store.state.VisitsModule.tonar_visits.length != 0) {
        interval.value = [
            Math.min(...store.state.VisitsModule.tonar_visits.map(o => o.checked_in)),
            Math.max(...store.state.VisitsModule.tonar_visits.map(o => o.checked_in))
        ]
        return
    };

    var now = new Date();
    now.setHours(0, 0, 0, 0);
    before = now.valueOf(); //(new Date(now.setDate(0))).setHours(23, 59, 59, 0);
    after = now.setDate(now.getDate() - 3);
    interval.value = [after, before]
    // store.dispatch('VisitsModule/update_tonars', { after, before });
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
        'Номер ТН': 'invoice_num',
        'Направление': 'destination',
        'Водитель': 'driver_name',
    };
};
const excel_items = () => {
    const rows = table.value ? table.value.filteredData : store.state.VisitsModule.tonar_visits
    let items = []
    for (var row of rows) {
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
    }
);
const visitDetailsModal = ref(null)
const drivers = ref([]);
const directions = ref([]);
const initDetailsModal = () => {
    detailModal = new Modal(visitDetailsModal.value)
    visitDetailsModal.value.addEventListener("hidden.bs.modal", onHidden)
};
const openDetails = (i) => {
    DriversAPI.get(i.contragent_id).then((ref) => (drivers.value = ref.data));
    PolygonsAPI.get_directions(i.polygon_id).then((ref) => (directions.value = ref.data));
    visitDetails.value = i;
    console.log(i)
    detailModal.show();
};
const onHidden = () => {
    drivers.value = [];
    directions.value = [];
};
onMounted(
    () => {
        bind_data();
        initDetailsModal();
    }
);
const change = (x) => {
    if (x.length == 2) {
        after = x[0].setHours(0, 0, 0, 0)
        before = x[1].setHours(23, 59, 59, 0)
        store.dispatch('VisitsModule/update_tonars', { after, before });
    }
};
</script>

<template>
    <div class="layout-px-spacing">
        <teleport to="#breadcrumb">
            <ul class="navbar-nav flex-row">
                <li>
                    <div class="page-header">
                        <nav class="breadcrumb-one" aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item active" aria-current="page">
                                    <span>{{ $t('tonars') }}</span>
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
                <vue3-json-excel class="btn btn-primary me-4" name="Визиты тонаров.xls" :fields="excel_columns()"
                    :json-data="excel_items()">Выгрузить&nbspв&nbspExcel</vue3-json-excel>
            </div>
        </teleport>
        <div class="row layout-top-spacing">
            <div v-show="store.state.VisitsModule.tonar_visits.length > 0"
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
                                        <a href="javascript:void(0);" class="dropdown-item">
                                            Изменить
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
                                    <p class="w-title">Всего визитов (Кир. / Лен.)</p>
                                    <p class="w-stats">{{ table ? table.filteredData.length : 0 }} (
                                        {{ table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Кировский' ? 1 : 0), 0
                                        ) : 0 }} /
                                        {{ table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Ленинский' ? 1 : 0), 0
                                        ) : 0 }}
                                        )
                                    </p>
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="w-detail">
                                    <p class="w-title">Общее нетто (Кир. / Лен.), тонн</p>
                                    <p class="w-stats">
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + visit.netto, 0) : 0) / 1000 }} (
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Кировский' ? visit.netto : 0), 0
                                        ) : 0) / 1000 }} /
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + (visit.polygon == 'Ленинский' ? visit.netto : 0), 0
                                        ) : 0) / 1000 }}
                                        )
                                    </p>
                                </div>
                            </div>
                            <div class="col-2">
                                <div class="w-detail">
                                    <p class="w-title">Мин. нетто, тонн</p>
                                    <p class="w-stats">
                                        {{ Math.min(...(table ? table.filteredData.map(o => o.netto) : [])) / 1000 }}
                                    </p>
                                </div>
                            </div>
                            <div class="col-2">
                                <div class="w-detail">
                                    <p class="w-title">Среднее нетто, тонн</p>
                                    <p class="w-stats">
                                        {{ Math.round(table ? table.filteredData.reduce(
                                            (acc, visit) => acc + visit.netto / table.filteredData.length, 0) : 0) /
                                            1000 }}
                                    </p>
                                </div>
                            </div>
                            <div class="col-2">
                                <div class="w-detail">
                                    <p class="w-title">Макс. нетто, тонн</p>
                                    <p class="w-stats">
                                        {{ Math.max(...(table ? table.filteredData.map(o => o.netto) : [])) / 1000 }}
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
                        <v-client-table :data="store.state.VisitsModule.tonar_visits" :columns="columns"
                            :options="table_option" ref="table">
                            <template #checked_in="props">
                                <div :data_sort="props.row.checked_in">{{ props.row.checked_in.toLocaleString('ru') }}</div>
                            </template>
                            <template #status="props">
                                <div v-html="statuses[props.row.status]"></div>
                            </template>
                            <template #tonar="props">
                                <div v-html="tonar[props.row.tonar]"></div>
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
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Отмена</button>
                    <button type="button" class="btn btn-primary" @click.prevent="updateVisit">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" ref="weightCorrectorModal" tabindex="-1" role="dialog"
        aria-labelledby="weightCorrectorModalLable" aria-hidden="true">
        <div class="modal-dialog modal" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="weightCorrectorModalLable">Изменить вес</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <form>
                                <div>
                                    <p>Use input <code>type="range"</code>.</p>
                                    <input type="range" class="form-range" required />
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Отмена</button>
                    <button type="button" class="btn btn-primary" @click.prevent="updateVisit">
                        Изменить
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
