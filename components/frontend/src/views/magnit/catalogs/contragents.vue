<script setup>
import '@/assets/sass/widgets/widgets.scss';
import { onMounted, ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { Modal } from 'bootstrap';
import { PartnersAPI } from '@/api/partnersAPI';
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
useMeta({ title: 'Контрагенты' });

const columns = ref([
    'short_name',
    'inn',
    'address',
    'phone',
    'actions',
]);
const table = ref(null);
const table_option = ref({
    perPage: 10000000,
    perPageValues: [10000000,],
    skin: 'table table-hover',
    headings: {
        id: '',
        inn: 'ИНН',
        ogrn: 'ОГРН',
        name: 'Полное наименование',
        short_name: 'Наименование',
        kpp: 'КПП',
        address: 'Адрес',
        phone: 'Телефон',
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
        'short_name',
        'inn',
        'address',
        'phone',
    ],
});
const excel_items = () => {
    const rows = table.value ? table.value.filteredData : store.state.PartnersModule.partners
    let items = []
    for (var row of rows) {
        items.push({
            'Полное название': row.name,
            'Название': row.short_name,
            'ИНН': row.inn,
            'ОГРН': row.ogrn,
            'КПП': row.kpp,
            'Адрес': row.address,
            'Телефон': row.phone,
            'Банк': row.bank,
            'Расчетный счет': row.settlement_account,
            'Корреспондентский счет': row.correspondent_account,
            'Электронная почта': row.e_mail,
            'Действительно с': row.valid_from ? row.valid_from.toLocaleString('ru') : '',
            'Действительно до': row.valid_to ? row.valid_to.toLocaleString('ru') : '',
        })
    }
    return items;
};
const bindData = () => {
    store.dispatch('PartnersModule/get');
    // PartnersAPI.get_all().then((ref) => (partners.value = ref.data));
    // PartnersAPI.get_partner_roles().then((ref) => (partnerRoles.value = ref.data));
}

// Details Modal

let detailModal = null;
const detailsData = ref(
    {
        id: null,
        inn: null,
        ogrn: null,
        name: null,
        short_name: null,
        kpp: null,
        address: null,
        phone: null,
        bank: null,
        settlement_account: null,
        correspondent_account: null,
        e_mail: null,
        valid_from: null,
        valid_to: null,
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

// New Partner Modal

let newPartnerModal = null;
const newPartnerData = ref(
    {
        id: null,
        inn: null,
        ogrn: null,
        name: null,
        short_name: null,
        kpp: null,
        address: null,
        phone: null,
        bank: null,
        settlement_account: null,
        correspondent_account: null,
        e_mail: null,
        valid_from: null,
        valid_to: null,
    }
)
const newPartnerModalData = ref(null);
const onHiddenNewPartnerModal = () => { };
const initNewPartnerModal = () => {
    newPartnerModal = new Modal(newPartnerModalData.value)
    newPartnerModalData.value.addEventListener("hidden.bs.modal", onHiddenNewPartnerModal)
};
const openNewForm = () => {
    newPartnerData.value = {
        id: null,
        inn: null,
        ogrn: null,
        name: null,
        short_name: null,
        kpp: null,
        address: null,
        phone: null,
        bank: null,
        settlement_account: null,
        correspondent_account: null,
        e_mail: null,
        valid_from: null,
        valid_to: null,
    };
    newPartnerModal.show();
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
    PartnersAPI.update(detailsData.value)
        .then((res) => { if (res.data.success) showMessage('Данные сохранены.') })
        .then(() => store.dispatch('PartnersModule/get').then(() => detailModal.hide()))
        .catch((error) => new window.Swal('Ошибка!', error.message, 'error'))
};
const create = () => {
    newPartnerData.value.valid_from = strToDate(newPartnerData.value.valid_from)
    newPartnerData.value.valid_to = strToDate(newPartnerData.value.valid_to)
    PartnersAPI.create(newPartnerData.value)
        .then((res) => { if (res.data.success) showMessage('Новый контрагент добавлен.') })
        .then(() => store.dispatch('PartnersModule/get').then(() => newPartnerModal.hide()))
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
    utils.book_append_sheet(wb, data, `Контрагенты`)
    writeFile(wb, 'Контрагенты.xlsx')
};

onMounted(
    () => {
        bindData();
        initDetailsModal();
        initNewPartnerModal();
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
                                    <span>{{ $t('partners') }}</span>
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
                        <v-client-table :data="store.state.PartnersModule.partners" :columns="columns"
                            :options="table_option" ref="table">
                            <template #afterFilterWrapper>
                                <button type="button" class="btn btn-primary me-4" @click="openNewForm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                        stroke-linejoin="round" class="feather feather-plus me-2" data-v-02c2cbc4="">
                                        <line x1="12" y1="5" x2="12" y2="19"></line>
                                        <line x1="5" y1="12" x2="19" y2="12"></line>
                                    </svg>
                                    Новый контрагент
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
        <div class="modal-dialog modal-xl" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="detailsModalLable">{{ detailsData.short_name }}</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="full_name">Полное название</label>
                            <input v-model="detailsData.name" type="text" class="form-control" readonly="true"
                                id="full_name" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-4">
                            <label class="col-form-label" for="inn">ИНН</label>
                            <input v-model="detailsData.inn" type="text" class="form-control" readonly="true" id="inn" />
                        </div>
                        <div class="col-md-4">
                            <label class="col-form-label" for="kpp">КПП</label>
                            <input v-model="detailsData.kpp" type="text" class="form-control" readonly="true" id="kpp" />
                        </div>
                        <div class="col-md-4">
                            <label class="col-form-label" for="ogrn">ОГРН</label>
                            <input v-model="detailsData.ogrn" type="text" class="form-control" readonly="true" id="ogrn" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="address">Адрес</label>
                            <textarea v-model="detailsData.address" type="text" class="form-control" id="address"
                                rows="4" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="phone">Телефон</label>
                            <input v-model="detailsData.phone" type="text" class="form-control" id="phone" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="e_mail">Электронная почта</label>
                            <input v-model="detailsData.e_mail" type="text" class="form-control" id="e_mail" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="bank">Банк</label>
                            <input v-model="detailsData.bank" type="text" class="form-control" id="bank" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="settlement_account">Расчетный счет</label>
                            <input v-model="detailsData.settlement_account" type="text" class="form-control"
                                id="settlement_account" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="correspondent_account">Корреспондентский счет</label>
                            <input v-model="detailsData.correspondent_account" type="text" class="form-control"
                                id="correspondent_account" />
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

    <div class="modal fade" ref="newPartnerModalData" tabindex="-1" role="dialog" aria-labelledby="newPartnerModalLable"
        aria-hidden="true">
        <div class="modal-dialog modal-xl" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="newPartnerModalLable">Новый пользователь</h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="new_partner_short_name">Короткое название</label>
                            <input v-model="newPartnerData.short_name" type="text" class="form-control"
                                id="new_partner_short_name" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="new_partner_full_name">Полное название</label>
                            <input v-model="newPartnerData.name" type="text" class="form-control"
                                id="new_partner_full_name" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-4">
                            <label class="col-form-label" for="new_partner_inn">ИНН</label>
                            <input v-model="newPartnerData.inn" type="text" class="form-control" id="new_partner_inn" />
                        </div>
                        <div class="col-md-4">
                            <label class="col-form-label" for="new_partner_kpp">КПП</label>
                            <input v-model="newPartnerData.kpp" type="text" class="form-control" id="new_partner_kpp" />
                        </div>
                        <div class="col-md-4">
                            <label class="col-form-label" for="new_partner_ogrn">ОГРН</label>
                            <input v-model="newPartnerData.ogrn" type="text" class="form-control" id="new_partner_ogrn" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="new_partner_address">Адрес</label>
                            <textarea v-model="newPartnerData.address" type="text" class="form-control" id="new_partner_address"
                                rows="4" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_partner_phone">Телефон</label>
                            <input v-model="newPartnerData.phone" type="text" class="form-control" id="new_partner_phone" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_partner_e_mail">Электронная почта</label>
                            <input v-model="newPartnerData.e_mail" type="text" class="form-control" id="new_partner_e_mail" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="col-form-label" for="new_partner_bank">Банк</label>
                            <input v-model="newPartnerData.bank" type="text" class="form-control" id="new_partner_bank" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_partner_settlement_account">Расчетный счет</label>
                            <input v-model="newPartnerData.settlement_account" type="text" class="form-control"
                                id="new_partner_settlement_account" />
                        </div>
                        <div class="col-md-6">
                            <label class="col-form-label" for="new_partner_correspondent_account">Корреспондентский счет</label>
                            <input v-model="newPartnerData.correspondent_account" type="text" class="form-control"
                                id="new_partner_correspondent_account" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="new_partner_valid_from" class="col-form-label">Действует c:</label>
                            <flat-pickr v-model="newPartnerData.valid_from" :config="pickr_conf"
                                class="form-control flatpickr active" id="new_partner_valid_from" />
                        </div>
                        <div class="col-md-6">
                            <label for="new_partner_valid_to" class="col-form-label">Действует до:</label>
                            <flat-pickr v-model="newPartnerData.valid_to" :config="pickr_conf"
                                class="form-control flatpickr active" id="new_partner_valid_to" />
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
