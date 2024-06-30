<script setup>
import '@/assets/sass/visits/visits.scss';
import { ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { minLength, required, numeric, minValue, maxValue, helpers } from '@vuelidate/validators';
import { useStore } from 'vuex';
import rightSideModal from '@/components/magnit/modals/rightSideModal';

const store = useStore();
const modalTitle = 'Новый заезд';

const permit_num = ref('')
const weight = ref('')
const lot = ref(null)
const truck_number = ref('')
const permit_error = ref(false)
const weight_error = ref(false)
const truck_number_error = ref(false)
const truck_number_validator = helpers.regex(/^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}$/ui)
const rules = computed(() => ({
    permit_num: {
        required,
        numeric,
        minLength: minLength(2)
    },
    lot: {
        required
    },
    weight: {
        required,
        numeric,
        minValueRef: minValue(store.state.PermitsModule.check_permit.tara || 0),
        maxValueRef: maxValue(store.state.PermitsModule.check_permit.max_weight * 1.2)
    },
    truck_number: {
        required: false,
        pattern: truck_number_validator,
        $lazy: true,
        $autoDirty: true
    },
}))

const v$ = useVuelidate(rules, { permit_num, lot,  weight, truck_number })


const isOpen = ref(null);
const createVisit = () => {
    store.dispatch('VisitsModule/add', {
        permission_id: store.state.PermitsModule.check_permit.permission_id,
        service_contract_id: store.state.PermitsModule.check_permit.service_contract_id,
        weight: weight.value,
        lot: lot.value.id,
        truck_number: store.state.PermitsModule.check_permit.reg_number || truck_number.value,
    })
        .then(() => {
            console.log(store.state.PermitsModule.check_permit.days_before_exp)
            if (store.state.PermitsModule.check_permit.days_before_exp <= 3) {
                new window.Swal(
                    'ВАЖНО!',
                    `Предупредите водителя!<br>До истечения пропуска, дней: ${store.state.PermitsModule.check_permit.days_before_exp}`,
                    'warning'
                );
            };
            closeAndClean();
            store.dispatch('VisitsModule/update')
        })
        .catch();
}

const checkPermit = (x) => {
    store.dispatch('PermitsModule/clear_check');
    if (String(permit_num.value).length > 2) {
        store.dispatch('PermitsModule/check', {
            number: permit_num.value
        })
            .then(() => permit_error.value = false)
            .catch(() => permit_error.value = true)
    };

}
const checkWeight = () => {
    let minWeight = store.state.PermitsModule.check_permit.tara || 0
    let maxWeight = store.state.PermitsModule.check_permit.max_weight
    weight_error.value = !(minWeight <= weight.value && weight.value <= maxWeight)
}
const checkTrackNumber = () => {
    let minWeight = store.state.PermitsModule.check_permit.tara || 0
    let maxWeight = store.state.PermitsModule.check_permit.max_weight
    weight_error.value = !(minWeight <= weight.value && weight.value <= maxWeight)
}

const statuses = {
    0: `<span class="ms-4 badge inv-status badge-danger">Просрочен</span>`,
    1: `<span class="ms-4 badge inv-status badge-success">Активен</span>`,
};

const closeAndClean = () => {
    store.commit('PermitsModule/clearCheckPermitData');
    permit_num.value = '';
    weight.value = '';
    isOpen.value = !isOpen.value;
};

</script>

<template>
    <rightSideModal :modalTitle="modalTitle" :isOpen="isOpen">

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
            <div class="mb-3"
                v-show="store.state.PermitsModule.check_permit.permit_num && !store.state.PermitsModule.check_permit.is_tonar">
                <label class="col-form-label" for="lot">Лот</label>
                <select class="form-select form-select-lg" id="lot" v-model="lot" placeholder="Выберите лот">
                    <option :value="null" disabled selected>Выберите Лот</option>
                    <option :value="{id: null, number: null}">Без Лота</option>
                    <option v-for="l in store.state.PermitsModule.check_permit.lots" :value="l">{{ l.number }}</option>
                </select>
            </div>
            <div class="mb-3 pt-3"
                v-show="store.state.PermitsModule.check_permit.permit_num && store.state.PermitsModule.check_permit.reg_number === null">

                <label for="truck_number" class="col-form-label">Номер ТС</label>
                <div>
                    <input v-model="truck_number" id="truck_number" type="text" class="form-control" placeholder="Номер ТС"
                        :class="[v$.truck_number.$invalid ? 'is-invalid' : '']" />
                    <div class="invalid-feedback" v-if="v$.truck_number.$error">
                        Введите номер в формате а555аа55(5)
                    </div>
                </div>
            </div>
            <button
                :disabled="v$.$invalid || Array(null, 0, undefined).includes(store.state.PermitsModule.check_permit.permit_status)"
                @click.prevent="createVisit" class="btn btn-primary my-4">
                Заехать
            </button>
        </form>

        <div v-show="!permit_error && store.state.PermitsModule.check_permit.reg_number" class="permit-info-list pt-5">
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

        <div v-show="store.state.PermitsModule.check_permit.permit_num && !store.state.PermitsModule.check_permit.reg_number"
            class="permit-info-list pt-5">
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
                    <!-- Контрагент -->
                    {{ store.state.PermitsModule.check_permit.contragent }}
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

    </rightSideModal>
</template>