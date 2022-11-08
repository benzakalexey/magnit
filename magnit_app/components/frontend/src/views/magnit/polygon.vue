<template>
    <div class="layout-px-spacing">
        <teleport to="#breadcrumb">
            <ul class="navbar-nav flex-row">
                <li>
                    <div class="page-header">
                        <nav class="breadcrumb-one" aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><a href="/">Полигон</a></li>
                                <li class="breadcrumb-item active" aria-current="page"><span>Контролер</span></li>
                            </ol>
                        </nav>
                    </div>
                </li>
            </ul>

            <ul class="navbar-nav flex-row ms-auto">
                <button type="button" class="btn btn-primary me-4" @click="isOpen = !isOpen">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="feather feather-plus me-2" data-v-02c2cbc4="">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    Новый заезд
                </button>
            </ul>
        </teleport>

        <div class="row layout-top-spacing">
            <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
                <div class="panel br-6 p-0">
                    <div class="custom-table">
                        <v-client-table :data="items" :columns="columns" :options="table_option">
                            <template #actions="props">
                                <div class="actions text-center">
                                    <button type="button" class="btn btn-primary btn-sm"
                                        @click.prevent="update_details(props.row)" data-bs-toggle="modal"
                                        data-bs-target="#visit-detail">Открыть</button>
                                </div>
                            </template>
                            <template #salary="props"> ${{ props.row.salary }} </template>
                        </v-client-table>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <!-- visit detail modal -->
    <div class="modal fade" id="visit-detail" tabindex="-1" role="dialog" ref="details-modal"
        aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Заезд {{ visit_data.id }} </h5>
                    <button type="button" data-dismiss="modal" data-bs-dismiss="modal" aria-label="Close"
                        class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="col-lg-12 col-12 layout-spacing">
                        <form>
                            <div class="mb-3">
                                <label for="email" class="col-form-label">Email address</label>
                                <div>
                                    <input id="email" type="email" class="form-control"
                                        placeholder="name@example.com" />
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="select" class="col-form-label">Example select</label>
                                <div>
                                    <select id="select" class="form-select">
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                    </select>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="multiselect" class="col-form-label">Example multiple select</label>
                                <div>
                                    <select id="multiselect" multiple class="form-select">
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                    </select>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="textarea" class="col-form-label">Email textarea</label>
                                <div>
                                    <textarea id="textarea" class="form-control" style="height: 95px"></textarea>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="file" class="col-form-label">Email file input</label>
                                <div>
                                    <input id="file" type="file" class="form-control-file" />
                                </div>
                            </div>

                            <button type="submit" class="btn btn-primary my-4">Submit</button>
                        </form>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn" data-dismiss="modal" data-bs-dismiss="modal"><i
                            class="flaticon-cancel-12"></i>
                        Discard</button>
                    <button type="button" class="btn btn-primary">Save</button>
                </div>
            </div>
        </div>
    </div>


    <div>

        <div class="left-side-modal" :class="{ active: isOpen }">

            <perfect-scrollbar class="sidbarchat p-3" tag="div">
                <a class="btn-close" href="javascript:;" @click="isOpen = !isOpen"> </a>




            </perfect-scrollbar>
        </div>
    </div>


</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import { useMeta } from '@/composables/use-meta';

useMeta({ title: 'Контролер' });

const columns = ref(
    [
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
    ]
);
const items = ref([]);
const table_option = ref({
    perPage: 50,
    perPageValues: [5, 10, 20, 50],
    skin: 'table table-hover',
    headings: {
        'permit_num': 'Пропуск',
        'reg_num': 'Номер',
        'contragent_name': 'Контрагент',
        'vehicle_mark': 'Марка ТС',
        'vehicle_type': 'Тип ТС',
        'weight_in': 'Вес заезда',
        'weight_out': 'Вес выезда',
        'loading_weight': 'Вес загрузки',
        'checked_in': 'Въезд',
        'checked_out': 'Выезд',
        'status': 'Статус',
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

const visit_data = ref(
    {
        'id': '',
        'name': '',
        'position': '',
        'office': '',
        'age': '',
        'start_date': '',
        'salary': '',
    }
);

const isOpen = ref(null);

onMounted(
    async () => {
        const { data } = await axios.get('/visits.json');
        items.value = data;
    }
);

const delete_row = (item) => {
    if (confirm('Are you sure want to delete selected row ?')) {
        items.value = items.value.filter((d) => d.id != item.id);
    }
};

const modal = document.getElementById('#visit-detail')

const update_details = (item) => {
    visit_data.value = item;
};

</script>
