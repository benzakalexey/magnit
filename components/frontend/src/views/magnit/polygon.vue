<script setup>
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import addVisit from '@/components/magnit/forms/addVisit';
import visitDetails from '@/components/magnit/forms/visitDetails';

const store = useStore();
useMeta({ title: 'Полигон' });

const columns = ref([
    'permit',
    'reg_number',
    'carrier',
    'truck_model',
    'checked_in',
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
const items = ref([]);
const table_option = ref({
    perPage: 20,
    perPageValues: [5, 10, 20, 50],
    skin: 'table table-hover',
    headings: {
        tonar: '',
        permit: 'Пропуск',
        reg_number: 'Номер',
        carrier: 'Контрагент',
        truck_model: 'Марка ТС',
        truck_type: 'Тип ТС',
        checked_in: 'Въезд',
        status: 'Статус',
        actions: '',
    },
    columnsClasses: { actions: 'actions text-center' },
    sortable: true,
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
    true: `<span class="badge inv-status badge-warning">Tонар</span>`,
    false: '',
};

const openDetails = (i) => {
    item.value = i;
    isOpen.value = !isOpen.value;
};
const closeDetails = () => {
    isOpen.value = !isOpen.value;
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

const printInvoice = (visit_id) => {
    var winPrint = window.open(
        '/invoice?visit_id=' + visit_id,
        '',
        'left=400,top=200,width=1200,height=800,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;

    function delay(time=1000) {
        return new Promise(resolve => setTimeout(resolve, time));
    }
    delay().then(() => winPrint.print());
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
        if (data.tonar) printInvoice(data.visit_id);
    }).catch((error) => new window.Swal('Ошибка!', error.data, 'error'))
};

onMounted(
    store.dispatch('VisitsModule/update'),
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
                                    <span>Кировский полигон</span>
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
        @print="printInvoice">
    </visitDetails>
</template>
