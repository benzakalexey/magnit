<script setup>
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import visitDetails from '@/components/magnit/forms/visitDetails';

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
    'truck_model',
    'polygon',
    'checked_in',
    // 'brutto',
    // 'tara',
    // 'netto',
    'invoice_num',
    'print'
]);

if (store.state.AuthModule.credentials.user_role === 'Супервайзер') {
    columns.value.push('actions')
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
const table_option = ref({
    perPage: 500,
    perPageValues: [500, 1000, 2000, 5000, 10000],
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
        'checked_in',
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
    },
    resizableColumns: false,
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


const interval = ref([]);
const bind_data = async () => {
    if (store.state.VisitsModule.garbage_truck_visits.length != 0) {
        interval.value = [
            Math.min(...store.state.VisitsModule.garbage_truck_visits.map(o => o.checked_in)),
            Math.max(...store.state.VisitsModule.garbage_truck_visits.map(o => o.checked_in))
        ]
        return
    };

    var now = new Date();
    now.setHours(0, 0, 0, 0);
    var before = (new Date(now.setDate(0))).setHours(23, 59, 59, 0);
    var after = now.setDate(1);
    interval.value = [after, before]
    store.dispatch('VisitsModule/update_garbage_trucks', { after, before });
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
        var after = x[0].setHours(0, 0, 0, 0)
        var before = x[1].setHours(23, 59, 59, 0)
        store.dispatch('VisitsModule/update_garbage_trucks', { after, before });
    }
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
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="store.state.VisitsModule.garbage_truck_visits" :columns="columns"
                            :options="table_option">
                            <template #checked_in="props">
                                <div :data_sort="props.row.checked_in">{{ props.row.checked_in.toLocaleString('ru') }}</div>
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
    <visitDetails :item="item" :isOpen="isOpen" @closed="closeDetails" @deleted="deleteItem" @print_akt="printAkt">
    </visitDetails>
</template>
