<script setup>
import '@/assets/sass/widgets/widgets.scss';
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { Modal } from 'bootstrap';
import { PolygonsAPI } from '@/api/polygonsAPI';
import { UsersAPI } from '@/api/usersAPI';
import '@suadelabs/vue3-multiselect/dist/vue3-multiselect.css';

import { utils, writeFile } from 'xlsx';

const store = useStore();
useMeta({ title: 'Пользователи' });

const polygons = ref([]);
const polygonsFromData = ref([]);
const userRolesFromData = ref([]);
const userRoles = ref([]);
const columns = ref([
    'name',
    'address',
    'valid_from',
    // 'is_staff',
    // 'is_active',
    // 'role',
    'actions',
]);
const table = ref(null);
const item = ref(
    {
        name: '',
        address: '',
        valid_from: '',
        id: '',
        // is_active: '',
        // is_staff: '',
        // first_name: '',
        // patronymic: '',
        // phone: '',
        // polygon: '',
        // role: '',
        // surname: '',
    }
);
const table_option = ref({
    perPage: 10000000,
    perPageValues: [10000000,],
    skin: 'table table-hover',
    headings: {
        name: 'Название',
        address: 'Адрес',
        valid_from: 'Изменено',
        // id: '',
        // is_active: 'Активен',
        // is_staff: 'Сотрудник',
        // first_name: 'Имя',
        // patronymic: 'Отчество',
        // phone: 'Телефон',
        // polygon: 'Полигон',
        // role: 'Группа',
        // surname: 'Фамилия',
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
        'valid_from',
    ],
});
const trueFalseBadge = {
    false: `<span class="badge inv-status badge-warning">Нет</span>`,
    true: `<span class="badge inv-status badge-success">Да</span>`,
};
const excel_items = () => {
    const rows = table.value ? table.value.filteredData : store.state.UsersModule.users
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
    store.dispatch('UsersModule/get')
        .then(() => {
            polygonsFromData.value = [...new Set(store.state.UsersModule.users.map(item => item.polygon))].map(item => ({ text: item }));
            userRolesFromData.value = [...new Set(store.state.UsersModule.users.map(item => item.role))].map(item => ({ text: item }));
        });
    PolygonsAPI.get_all().then((ref) => (polygons.value = ref.data));
    UsersAPI.get_user_roles().then((ref) => (userRoles.value = ref.data));
}

// Details Modal

let detailModal = null;
const detailsData = ref(
    {
        added_at: '',
        added_by: '',
        full_name: '',
        id: '',
        is_active: '',
        is_staff: '',
        first_name: '',
        patronymic: '',
        phone: '',
        polygon: '',
        role: '',
        surname: '',
    }
)
const detailsDataModal = ref(null);
const onHidden = () => {};
const initDetailsModal = () => {
    detailModal = new Modal(detailsDataModal.value)
    detailsDataModal.value.addEventListener("hidden.bs.modal", onHidden)
};
const openDetails = (data) => {
    detailsData.value = data;
    detailModal.show();
};

// New User Modal

let newUserModal = null;
const newUserData = ref(
    {
        polygon_id: '',
        phone: '',
        password: '',
        role: '',
        is_staff: '',
        is_active: '',
        surname: '',
        first_name: '',
        patronymic: '',
    }
)
const newUserModalData = ref(null);
const onHiddenNewUserModal = () => {};
const initNewUserModal = () => {
    newUserModal = new Modal(newUserModalData.value)
    newUserModalData.value.addEventListener("hidden.bs.modal", onHiddenNewUserModal)
};
const openNewForm = () => {
    newUserData.value = {
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
    newUserModal.show();
};

const resetPassword = async () => {
    detailModal.hide();
    const newPasswordForm = window.Swal.mixin({
        confirmButtonText: 'Сохранить',
        showCancelButton: true,
        input: 'text',
        inputAttributes: {
            required: true,
        },
        validationMessage: 'Обязательно для заполнения!',
        padding: '2em',
    });
    let newPassword;
    for (let step = 0; step < 2; step++) {
        if (step === 0) {
            const result = await newPasswordForm.fire({
                title: 'Сброс пароля',
                text: 'Задайте новый пароль',
                showCancelButton: true,
                cancelButtonText: 'Отменить',
                currentProgressStep: step,
            });
            if (result.dismiss === window.Swal.DismissReason.cancel) {
                break;
            };
            if (result.dismiss === window.Swal.DismissReason.backdrop) {
                break;
            };
            newPassword = result.value;
            if (result.value) {
                UsersAPI.updp(
                    {
                        user_id: detailsData.value.id, 
                        new_pass: newPassword,
                    }
                )
                    .then((res) => { if (res.data.success) showMessage('Данные сохранены.') })
                    .then(() => store.dispatch('UsersModule/get').then(() => detailModal.hide()))
                    .catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
            };
            continue;
        };

    };
};
const save = () => {
    UsersAPI.update(detailsData.value)
        .then((res) => { if (res.data.success) showMessage('Данные сохранены.') })
        .then(() => store.dispatch('UsersModule/get').then(() => detailModal.hide()))
        .catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};
const create = () => {
    UsersAPI.create(newUserData.value)
        .then((res) => { if (res.data.success) showMessage('Новый пользователь добавлен.') })
        .then(() => store.dispatch('UsersModule/get').then(() => newUserModal.hide()))
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
    utils.book_append_sheet(wb, data, `Пользователи`)
    writeFile(wb, 'Пользователи.xlsx')
};

onMounted(
    () => {
        bindData();
        initDetailsModal();
        initNewUserModal();
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
                <button type="button" class="btn btn-primary me-4" v-on:click="download">Выгрузить&nbspв&nbspExcel</button>
            </div>
        </teleport>
        <div class="row layout-top-spacing">
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="polygons" :columns="columns" :options="table_option"
                            ref="table">
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
                            <!-- <template #valid_from="props">
                                <div :data_sort="props.row.valid_from">
                                    {{ props.row.valid_from ? props.row.valid_from.toLocaleDateString('ru') : '-' }}
                                </div>
                            </template> -->
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
                        <div class="col-md-3">
                            <div class="checkbox-default custom-control custom-checkbox">
                                <input type="checkbox" class="custom-control-input" id="is_staff"
                                    v-model="detailsData.is_staff" />
                                <label class="custom-control-label" for="is_staff"> Сотрудник </label>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="checkbox-default custom-control custom-checkbox">
                                <input type="checkbox" class="custom-control-input" id="is_active"
                                    v-model="detailsData.is_active" />
                                <label class="custom-control-label" for="is_active"> Активен </label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="phone">Телефон</label>
                            <input v-model="detailsData.phone" type="text" readonly="true" class="form-control"
                                id="phone" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="role">Должность</label>
                            <select class="form-select form-select" v-model="detailsData.role" id="role">
                                <option selected value=null>-</option>
                                <option v-for="p in userRoles" :value="p">{{ p }}
                                </option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="polygon">Полигон</label>
                            <select class="form-select form-select" v-model="detailsData.polygon_id" id="polygon">
                                <option selected value=null>-</option>
                                <option v-for="p in polygons" :value="p.id">{{ p.name }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="modal-footer mx-2">
                    <button :disabled="item.is_deleted" type="button" class="btn btn-outline-danger me-auto"
                        @click.prevent="resetPassword">Установить пароль</button>
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>Закрыть</button>
                    <button type="button" class="btn btn-primary" @click.prevent="save">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" ref="newUserModalData" tabindex="-1" role="dialog" aria-labelledby="newUserModalLable"
        aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="newUserModalLable">Новый пользователь</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-3">
                            <div class="checkbox-default custom-control custom-checkbox">
                                <input type="checkbox" class="custom-control-input" id="new_user_is_staff"
                                    v-model="newUserData.is_staff" />
                                <label class="custom-control-label" for="new_user_is_staff"> Сотрудник </label>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="checkbox-default custom-control custom-checkbox">
                                <input type="checkbox" class="custom-control-input" id="new_user_is_active"
                                    v-model="newUserData.is_active" />
                                <label class="custom-control-label" for="new_user_is_active"> Активен </label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_user_last_name">Фамилия</label>
                            <input v-model="newUserData.surname" type="text" class="form-control"
                                id="new_user_last_name" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_user_phone">Телефон</label>
                            <input v-model="newUserData.phone" type="text" class="form-control"
                                id="new_user_phone" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_user_first_name">Имя</label>
                            <input v-model="newUserData.first_name" type="text" class="form-control"
                                id="new_user_first_name" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_user_role">Должность</label>
                            <select class="form-select form-select" v-model="newUserData.role" id="new_user_role">
                                <option selected value=null>-</option>
                                <option v-for="p in userRoles" :value="p">{{ p }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_user_patronymic">Отчество</label>
                            <input v-model="newUserData.patronymic" type="text" class="form-control"
                                id="new_user_patronymic" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_user_polygon">Полигон</label>
                            <select class="form-select form-select" v-model="newUserData.polygon_id" id="new_user_polygon">
                                <option selected value=null>-</option>
                                <option v-for="p in polygons" :value="p.id">{{ p.name }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="new_user_pass">Пароль</label>
                            <input v-model="newUserData.password" type="text" class="form-control"
                                id="new_user_pass" />
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
