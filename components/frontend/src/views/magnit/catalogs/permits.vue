<script setup>
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import addVisit from '@/components/magnit/forms/addVisit'
import { useStore } from 'vuex';
import AddVehicle from '@/components/magnit/forms/addVehicle';

useMeta({ title: 'Пропуска' });

const store = useStore();
const isOpen = ref(null);
const item = ref(null);
const columns = ref(
    [
        'permit_num',
        'vehicle_num',
        'vehicle_type',
        'vehicle_mark',
        'contragent',
        'expired_at',
        'days_before_exp',
        'actions',
    ]
);

// permit_num
// vehicle_num
// vehicle_type
// vehicle_mark
// contragent
// expired_at
// is_active
// days_before_exp
// vehicle_mark
// vehicle_mark
// min_weight
// max_weight

const table_option = ref({
    perPage: 20,
    perPageValues: [5, 10, 20, 50],
    skin: 'table table-hover',
    headings: {
        'permit_num': 'Пропуск',
        'vehicle_num': 'Рег. номер ТС',
        'vehicle_type': 'Тип ТС',
        'vehicle_mark': 'Мартка ТС',
        'contragent': 'Контрагент',
        'expired_at': 'Истекает',
        'days_before_exp': 'До истечения, дней',
        'actions': '',
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

onMounted(
    store.dispatch('PermitsModule/get_all'),
);

const openDetails = (i) => {
    item.value = i;
    isOpen.value = !isOpen.value;
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
                                <li class="breadcrumb-item">{{ $t('catalog') }}</li>
                                <li class="breadcrumb-item active" aria-current="page"><span>{{ $t('permits') }}</span>
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
                        <v-client-table :data="store.state.PermitsModule.permits" :columns="columns"
                            :options="table_option">
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


    <addVehicle></addVehicle>


</template>
