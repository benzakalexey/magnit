<script setup>
import '@/assets/sass/widgets/widgets.scss';
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { Modal } from 'bootstrap';
import { PartnersAPI } from '@/api/partnersAPI';
import { DriversAPI } from '@/api/driversAPI';
import '@suadelabs/vue3-multiselect/dist/vue3-multiselect.css';

import { utils, writeFile } from 'xlsx';

const store = useStore();
useMeta({ title: 'Водители' });

const employer = ref([]);
const employers = ref([]);
const employersFromData = ref([]);
const driverRolesFromData = ref([]);
const driverRoles = ref([]);
const columns = ref([
    'full_name',
    'license',
    'employer',
    'actions',
]);
const item = ref(
    {
        first_name: '',
        last_name: '',
        patronymic: '',
        id: '',
        full_name: '',
        license: '',
        employer: '',
        employer_id: '',
        actions: '',
    }
);
const table = ref(null)
const table_option = ref({
    perPage: 10000000,
    perPageValues: [10000000,],
    skin: 'table table-hover',
    headings: {
        first_name: 'Имя',
        last_name: 'Фамилия',
        patronymic: 'Отчество',
        id: 'ИД',
        full_name: 'ФИО',
        license: 'Вод. удостоверение',
        employer: 'Организация',
        actions: '',
    },
    columnsClasses: { actions: 'actions text-center' },
    sortable: [],
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
        'full_name',
        'license',
        'employer',
    ],
    listColumns: {
        employer: employersFromData,
    },
});
const trueFalseBadge = {
    false: `<span class="badge inv-status badge-warning">Нет</span>`,
    true: `<span class="badge inv-status badge-success">Да</span>`,
};
const excel_items = () => {
    const rows = table.value ? table.value.filteredData : store.state.DriversModule.drivers
    let items = []
    for (var row of rows) {
        items.push({
            'Фамилия': row.last_name,
            'Имя': row.first_name,
            'Отчество': row.patronymic,
            'Вод. удостоверение': row.license,
            'Организация': row.employer,
        })
    }
    return items;
};
const bindData = () => {
    store.dispatch('DriversModule/get_all')
        .then(() => {
            employersFromData.value = [...new Set(store.state.DriversModule.drivers.map(item => item.employer))].map(item => ({ text: item }));
            driverRolesFromData.value = [...new Set(store.state.DriversModule.drivers.map(item => item.role))].map(item => ({ text: item }));
        });
    PartnersAPI.get_all().then((ref) => (employers.value = ref.data));
    // DriversAPI.get_driver_roles().then((ref) => (driverRoles.value = ref.data));
}

// Details Modal

let detailModal = null;
const detailsData = ref(
    {
        first_name: '',
        last_name: '',
        patronymic: '',
        id: '',
        full_name: '',
        license: '',
        employer: '',
        employer_id: '',
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

// New Driver Modal

let newDriverModal = null;
const newDriverData = ref(
    {
        first_name: null,
        last_name: null,
        patronymic: null,
        license: null,
        employer_id: null,
    }
)
const newDriverModalData = ref(null);
const onHiddenNewDriverModal = () => { };
const initNewDriverModal = () => {
    newDriverModal = new Modal(newDriverModalData.value)
    newDriverModalData.value.addEventListener("hidden.bs.modal", onHiddenNewDriverModal)
};
const openNewDriverModal = () => {
    newDriverData.value = {
        first_name: null,
        last_name: null,
        patronymic: null,
        license: null,
        employer_id: null,
    };
    newDriverModal.show();
};

const save = () => {
    DriversAPI.update(detailsData.value)
        .then((res) => { if (res.data.success) showMessage('Данные сохранены.') })
        .then(() => store.dispatch('DriversModule/get_all').then(() => detailModal.hide()))
        .catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};
const create = () => {
    DriversAPI.create(newDriverData.value)
        .then((res) => { if (res.data.success) showMessage('Новый водитель добавлен.') })
        .then(() => store.dispatch('DriversModule/get_all').then(() => newDriverModal.hide()))
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
    utils.book_append_sheet(wb, data, `Водители`)
    writeFile(wb, 'Водители.xlsx')
};

onMounted(
    () => {
        bindData();
        initDetailsModal();
        initNewDriverModal();
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
                                    <span>{{ $t('drivers') }}</span>
                                </li>
                            </ol>
                        </nav>
                    </div>
                </li>
            </ul>
            <div class="navbar-nav d-flex justify-content-end align-items-center">
                <button type="button" class="btn btn-primary me-4" v-on:click="download">Выгрузить&nbspв&nbspExcel</button>
            </div>
        </teleport>
        <div class="row layout-top-spacing">
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="store.state.DriversModule.drivers" :columns="columns" :options="table_option"
                            ref="table">
                            <template #afterFilterWrapper>
                                <button type="button" class="btn btn-primary me-4" @click="openNewDriverModal">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                        stroke-linejoin="round" class="feather feather-plus me-2" data-v-02c2cbc4="">
                                        <line x1="12" y1="5" x2="12" y2="19"></line>
                                        <line x1="5" y1="12" x2="19" y2="12"></line>
                                    </svg>
                                    Новый водитель
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
                    <h5 class="modal-title" id="detailsModalLable">{{ detailsData.full_name }}</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">

                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="license">Водительское удостоверение</label>
                            <input v-model="detailsData.license" type="text" class="form-control" id="license" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="employer">Организация</label>
                            <select class="form-select form-select" v-model="detailsData.employer_id" id="employer">
                                <option selected value=null>-</option>
                                <option v-for="p in employers" :value="p.id">{{ p.short_name }}
                                </option>
                            </select>
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

    <div class="modal fade" ref="newDriverModalData" tabindex="-1" role="dialog" aria-labelledby="newDriverModalLable"
        aria-hidden="true">
        <div class="modal-dialog modal-xl" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="newDriverModalLable">Новый водитель</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-4">
                            <label class="col-form-label" for="new_driver_last_name">Фамилия</label>
                            <input v-model="newDriverData.last_name" type="text" class="form-control"
                                id="new_driver_last_name" />
                        </div>
                        <div class="col-md-4">
                            <label class="col-form-label" for="new_driver_first_name">Имя</label>
                            <input v-model="newDriverData.first_name" type="text" class="form-control"
                                id="new_driver_first_name" />
                        </div>
                        <div class="col-md-4">
                            <label class="col-form-label" for="new_driver_patronymic">Отчество</label>
                            <input v-model="newDriverData.patronymic" type="text" class="form-control"
                                id="new_driver_patronymic" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="license">Водительское удостоверение</label>
                            <input v-model="newDriverData.license" type="text" class="form-control" id="license" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="employer">Организация</label>
                            <select class="form-select form-select" v-model="newDriverData.employer_id" id="employer">
                                <option selected value=null>-</option>
                                <option v-for="p in employers" :value="p.id">{{ p.short_name }}
                                </option>
                            </select>
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
