<script setup>
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import addVisit from '@/components/magnit/forms/addVisit';
import visitDetails from '@/components/magnit/forms/visitDetails';

const store = useStore();
useMeta({ title: 'Полигон' });

const columns = ref([
    // 'invoice_num',
    'permit',
    'reg_number',
    'carrier',
    'truck_model',
    'checked_in',
    'weight_in',
    'tonar',
    'status',
    'actions',
]);
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
    perPage: 15,
    perPageValues: [15, 50, 100],
    skin: 'table table-hover',
    headings: {
        tonar: '',
        invoice_num: 'Номер накладной',
        permit: 'Пропуск',
        reg_number: 'Номер',
        carrier: 'Контрагент',
        truck_model: 'Марка ТС',
        truck_type: 'Тип ТС',
        checked_in: 'Въезд',
        weight_in: 'Вес въезда, кг',
        status: 'Статус',
        actions: '',
    },
    columnsClasses: { actions: 'actions text-center' },
    sortable: [
        'permit',
        'reg_number',
        'carrier',
        'truck_model',
        'checked_in',
        'weight_in',
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
const tonar = {
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
const getOut = (data) => {
    store.dispatch('VisitsModule/finish', {
        visit_id: data.visit_id,
        weight_out: data.out_weight,
        driver_id: data.driver,
        contract_id: data.direction,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Успешно!', 'Автомобиль выехал.', 'success');
            store.dispatch('VisitsModule/update');
        }
        if (data.tonar) {
            printTonarPack(data.visit_id);
        }
    })
    .catch((error) => new window.Swal('Ошибка!', error.data, 'error'))
};

const bind_data = async() => {
    while (true) {
        store.dispatch('VisitsModule/update');
        await new Promise(r => setTimeout(r, 120_000));
    }  
};

onMounted(
    bind_data(),
);

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
                                    <span>{{ store.state.VisitsModule.polygon }}</span>
                                </li>
                            </ol>
                        </nav>
                    </div>
                </li>
            </ul>
        </teleport>

        <div class="row layout-top-spacing">
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="store.state.VisitsModule.visits" :columns="columns" :options="table_option">
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

    <addVisit></addVisit>
    <visitDetails :item="item" :isOpen="isOpen" @closed="closeDetails" @deleted="deleteItem" @get_out="getOut"
        @print_invoice="printInvoice" @print_akt="printAkt" @print_pack="printTonarPack">
    </visitDetails>
</template>
