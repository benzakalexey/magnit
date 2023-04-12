<script setup>
import '@/assets/sass/visits/visits.scss';
import { ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { minLength, required, numeric, minValue, maxValue } from '@vuelidate/validators';
import { useStore } from 'vuex';
import rightSideModal from '@/components/magnit/modals/rightSideModal';

const store = useStore();
const modalTitle = 'Новый заезд';

const permit_num = ref('')
const weight = ref('')
const permit_error = ref(false)
const weight_error = ref(false)
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


const isOpen = ref(null);
const createVisit = () => {
    store.dispatch('VisitsModule/add', {
        permission_id: store.state.PermitsModule.check_permit.permission_id,
        weight: weight.value
    })
        .then(() => {
            store.dispatch('VisitsModule/update')
            if (store.state.PermitsModule.check_permit.days_before_exp <= 30) {
                new window.Swal(
                    'ВАЖНО!',
                    `Предупредите водителя!<br>До истечения пропуска, дней: ${store.state.PermitsModule.check_permit.days_before_exp}`,
                    'warning'
                );
            }
        })
        .catch();
    closeAndClean();
}

const checkPermit = (x) => {
    store.dispatch('PermitsModule/check', {
        number: permit_num.value
    })
        .then(() => permit_error.value = false)
        .catch(() => permit_error.value = true)
}
const checkWeight = () => {
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

    </rightSideModal>
</template>