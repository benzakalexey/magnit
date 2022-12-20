<script setup>
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import addVisit from '@/components/magnit/forms/addVisit';
import visitDetails from '@/components/magnit/forms/visitDetails';

const store = useStore();
useMeta({ title: 'Полигон' });

const columns = ref([
    'permit_num',
    'reg_num',
    'contragent_name',
    'vehicle_mark',
    'vehicle_type',
    'weight_in',
    'weight_out',
    'loading_weight',
    'checked_in',
    'checked_out',
    'status',
    'actions',
]);
const isOpen = ref(null);
const item = ref(
    {
        permit_num: '',
        reg_num: '',
        contragent_name: '',
        vehicle_mark: '',
        vehicle_type: '',
        weight_in: '',
        weight_out: '',
        loading_weight: '',
        checked_in: '',
        checked_out: '',
        status: '',
    }
);
const items = ref([]);
const table_option = ref({
    perPage: 20,
    perPageValues: [5, 10, 20, 50],
    skin: 'table table-hover',
    headings: {
        permit_num: 'Пропуск',
        reg_num: 'Номер',
        contragent_name: 'Контрагент',
        vehicle_mark: 'Марка ТС',
        vehicle_type: 'Тип ТС',
        weight_in: 'Вес заезда',
        weight_out: 'Вес выезда',
        loading_weight: 'Вес загрузки',
        checked_in: 'Въезд',
        checked_out: 'Выезд',
        status: 'Статус',
        actions: '',
    },
    columnsClasses: { actions: 'actions text-center' },
    sortable: [],
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

const openDetails = (i) => {
    item.value = i;
    isOpen.value = !isOpen.value;
};
const closeDetails = () => {
    isOpen.value = !isOpen.value;
};
const deleteItem = (id, reason) => {
    store.dispatch('VisitsModule/delete', {
        id: id,
        reason: reason,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Удалено!', 'Данные помечены как удаленные.', 'success')
        }
    }).catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
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
                        <v-client-table :data="store.state.VisitsModule.visits" :columns="columns"
                            :options="table_option">
                            <template #status="props">
                                <div v-html="statuses[props.row.status]"></div>
                            </template>
                            <template #actions="props">
                                <div class="actions text-center">
                                    <a href="javascript:;" class="btn btn-primary btn-sm"
                                        @click="openDetails(props.row)">Открыть</a>
                                </div>
                            </template>
                            <template #salary="props"> ${{ props.row.salary }} </template>
                        </v-client-table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <addVisit></addVisit>
    <visitDetails :item="item" :isOpen="isOpen" @closed="closeDetails" @deleted="deleteItem">
    </visitDetails>
</template>
