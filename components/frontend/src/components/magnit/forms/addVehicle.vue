<script setup>
import '@/assets/sass/visits/visits.scss';
import { ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { minLength, required, numeric } from '@vuelidate/validators'
import rightSideModal from '@/components/magnit/modals/rightSideModal';
import '@/assets/sass/font-icons/fontawesome/css/regular.css';
import '@/assets/sass/font-icons/fontawesome/css/fontawesome.css';

const modalTitle = 'Новый автомобиль';
const form = ref(
    {
        name: '',
        email: '',
        password: '',
        passwordRepeat: '',
        hasWebsite: false,
        websiteURL: ''
    }
)

// Контрагент	
// Номер СТС	
// Регистрационный знак	
// Марка, модель	
// Тип ТС	
// Год выпуска ТС	
// Разрешенная max масса, кг	
// Масса без нагрузки, кг	
// ТОНАР


// const mixin = validationMixin
const permit_num = ref('')
const weight = ref('')
const requiredNameLength = ref(3)
const rules = computed(() => ({
    permit_num: {
        required,
        numeric,
        minLength: minLength(requiredNameLength.value)
    },
    weight: {
        required,
        numeric,
        minLength: minLength(requiredNameLength.value)
    },
}))

const v$ = useVuelidate(rules, { permit_num, weight })

const createVisit = (f) => {
    console.log(permit_num.value)
    console.log(weight.value)
    console.log(v$.value)
}

</script>

<template>

    <rightSideModal :modalTitle="modalTitle">

        <form>
            <div class="mb-3 pt-5">
                <label for="permit_num" class="col-form-label">Номер пропуска</label>
                <div>
                    <input v-model="permit_num" id="permit_num" type="number" class="form-control"
                        placeholder="Номер пропуска" />
                    <!-- :class="[v$.permit_num.$invalid ? (form.name ? 'is-valid' : 'is-invalid') : '']"  -->

                </div>
            </div>
            <div class="mb-3 pt-3">
                <label for="weight" class="col-form-label">Вес въезда</label>
                <div>
                    <input v-model="weight" id="weight" type="number" class="form-control" placeholder="Вес, кг" />
                </div>
            </div>
            <button :disabled="v$.$invalid" @click.prevent="createVisit" class="btn btn-primary my-4">Заехать</button>
        </form>

        <div v-show="!v$.$invalid" class="permit-info-list pt-5">
            <!-- <hr /> -->
            <h5 class="rs-modal-title">Информация о ТС</h5>
            <ul class="info-block list-inline">
                <li class="info-block__item">
                    <i class="far fa-flag" />
                    Контрагент
                </li>
                <li class="info-block__item">
                    <i class="far fa-bookmark"></i>
                    Марка ТС
                </li>
                <li class="info-block__item">
                    <i class="far fa-address-book"></i>
                    Регистрационный номер
                </li>
                <li class="info-block__item">
                    <i class="far fa-id-card"></i>
                    Статус пропуска
                </li>
                <li class="info-block__item">
                    <i class="far fa-clock"></i>
                    Дата истечения
                </li>
            </ul>
        </div>

    </rightSideModal>


</template>