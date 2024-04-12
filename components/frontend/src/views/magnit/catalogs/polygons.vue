<script setup>
import '@/assets/sass/widgets/widgets.scss';
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { Modal } from 'bootstrap';
import { PolygonsAPI } from '@/api/polygonsAPI';
import '@suadelabs/vue3-multiselect/dist/vue3-multiselect.css';

import { utils, writeFile } from 'xlsx';

//flatpickr
import flatpickr from 'flatpickr';
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import '@/assets/sass/forms/custom-flatpickr.css';

import { Russian } from "flatpickr/dist/l10n/ru.js"

flatpickr.localize(Russian); // default locale is now Russian
const pickr_conf = ref({
    dateFormat: 'd.m.Y',
});

const store = useStore();
useMeta({ title: 'Полигоны' });

const polygons = ref([]);
const polygonsFromData = ref([]);
const polygonRolesFromData = ref([]);
const polygonRoles = ref([]);
const columns = ref([
    'name',
    'address',
    'actions',
]);
const table = ref(null);
const item = ref(
    {
        name: '',
        address: '',
        valid_from: '',
        id: '',
    }
);
const table_option = ref({
    perPage: 10000000,
    perPageValues: [10000000,],
    skin: 'table table-hover',
    headings: {
        name: 'Название',
        address: 'Адрес',
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
        'name',
        'address',
    ],
});
const excel_items = () => {
    const rows = table.value ? table.value.filteredData : store.state.PolygonsModule.polygons
    let items = []
    for (var row of rows) {
        items.push({
            'Фамилия': row.surname,
            'Имя': row.first_name,
            'Отчество': row.patronymic,
            'Телефон': row.phone,
            'Сотрудник': row.is_staff ? 'ДА' : 'НЕТ',
            'Активен': row.is_active ? 'ДА' : 'НЕТ',
            'Полигон': row.polygon,
            'Группа': row.role,
            'Добавил': row.added_by,
            'Добавил': row.added_by,
            'Дата добавления': row.added_at.toLocaleString('ru'),
        })
    }
    return items;
};
const bindData = () => {
    store.dispatch('PolygonsModule/get')
        .then(() => {
            polygonsFromData.value = [...new Set(store.state.PolygonsModule.polygons.map(item => item.polygon))].map(item => ({ text: item }));
            polygonRolesFromData.value = [...new Set(store.state.PolygonsModule.polygons.map(item => item.role))].map(item => ({ text: item }));
        });
    // PolygonsAPI.get_all().then((ref) => (polygons.value = ref.data));
    // PolygonsAPI.get_polygon_roles().then((ref) => (polygonRoles.value = ref.data));
}

// Details Modal

let detailModal = null;
const detailsData = ref(
    {
        polygon_id: null,
        name: null,
        address: null,
        valid_from: null,
        valid_to: null,
        scale_accuracy: null
    }
)
const detailsDataModal = ref(null);
const onHidden = () => { };
const initDetailsModal = () => {
    detailModal = new Modal(detailsDataModal.value)
    detailsDataModal.value.addEventListener("hidden.bs.modal", onHidden)
};
const openDetails = (data) => {
    detailsData.value = data;
    detailModal.show();
};

// New Polygon Modal

let newPolygonModal = null;
const newPolygonData = ref(
    {
        polygon_id: '',
        name: '',
        address: '',
        valid_from: '',
        valid_to: '',
        scale_accuracy: '',
    }
)
const newPolygonModalData = ref(null);
const onHiddenNewPolygonModal = () => { };
const initNewPolygonModal = () => {
    newPolygonModal = new Modal(newPolygonModalData.value)
    newPolygonModalData.value.addEventListener("hidden.bs.modal", onHiddenNewPolygonModal)
};
const openNewForm = () => {
    newPolygonData.value = {
        polygon_id: null,
        phone: '',
        password: '',
        role: null,
        is_staff: true,
        is_active: true,
        surname: '',
        first_name: '',
        patronymic: '',
    };
    newPolygonModal.show();
};
const strToDate = (dateString) => {
    if (dateString === null) {
        return dateString
    }
    const [day, month, year] = dateString.split('.');
    return new Date([month, day, year].join('/'));
};
const save = () => {
    detailsData.value.valid_from = strToDate(detailsData.value.valid_from)
    detailsData.value.valid_to = strToDate(detailsData.value.valid_to)
    PolygonsAPI.update(detailsData.value)
        .then((res) => { if (res.data.success) showMessage('Данные сохранены.') })
        .then(() => store.dispatch('PolygonsModule/get').then(() => detailModal.hide()))
        .catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};
const create = () => {
    newPolygonData.value.valid_from = strToDate(newPolygonData.value.valid_from)
    newPolygonData.value.valid_to = strToDate(newPolygonData.value.valid_to)
    PolygonsAPI.create(newPolygonData.value)
        .then((res) => { if (res.data.success) showMessage('Новый полигон добавлен.') })
        .then(() => store.dispatch('PolygonsModule/get').then(() => newPolygonModal.hide()))
        .catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
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
    utils.book_append_sheet(wb, data, `Полигоны`)
    writeFile(wb, 'Полигоны.xlsx')
};

onMounted(
    () => {
        bindData();
        initDetailsModal();
        initNewPolygonModal();
    }
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
                                <li class="breadcrumb-item">{{ $t('catalog') }}</li>
                                <li class="breadcrumb-item active" aria-current="page">
                                    <span>{{ $t('polygons') }}</span>
                                </li>
                            </ol>
                        </nav>
                    </div>
                </li>
            </ul>
            <div class="navbar-nav d-flex justify-content-end align-items-center">
                <button type="button" class="btn btn-primary me-4"
                    v-on:click="download">Выгрузить&nbspв&nbspExcel</button>
            </div>
        </teleport>
        <div class="row layout-top-spacing">
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="store.state.PolygonsModule.polygons" :columns="columns"
                            :options="table_option" ref="table">
                            <template #afterFilterWrapper>
                                <button type="button" class="btn btn-primary me-4" @click="openNewForm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                        stroke-linejoin="round" class="feather feather-plus me-2" data-v-02c2cbc4="">
                                        <line x1="12" y1="5" x2="12" y2="19"></line>
                                        <line x1="5" y1="12" x2="19" y2="12"></line>
                                    </svg>
                                    Новый полигон
                                </button>
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

    <div class="modal fade" ref="detailsDataModal" tabindex="-1" role="dialog" aria-labelledby="detailsModalLable"
        aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="detailsModalLable">{{ detailsData.name }}</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="address">Адрес</label>
                            <textarea v-model="detailsData.address" type="text" class="form-control" id="address"
                                rows="8" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="scale_accuracy">Точность весов</label>
                            <input v-model="detailsData.scale_accuracy" type="number" class="form-control"
                                id="scale_accuracy" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="valid_from" class="col-form-label">Действует c:</label>
                            <flat-pickr v-model="detailsData.valid_from" :config="pickr_conf"
                                class="form-control flatpickr active" id="valid_from" />
                        </div>
                        <div class="col-md-6">
                            <label for="valid_to" class="col-form-label">Действует до:</label>
                            <flat-pickr v-model="detailsData.valid_to" :config="pickr_conf"
                                class="form-control flatpickr active" id="valid_to" />
                        </div>
                    </div>
                </div>
                <div class="modal-footer mx-2">
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Закрыть</button>
                    <button type="button" class="btn btn-primary" @click.prevent="save">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" ref="newPolygonModalData" tabindex="-1" role="dialog" aria-labelledby="newPolygonModalLable"
        aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="newPolygonModalLable">Новый пользователь</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="new_polygon_name">Наименование</label>
                            <input v-model="newPolygonData.name" type="text" class="form-control"
                                id="new_polygon_name" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="new_polygon_address">Адрес</label>
                            <textarea v-model="newPolygonData.address" type="text" class="form-control"
                                id="new_polygon_address" rows="8" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="new_polygon_scale_accuracy">
                                Точность весов
                            </label>
                            <textarea v-model="newPolygonData.scale_accuracy" type="text" class="form-control"
                                id="new_polygon_scale_accuracy" rows="8" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="new_polygon_valid_from" class="col-form-label">Действует c:</label>
                            <flat-pickr v-model="newPolygonData.valid_from" :config="pickr_conf"
                                class="form-control flatpickr active" id="new_polygon_valid_from" />
                        </div>
                        <div class="col-md-6">
                            <label for="new_polygon_valid_to" class="col-form-label">Действует до:</label>
                            <flat-pickr v-model="newPolygonData.valid_to" :config="pickr_conf"
                                class="form-control flatpickr active" id="new_polygon_valid_to" />
                        </div>
                    </div>
                </div>
                <div class="modal-footer mx-2">
                    <button type="button" class="btn me-auto" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Отменить</button>
                    <button type="button" class="btn btn-primary" @click.prevent="create">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="feather feather-save me-2" data-v-5522efca="">
                            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                            <polyline points="17 21 17 13 7 13 7 21"></polyline>
                            <polyline points="7 3 7 8 15 8"></polyline>
                        </svg>
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
