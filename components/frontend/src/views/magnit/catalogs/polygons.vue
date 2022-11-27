<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import { useMeta } from '@/composables/use-meta';
import addVisit from '@/components/magnit/forms/addVisit'
import { VisitsAPI } from "@/api/visitsAPI";

useMeta({ title: 'Полигоны' });

const columns = ref(
    [
        'reg_number',
        'model',
        'vehicle_type',
        'pts_number',
        'max_weight',
        'actions',
        // 'production_year',
        // 'tara',
        // 'body_volume',
        // 'compress_ratio',
    ]
);
const items = ref([]);
const table_option = ref({
    perPage: 50,
    perPageValues: [5, 10, 20, 50],
    skin: 'table table-hover',
    headings: {
        'model': 'Марка, модель',
        'reg_number': 'Регистрационный знак',
        'pts_number': 'Номер ПТС',
        'production_year': 'Год выпуска ТС',
        'vehicle_type': 'Тип ТС',
        'tara': 'Масса без нагрузки, кг',
        'max_weight': 'Разрешенная max масса, кг',
        'body_volume': 'Объем кузова, м3',
        'compress_ratio': 'Коэффициент сжатия',
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

const item = ref(
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

onMounted(
    VisitsAPI.get_all().then((res) => items.value = res.data),
);

const delete_row = (item) => {
    if (confirm('Are you sure want to delete selected row ?')) {
        items.value = items.value.filter((d) => d.id != item.id);
    }
};

const modal = document.getElementById('#visit-detail')

const update_details = (d) => {
    item.value = d;
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
                                <li class="breadcrumb-item active" aria-current="page"><span>{{ $t('polygons') }}</span></li>
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
                        <v-client-table :data="items" :columns="columns" :options="table_option">
                            <template #actions="props">
                                <div class="actions text-center">
                                    <button type="button" class="btn btn-primary btn-sm"
                                        @click.prevent="item(props.row)" data-bs-toggle="modal"
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
                    <h5 class="modal-title" id="exampleModalLabel">Заезд {{ item.id }}</h5>
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
                    <button type="button" class="btn btn-primary">Сохранить</button>
                </div>
            </div>
        </div>
    </div>


    <addVisit></addVisit>


</template>
