<script setup>
import '@/assets/sass/visits/visits.scss';
import { ref, computed, onMounted } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { minLength, required, numeric, minValue, maxValue } from '@vuelidate/validators';
import { useStore } from 'vuex';
import rightSideModal from '@/components/magnit/modals/rightSideModal';
// import '@/assets/sass/font-icons/fontawesome/css/regular.css';
// import '@/assets/sass/font-icons/fontawesome/css/fontawesome.css';

import feather from 'feather-icons';

const store = useStore();
const modalTitle = 'Новый заезд';

// const mixin = validationMixin
const permit_num = ref('')
const weight = ref('')
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
const createVisit = (f) => {
    store.dispatch('VisitsModule/add', {
        permission_id: store.state.PermitsModule.check_permit.permission_id,
        weight: weight.value
    }).catch();
    store.dispatch('VisitsModule/update');
    closeAndClean();
}

const checkPermit = (x) => {
    store.dispatch('PermitsModule/check', {
        number: permit_num.value
    }).catch()
}

const statuses = {
    0: `<span class="badge inv-status badge-danger">Просрочен</span>`,
    1: `<span class="badge inv-status badge-success">Активен</span>`,
};

onMounted(() => {
    feather.replace();
});

const closeAndClean = () => {
    store.commit('PermitsModule/clearCheckPermitData');
    permit_num.value = '';
    weight.value = '';
    isOpen.value = !isOpen.value;
};

</script>

<template>
    <rightSideModal :modalTitle="modalTitle" :isOpen="isOpen">

        <form>
            <div class="mb-3 pt-5">
                <label for="permit_num" class="col-form-label">Номер пропуска</label>
                <div>
                    <input v-model="permit_num" id="permit_num" type="number" class="form-control"
                        placeholder="Номер пропуска" v-on:input="checkPermit($event)" />
                </div>
            </div>
            <div class="mb-3 pt-3">
                <label for="weight" class="col-form-label">Вес въезда</label>
                <div>
                    <input v-model="weight" id="weight" type="number" class="form-control" placeholder="Вес, кг" />
                </div>
            </div>
            <button :disabled="v$.$invalid" @click.prevent="createVisit" class="btn btn-primary my-4">
                Заехать
            </button>
        </form>

        <div v-show="store.state.PermitsModule.check_permit.reg_number" class="permit-info-list pt-5">
            <h5 class="rs-modal-title">Пропуск</h5>


            <ul class="info-block list-inline">
                <li class="info-block__item">
                    <i data-feather="check"></i>
                    <!-- Статус -->
                    <text v-html="statuses[store.state.PermitsModule.check_permit.permit_status]" />
                </li>
                <li class="info-block__item">
                    <i data-feather="check"></i>
                    <!-- Регистрационный номер -->
                    {{ store.state.PermitsModule.check_permit.reg_number }}
                </li>
                <li class="info-block__item">
                    <i data-feather="truck"></i>
                    <!-- Марка ТС -->
                    {{ store.state.PermitsModule.check_permit.truck_model }}
                </li>
                <li class="info-block__item">
                    <i data-feather="flag"></i>
                    <!-- Контрагент -->
                    {{ store.state.PermitsModule.check_permit.contragent }}
                </li>
                <li class="info-block__item">
                    <i data-feather="minus"></i>
                    <!-- Марка ТС -->
                    {{ store.state.PermitsModule.check_permit.truck_type }}
                </li>
                <li class="info-block__item">
                    <i data-feather="minus"></i>Тара:
                    {{ store.state.PermitsModule.check_permit.tara }}
                </li>
                <li class="info-block__item">
                    <i data-feather="minus"></i>Макс. Брутто:
                    {{ store.state.PermitsModule.check_permit.max_weight }}
                </li>
                <li class="info-block__item">
                    <i data-feather="minus"></i>Истекает:
                    {{ new Date(store.state.PermitsModule.check_permit.expired_at).toLocaleDateString('RU') }}
                </li>
            </ul>
        </div>

    </rightSideModal>
</template>