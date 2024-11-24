<script setup>
import '@/assets/sass/widgets/widgets.scss';
import { onMounted, ref, computed } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';

useMeta({ title: 'Транспортная накладная' });

const invoice = ref(
    {
        date: new Date(),
        time: '-',
        planned_time: '-',
        number: '',
        cargo_type: 'Строительные отходы',
        receiver: 'Общество с ограниченной ответственностью «Спецпереработчик», Адрес: 644070, г. Омск, ул. А. Нейбута, 91 ИНН 5504201636, КПП 550401001',
        direction: 'Производственная площадка по сбору, обработке, обезвреживанию, утилизации отходов III-V класса опасности.  644091, Омская область, г Омск, ул. Черлакский тракт, д. 12А',
        volume: '33',
        carrier: 'Общество с ограниченной ответственностью "Экоград", ИНН 7743324086, Адрес: 125438, Москва, ул. Автомоторная, дом 1/3, стр 2, Эт/П/К/Нрм 6/I/38/8',
        driver: 'Ерунков Олег Алексеевич',
        driver_licence: '99 20 461453, 22.08.2020 г.',
        truck: 'Тягач SHACMAN, Прицеп Тонар 95892 33 м³',
        truck_number: 'К360СВ186',
        trailer_number: 'ХУ074986',
        truck_volume: '',
        trailer_weight: '',
        truck_weight: '',
        contract: '0101/23-ЭГ от 01.01.2023 г.',
        polygon: 'Мусоросортировочный комплекс, расположенный по адресу: местоположение установлено относительно ориентира, расположенного в границах участка. Ориентир относительно ориентира расположенного за пределами участка, в 500 метрах юго-западнее здания с почтовым адресом: Российская Федерация, Омская область, г. Омск, Ленинский АО, yл. Черлакский тракт, дом 10. Кадастровый номер земельного участка – 55:36:200106:224.',
        weight_txt: '-',
    }
)

const printAkt = () => {
    let date = new Date(invoice.value.date)
    let query_params = '&date=' + date.toLocaleDateString('ru') +
        '&time=' + invoice.value.time +
        '&planned_time=' + invoice.value.planned_time +
        '&number=' + invoice.value.number +
        '&cargo_type=' + invoice.value.cargo_type +
        '&receiver=' + invoice.value.receiver +
        '&direction=' + invoice.value.direction +
        '&volume=' + invoice.value.volume +
        '&carrier=' + invoice.value.carrier +
        '&driver=' + invoice.value.driver +
        '&driver_licence=' + invoice.value.driver_licence +
        '&truck=' + invoice.value.truck +
        '&truck_number=' + invoice.value.truck_number +
        '&trailer_number=' + invoice.value.trailer_number +
        '&truck_volume=' + invoice.value.truck_volume +
        '&trailer_weight=' + invoice.value.trailer_weight +
        '&truck_weight=' + invoice.value.truck_weight +
        '&contract=' + invoice.value.contract +
        '&polygon=' + invoice.value.polygon +
        '&weight_txt=' + invoice.value.weight_txt;

    let winPrint = window.open(
        '/hand_filled_invoice?print=true' + query_params,
        'fullscreen=yes,toolbar=0,scrollbars=0,status=0'
    );
    winPrint.focus();
    winPrint.onafterprint = winPrint.close;
};

</script>
<style>
.multiselect__option--highlight {
    background: #fff;
    color: #4361ee;
}

.multiselect__option--selected {
    background-color: rgba(27, 85, 226, 0.23921568627450981);
    color: #4361ee;
    font-weight: normal;
}

.multiselect__option--disabled {
    background: inherit !important;
}

.multiselect__tags {
    width: 18em;
    height: 2.5em;
}

.multiselect__tag {
    color: #000;
    background: #e4e4e4;
}

.multiselect__tag-icon:after {
    color: #000 !important;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
    background: inherit;
}
</style>

<template>
    <div class="layout-px-spacing">
        <teleport to="#breadcrumb">
            <ul class="navbar-nav flex-row">
                <li>
                    <div class="page-header">
                        <nav class="breadcrumb-one" aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item active" aria-current="page">
                                    <span>{{ $t('visits') }}</span>
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
                    <div class="col-lg-12 layout-spacing">
                        <div class="statbox panel box box-shadow">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xl-12 col-md-12 col-sm-12 col-12">
                                        <h4>Транспортная накладная</h4>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-body">

                                <form>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="date">Дата</label>
                                        <input v-model="invoice.date" type="date" id="date" required
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="number">Номер</label>
                                        <input v-model="invoice.number" id="number" type="text"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="receiver">Грузополучатель</label>
                                        <textarea v-model="invoice.receiver" id="receiver"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="direction">Реквизиты грузополучателя</label>
                                        <textarea v-model="invoice.direction" id="direction"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="carrier">Перевозчик</label>
                                        <textarea v-model="invoice.carrier" type="text" id="carrier"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="driver">Водитель</label>
                                        <textarea v-model="invoice.driver" type="text" id="driver"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="driver_licence">Водительское удостоверение</label>
                                        <textarea v-model="invoice.driver_licence" type="text" id="driver_licence"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="truck">Транспортное средство</label>
                                        <textarea v-model="invoice.truck" type="text" id="truck"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="truck_number">Регистрационный номер ТС</label>
                                        <input v-model="invoice.truck_number" type="text" id="truck_number"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="trailer_number">Регистрационный номер прицепа</label>
                                        <input v-model="invoice.trailer_number" type="text" id="trailer_number"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="contract">Договор</label>
                                        <input v-model="invoice.contract" type="text" id="contract"
                                            class="form-control form-control-lg" />
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="polygon">Полигон</label>
                                        <textarea v-model="invoice.polygon" type="text" id="polygon"
                                            class="form-control form-control-lg" rows="5"/>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="weight_txt">Масса груза</label>
                                        <input v-model="invoice.weight_txt" type="text" id="weight_txt"
                                            class="form-control form-control-lg"/>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="col-form-label" for="volume">Объем груза</label>
                                        <input v-model="invoice.volume" type="text" id="volume"
                                            class="form-control form-control-lg"/>
                                    </div>


                                </form>
                                <button type="button" class="btn btn-success" @click="printAkt()">
                                    <!-- Печать -->
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                        stroke-linejoin="round" class="feather feather-printer mx-3">
                                        <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                        <path
                                            d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2">
                                        </path>
                                        <rect x="6" y="14" width="12" height="8"></rect>
                                    </svg>
                                </button>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
