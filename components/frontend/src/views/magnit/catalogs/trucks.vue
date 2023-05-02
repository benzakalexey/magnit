<script setup>
import '@/assets/sass/visits/visits.scss';
import { onMounted, ref, computed, nextTick } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useVuelidate } from '@vuelidate/core'
import { helpers, required, numeric, minValue, minLength, maxLength } from '@vuelidate/validators';
import { Modal } from 'bootstrap';
import { EventBus } from 'v-tables-3';

//flatpickr
import flatpickr from 'flatpickr';
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import '@/assets/sass/forms/custom-flatpickr.css';

import { Russian } from "flatpickr/dist/l10n/ru.js"

flatpickr.localize(Russian); // default locale is now Russian

const store = useStore();
useMeta({ title: 'Автомобили' });

const columns = ref([
    'permit',
    'permission_owner',
    'started_at',
    'expired_at',
    'days_before_exp',
    'reg_number',
    'truck_model',
    'tonar',
    'actions',
]);
const isOpen = ref(null);
const tonar = {
    true: `<span class="badge inv-status outline-badge-warning">Tонар</span>`,
    false: '',
};
const table_option = ref({
    perPage: 15,
    perPageValues: [15, 50, 100],
    skin: 'table table-hover',
    headings: {
        reg_number: 'Рег. номер',
        passport: 'Номер СТС',
        manufactured_at: 'Год выпуска',
        truck_model: 'Марка',
        truck_type: 'Тип ТС',
        tara: 'Масса пустого',
        tonar: '',
        max_weight: 'Макс. масса',
        body_volume: 'Объем кузова',
        permit: 'Пропуск',
        permission_owner: 'Контрагент',
        started_at: 'Выдан',
        expired_at: 'Истекает',
        days_before_exp: 'Осталось, дн.',
        actions: '',
    },
    columnsClasses: { actions: 'actions text-center' },
    sortable: [
        'permit',
        'permission_owner',
        'manufactured_at',
        'truck_type',
        'tara',
        'max_weight',
        'body_volume',
        'started_at',
        'expired_at',
        'days_before_exp',
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
        noResults: 'Нет данных',
    },
    resizableColumns: false,
    customFilters: [
        {
            name: 'expiredAt',
            callback: (row, days) => 0 < row.days_before_exp && row.days_before_exp < days,
        },
        {
            name: 'all',
            callback: (row, query) => true,
        },
    ],
});

const closeDetails = () => {
    isOpen.value = false;
};

// new Truck form
const model = ref(null);
const reg_number = ref(null);
const type = ref(null);
const tara = ref(null);
const max_weight = ref(null);
const production_year = ref(null);
const body_volume = ref(null);
const permit_exp = ref(null);
const carrier = ref(null);
const trailer = ref(null);
const is_tonar = ref(false);
const closeNewForm = () => {
    isOpen.value = false;
    clearNewForm();
}
const clearNewForm = () => {
    model.value = null
    reg_number.value = null
    type.value = null
    tara.value = null
    max_weight.value = null
    production_year.value = null
    body_volume.value = null
    permit_exp.value = null
    carrier.value = null
    trailer.value = null
    is_tonar.value = false
}

const createTruck = () => {
    const data = {
        model: model.value,
        reg_number: reg_number.value.toUpperCase(),
        type: type.value,
        tara: tara.value,
        max_weight: max_weight.value,
        production_year: production_year.value,
        body_volume: body_volume.value,
        permit_exp: strToDate(permit_exp.value),
        carrier: carrier.value,
        trailer: trailer.value,
        is_tonar: is_tonar.value,
    }
    store.dispatch('TrucksModule/add', data)
        .then((res) => {
            if (res.data.success) {
                new window.Swal('Успешно!', 'Автомобиль создан.', 'success');
                closeNewForm();
                store.dispatch('TrucksModule/update');
            }
        })
        .catch((error) => new window.Swal('Ошибка!', error.data, 'error'))
};

const reg_number_validator = helpers.regex(/^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}$/ui)
const pickr_conf = ref({
    dateFormat: 'd.m.Y',
});
const strToDate = (dateString) => {
    const [day, month, year] = dateString.split('.');
    return new Date([month, day, year].join('/'));
};

const rules = computed(() => ({
    reg_number: {
        required,
        pattern: reg_number_validator,
        $lazy: true,
        $autoDirty: true
    },
    tara: {
        required,
        numeric,
        minValue: minValue(0),
        $lazy: true,
        $autoDirty: true
    },
    max_weight: {
        required,
        numeric,
        minValue: minValue(0),
        $lazy: true,
        $autoDirty: true
    },
    production_year: {
        required,
        numeric,
        minValue: minValue(1970),
        minLength: minLength(4),
        maxLength: maxLength(4),
        $lazy: true,
        $autoDirty: true
    },
    body_volume: {
        required,
        numeric,
        minValue: minValue(0),
        $lazy: true,
        $autoDirty: true
    },
    permit_exp: {
        required,
        $lazy: true,
        $autoDirty: true
    },
}));

const v$ = useVuelidate(rules, {
    reg_number,
    tara,
    max_weight,
    production_year,
    body_volume,
    permit_exp,
});

// Details Modal

let detailModal = null;

const truckDetails = ref(
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
const truckDetailsModal = ref(null)
const initDetailsModal = () => {
    detailModal = new Modal(truckDetailsModal.value)
    truckDetailsModal.value.addEventListener("hidden.bs.modal", onHidden)
};
const partnerIdByName = (name) => {
    return store.state.PartnersModule.partners[
        store.state.PartnersModule.partners.findIndex((i) => i['short_name'] == name)
    ].id
};
const trailerIdByNum = (name) => {
    var index = store.state.TrucksModule.trailers.findIndex((i) => i['reg_number'] == name)
    if (index !== -1) {
        return store.state.TrucksModule.trailers[index].id
    }

};
const openDetails = (i) => {
    truckDetails.value = i;

    carrier.value = partnerIdByName(i.permission_owner)
    trailer.value = trailerIdByNum(i.trailer)
    is_tonar.value = i.tonar
    permit_exp.value = i.expired_at


    store.dispatch(
        'PermitsModule/get_history', { num: truckDetails.value.permit }
    ).then(() => detailModal.show())
};
const onHidden = () => {
    trailer.value = null;
    carrier.value = null;
    permit_exp.value = null;
    is_tonar.value = false;
};

const updatePermit = () => {
    const data = {
        permit: truckDetails.value.permit,
        permit_exp: strToDate(permit_exp.value),
        carrier: carrier.value,
        trailer: trailer.value,
        is_tonar: is_tonar.value,
        truck_type: truckDetails.value.truck_type,
        tara: truckDetails.value.tara,
        max_weight: truckDetails.value.max_weight,
        body_volume: truckDetails.value.body_volume,
    };
    store.dispatch('PermitsModule/add_permission', data)
        .then((res) => {
            if (res.data.success) {
                new window.Swal('Успешно!', 'Пропуск обновлен.', 'success');
                detailModal.hide();
                store.dispatch('TrucksModule/update');
            };
        })
        .catch((error) => new window.Swal('Ошибка!', error.data, 'error'))
};

onMounted(
    () => {
        // Update Data
        store.dispatch('TrucksModule/update').then(() => {
            store.dispatch('TrucksModule/update_trailers');
            store.dispatch('PartnersModule/update');
            store.dispatch('TrucksModule/update_models');
            store.dispatch('TrucksModule/update_types');
        })
        // Init modal
        initDetailsModal();
    }
);
const table = ref(null);
const showTable = ref(true);
let clickedExpSoon = ref(false);
const expSoonFilter = () => {
    clickedExpSoon.value = !clickedExpSoon.value;

    if (clickedExpSoon.value) {
        EventBus.emit('vue-tables.filter::expiredAt', 7)
    }
    else {
        showTable.value = !showTable.value;

        nextTick(() => showTable.value = !showTable.value)
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
                                <li class="breadcrumb-item active" aria-current="page"><span>{{ $t('trucks') }}</span></li>
                            </ol>
                        </nav>
                    </div>
                </li>
            </ul>
            <div class="navbar-nav justify-content-end align-items-center">
                <button v-show="store.state.TrucksModule.trucks.reduce((acc, e) => acc +
                    (e.days_before_exp < 7 && e.days_before_exp > 0 ? 1 : 0), 0)" type="button"
                    class="btn me-4" :class="clickedExpSoon ? 'btn-secondary' : 'btn-outline-secondary'" @click="expSoonFilter()">
                    <span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="feather feather-alert-triangle me-2" data-v-5522efca="">
                            <path
                                d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z">
                            </path>
                            <line x1="12" y1="9" x2="12" y2="13"></line>
                            <line x1="12" y1="17" x2="12.01" y2="17"></line>
                        </svg>
                    </span>
                    Скоро истекает
                    <span class="badge badge-danger counter" style="top: -8px; right: -8px;">
                        {{ store.state.TrucksModule.trucks.reduce((acc, e) => acc +
                            (e.days_before_exp < 7 && e.days_before_exp > 0 ? 1 : 0), 0) }}</span>
                </button>
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
                        <v-client-table v-if="showTable" :data="store.state.TrucksModule.trucks" :columns="columns" :options="table_option"
                            ref="table">
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
                            <template #days_before_exp="props">
                                <span v-show="props.row.days_before_exp <= 0"
                                    class="badge inv-status outline-badge-danger">Просрочен</span>
                                <div v-show="props.row.days_before_exp > 0">
                                    {{ props.row.days_before_exp }}
                                </div>
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

        <div class="right-side-modal" :class="{ active: isOpen }">
            <div class="sidbarchat p-3" tag="div">
                <a class="btn-close" href="javascript:;" @click="closeNewForm()"> </a>
                <h5 class="rs-modal-title mb-5">Новый автомобиль</h5>

                <form novalidate>
                    <div class="mb-3">
                        <label for="reg_number" class="col-form-label">Рег. номер ТС</label>
                        <div>
                            <input v-model="reg_number" id="reg_number" type="text" class="form-control" placeholder=""
                                :class="[v$.reg_number.$invalid ? 'is-invalid' : '']" />
                            <div class="invalid-feedback" v-if="v$.reg_number.$error">Введите номер в формате а555аа55(5)
                            </div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="col-form-label" for="out_weight">Марка ТС</label>
                        <select class="form-select form-select" v-model="model">
                            <option selected disabled>Выберите значение</option>
                            <option v-for="model in store.state.TrucksModule.models" :value="model.id">{{ model.name }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="reg_number" class="col-form-label">Масса пустого</label>
                        <div>
                            <input v-model="tara" id="tara" type="number" class="form-control" placeholder=""
                                :class="[v$.tara.$invalid ? 'is-invalid' : '']" />
                            <div class="invalid-feedback" v-if="v$.tara.$error">Недопустимая масса</div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="reg_number" class="col-form-label">Максимальная масса</label>
                        <div>
                            <input v-model="max_weight" id="max_weight" type="number" class="form-control" placeholder=""
                                :class="[v$.max_weight.$invalid ? 'is-invalid' : '']" />
                            <div class="invalid-feedback" v-if="v$.max_weight.$error">Недопустимая масса</div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="col-form-label" for="out_weight">Тип ТС</label>
                        <select class="form-select form-select" v-model="type">
                            <option selected disabled>Выберите значение</option>
                            <option v-for="t in store.state.TrucksModule.types">{{ t }}</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="production_year" class="col-form-label">Год выпуска</label>
                        <div>
                            <input v-model="production_year" id="production_year" type="number" class="form-control"
                                placeholder="" :class="[v$.production_year.$invalid ? 'is-invalid' : '']" />
                            <div class="invalid-feedback" v-if="v$.production_year.$error">Год в формате ГГГГ, например
                                2023.
                            </div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="production_year" class="col-form-label">Объем кузова</label>
                        <div>
                            <input v-model="body_volume" id="body_volume" type="number" class="form-control" placeholder=""
                                :class="[v$.body_volume.$invalid ? 'is-invalid' : '']" />
                            <div class="invalid-feedback" v-if="v$.body_volume.$error">Недопустимый значение</div>
                        </div>
                    </div>
                    <h5 class="rs-modal-title mt-5">Пропуск</h5>
                    <div class="my-3">
                        <label for="permit_exp" class="col-form-label">Действует до</label>
                        <flat-pickr v-model="permit_exp" :config="pickr_conf"
                            class="form-control flatpickr active"></flat-pickr>
                    </div>
                    <div class="mb-3">
                        <label class="col-form-label" for="out_weight">Компания-перевозчик</label>
                        <select class="form-select form-select" v-model="carrier">
                            <option selected disabled>Выберите значение</option>
                            <option v-for="p in store.state.PartnersModule.partners" :value="p.id">{{ p.short_name }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="col-form-label" for="out_weight">Прицеп</label>
                        <select class="form-select form-select" v-model="trailer">
                            <option selected disabled>Выберите значение</option>
                            <option v-for="t in store.state.TrucksModule.trailers" :value="t.id">{{ t.reg_number }}</option>
                        </select>
                    </div>
                    <div class="m-4">
                        <div class="checkbox-default custom-checkbox">
                            <input type="checkbox" class="custom-control-input" id="chk_default" v-model="is_tonar" />
                            <label class="ps-2 custom-control-label" for="chk_default"> Тонар </label>
                        </div>
                    </div>
                    <button :disabled="v$.$invalid" @click.prevent="createTruck" class="btn btn-primary my-4">
                        Добавить
                    </button>
                </form>

            </div>
        </div>


        <div class="modal fade" ref="truckDetailsModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-xl" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Данные транспортного средства</h5>
                        <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                            class="btn-close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-4">
                                <form>
                                    <div class="mb-3">
                                        <label class="col-form-label" for="reg_num">Рег. номер</label>
                                        <input v-model="truckDetails.reg_number" type="text" readonly="true"
                                            class="form-control" id="reg_num" />
                                    </div>
                                    <div class="mb-3">
                                        <label class="col-form-label" for="permit">Пропуск</label>
                                        <input v-model="truckDetails.permit" type="text" readonly="true"
                                            class="form-control" id="permit" />
                                    </div>
                                    <div class="mb-3">
                                        <label class="col-form-label" for="truck_model">Модель ТС</label>
                                        <input v-model="truckDetails.truck_model" type="text" readonly="true"
                                            class="form-control" id="truck_model" />
                                    </div>
                                    <div class="mb-3">
                                        <label class="col-form-label" for="truck_type">Тип ТС</label>
                                        <select class="form-select form-select" v-model="truckDetails.truck_type">
                                            <option selected disabled>Выберите значение</option>
                                            <option v-for="t in store.state.TrucksModule.types">{{ t }}</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label class="col-form-label" for="tara">Вес пустого</label>
                                        <input v-model="truckDetails.tara" type="number" class="form-control" id="tara" />
                                    </div>
                                    <div class="mb-3">
                                        <label class="col-form-label" for="max_weight">Макс. масса</label>
                                        <input v-model="truckDetails.max_weight" type="number" class="form-control"
                                            id="max_weight" />
                                    </div>
                                    <div class="mb-3">
                                        <label class="col-form-label" for="body_volume">Объем кузова</label>
                                        <input v-model="truckDetails.body_volume" type="number" class="form-control"
                                            id="body_volume" />
                                    </div>
                                </form>
                            </div>
                            <div class="col-8">
                                <form>
                                    <div class="mb-3">
                                        <label class="col-form-label" for="out_weight">Компания-перевозчик</label>
                                        <select class="form-select form-select" v-model="carrier">
                                            <option selected disabled>Выберите значение</option>
                                            <option v-for="p in store.state.PartnersModule.partners" :value="p.id">{{
                                                p.short_name }}
                                            </option>
                                        </select>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <label for="permit_exp" class="col-form-label">Действует до</label>
                                            <flat-pickr v-model="permit_exp" :config="pickr_conf"
                                                class="form-control flatpickr active"></flat-pickr>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="col-form-label" for="out_weight">Прицеп</label>
                                            <select class="form-select form-select" v-model="trailer">
                                                <option selected disabled>Выберите значение</option>
                                                <option v-for="t in store.state.TrucksModule.trailers" :value="t.id">{{
                                                    t.reg_number }}</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="m-4">
                                        <div class="checkbox-default custom-checkbox">
                                            <input type="checkbox" class="custom-control-input" id="chk_default"
                                                v-model="is_tonar" />
                                            <label class="ps-2 custom-control-label" for="chk_default"> Тонар </label>
                                        </div>
                                    </div>
                                </form>
                                <div class="table-responsive">
                                    <label class="col-form-label">История пропуска</label>
                                    <table role="table" aria-busy="false" aria-colcount="5"
                                        class="table table-hover table-bordered" id="__BVID__415">
                                        <thead role="rowgroup">
                                            <tr role="row">
                                                <th role="columnheader" scope="col" aria-colindex="1">
                                                    <div>Контрагент</div>
                                                </th>
                                                <th role="columnheader" scope="col" aria-colindex="2">
                                                    <div>Тонар</div>
                                                </th>
                                                <th role="columnheader" scope="col" aria-colindex="3">
                                                    <div>Выдан</div>
                                                </th>
                                                <th role="columnheader" scope="col" aria-colindex="4">
                                                    <div>Истекает</div>
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody role="rowgroup">
                                            <tr v-for="item in store.state.PermitsModule.permit_histoty" role="row">
                                                <td aria-colindex="1" role="cell">{{ item.contragent_name }}</td>
                                                <td aria-colindex="2" role="cell">
                                                    <span v-show="item.is_tonar"
                                                        class="badge inv-status outline-badge-warning">Tонар</span>
                                                </td>
                                                <td aria-colindex="3" role="cell">{{
                                                    item.added_at.toLocaleDateString('ru') }}</td>
                                                <td aria-colindex="4" role="cell">{{
                                                    item.expired_at.toLocaleDateString('ru') }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                                class="flaticon-cancel-12"></i>Отмена</button>
                        <button type="button" class="btn btn-primary" @click.prevent="updatePermit">
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>
