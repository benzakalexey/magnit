<script setup>
import { onMounted, ref, computed } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useVuelidate } from '@vuelidate/core'

const store = useStore();
useMeta({ title: 'Автомобили' });

const columns = ref([
    'permit',
    'started_at',
    'expired_at',
    'permission_owner',
    'days_before_exp',
    'reg_number',
    'truck_model',
    // 'truck_type',
    // 'tara',
    // 'max_weight',
    'actions',
]);
const isOpen = ref(null);
const item = ref(
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
const items = ref([]);
const table_option = ref({
    perPage: 15,
    perPageValues: [15, 50, 100],
    skin: 'table table-hover',
    headings: {
        truck_model: 'Модель ТС',
        reg_number: 'Рег. номер',
        truck_type: 'Тип ТС',
        tara: 'Масса пустого',
        max_weight: 'Макс. масса',
        permit: 'Пропуск',
        permission_owner: 'Контрагент',
        started_at: 'Действует с',
        expired_at: 'Действует до',
        days_before_exp: 'До окончания, дней',
        actions: '',
    },
    columnsClasses: { actions: 'actions text-center' },
    sortable: [
        'permit',
        'started_at',
        'expired_at',
        'permission_owner',
        'days_before_exp',
        'reg_number',
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
const openDetails = (i) => {
    item.value = i;
    isOpen.value = true;
};
const closeDetails = () => {
    isOpen.value = false;
};
const deleteItem = (id, reason) => {
    store.dispatch('TrucksModule/delete', {
        visit_id: id,
        reason: reason,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Удалено!', 'Данные помечены как удаленные.', 'success');
            store.dispatch('TrucksModule/update');
        }
    }).catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};
const printInvoice = (visit_id) => {
    var winPrint = window.open(
        '/invoice?print=true&visit_id=' + visit_id,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
};
const getOut = (data) => {
    store.dispatch('TrucksModule/finish', {
        visit_id: data.visit_id,
        weight_out: data.out_weight,
        driver_id: data.driver,
        contract_id: data.direction,
    }).then((res) => {
        if (res.data.success) {
            new window.Swal('Успешно!', 'Автомобиль выехал.', 'success');
            store.dispatch('TrucksModule/update');
        }
        if (data.tonar) printInvoice(data.visit_id);
    }).catch((error) => new window.Swal('Ошибка!', error.data, 'error'))
};

onMounted(
    store.dispatch('TrucksModule/update'),
);

const rules = computed(() => ({
    permit_num: {
        required,
        numeric,
        minLength: minLength(2)
    },
    weight: {
        required,
        numeric,
        minValueRef: minValue(store.state.PermitsModule.check_permit.tara || 0),
        maxValueRef: maxValue(store.state.PermitsModule.check_permit.max_weight * 1.2)
    },
}))

const v$ = useVuelidate(rules, { permit_num, weight })

</script>

<template>
    <div class="layout-px-spacing">
        <teleport to="#breadcrumb">
            <div class="navbar-nav flex-row ms-auto">
                <button type="button" class="btn btn-primary me-4" @click="isOpen = !isOpen">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="feather feather-plus me-2" data-v-02c2cbc4="">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    Новый автомобиль
                </button>
            </div>
        </teleport>

        <div class="row layout-top-spacing">
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="store.state.TrucksModule.trucks" :columns="columns" :options="table_option">
                            <template #started_at="props">
                                <div :data_sort="props.row.started_at">
                                    {{ props.row.started_at ? props.row.started_at.toLocaleDateString('ru') : '-' }}
                                </div>
                            </template>
                            <template #expired_at="props">
                                <div :data_sort="props.row.expired_at">
                                    {{ props.row.expired_at ? props.row.expired_at.toLocaleDateString('ru') : '-' }}
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

        <div class="right-side-modal" :class="{ active: isOpen }">
            <div class="sidbarchat p-3" tag="div">
                <a class="btn-close" href="javascript:;" @click="isOpen = !isOpen"> </a>
                <h5 class="rs-modal-title">Новый автомобиль</h5>

                <form novalidate>
                    <div class="mb-3 pt-5">
                        <label for="permit_num" class="col-form-label">Номер пропуска</label>
                        <div>
                            <input v-model="permit_num" id="permit_num" type="number" class="form-control"
                                placeholder="Номер пропуска" v-on:input="checkPermit($event)"
                                :class="[permit_error ? 'is-invalid' : '']" />
                            <div class="invalid-feedback">Нет данных о пропуске</div>
                        </div>
                    </div>
                    <div class="mb-3 pt-3">
                        <label for="weight" class="col-form-label">Вес въезда</label>
                        <div>
                            <input v-model="weight" id="weight" type="number" class="form-control" placeholder="Вес, кг"
                                v-on:input="checkWeight($event)" :class="[weight_error ? 'is-invalid' : '']" />
                            <div class="invalid-feedback">Недопустимый вес</div>
                        </div>
                    </div>
                    <button
                        :disabled="v$.$invalid || Array(null, 0, undefined).includes(store.state.PermitsModule.check_permit.permit_status)"
                        @click.prevent="createVisit" class="btn btn-primary my-4">
                        Заехать
                    </button>
                </form>

                <div v-show="store.state.PermitsModule.check_permit.reg_number" class="permit-info-list pt-5">
                    <h5 class="rs-modal-title">
                        Пропуск
                        <text v-html="statuses[store.state.PermitsModule.check_permit.permit_status]" />
                    </h5>


                    <ul class="info-block list-inline">
                        <li class="info-block__item">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-camera" data-v-5522efca="">
                                <circle cx="12" cy="13" r="4"></circle>
                            </svg>
                            <!-- Регистрационный номер -->
                            {{ store.state.PermitsModule.check_permit.reg_number }}
                            <span v-show="store.state.PermitsModule.check_permit.is_tonar"
                                class="mx-3 badge inv-status badge-warning">Tонар</span>
                        </li>
                        <li class="info-block__item">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-camera" data-v-5522efca="">
                                <circle cx="12" cy="13" r="4"></circle>
                            </svg>
                            <!-- Марка ТС -->
                            {{ store.state.PermitsModule.check_permit.truck_model }}
                        </li>
                        <li class="info-block__item">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-camera" data-v-5522efca="">
                                <circle cx="12" cy="13" r="4"></circle>
                            </svg>
                            <!-- Контрагент -->
                            {{ store.state.PermitsModule.check_permit.contragent }}
                        </li>
                        <li class="info-block__item">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-camera" data-v-5522efca="">
                                <circle cx="12" cy="13" r="4"></circle>
                            </svg>
                            Масса пустого:
                            {{ store.state.PermitsModule.check_permit.tara }}
                        </li>
                        <li class="info-block__item">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-camera" data-v-5522efca="">
                                <circle cx="12" cy="13" r="4"></circle>
                            </svg>
                            Макс. масса:
                            {{ store.state.PermitsModule.check_permit.max_weight }}
                        </li>
                        <li class="info-block__item">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-camera" data-v-5522efca="">
                                <circle cx="12" cy="13" r="4"></circle>
                            </svg>
                            Истекает:
                            {{ new Date(store.state.PermitsModule.check_permit.expired_at).toLocaleDateString('RU') }}
                        </li>
                    </ul>
                </div>

            </div>
        </div>

    </div>
</template>
