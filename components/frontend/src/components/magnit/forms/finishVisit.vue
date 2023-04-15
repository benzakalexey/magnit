<script setup>
import '@/assets/sass/visits/visits.scss';
import { toRefs, ref, computed, onMounted, watch } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, numeric, requiredIf, minValue, maxValue } from '@vuelidate/validators';
import { PolygonsAPI } from '@/api/polygonsAPI'
import { DriversAPI } from '@/api/driversAPI'
import { Modal } from 'bootstrap';

const props = defineProps({
    isOpen: false,
    item: false,
})
const { item } = toRefs(props);


const finishVisitModal = ref(null)
let modal = null;
onMounted(
    () => initPopup(),
);

const initPopup = () => {
    modal = new Modal(finishVisitModal.value)
    finishVisitModal.value.addEventListener("hidden.bs.modal", onHidden)
};

const weight = ref('')
const driver = ref('')
const drivers = ref(null)
const direction = ref('')
const directions = ref(null)
const weight_error = ref(false)
const rules = computed(() => ({
    weight: {
        required,
        numeric,
        minValueRef: minValue(item.value.tonar ? item.value.weight_in : item.value.tara),
        maxValueRef: maxValue(item.value.tonar ? item.value.max_weight : item.value.weight_in),
    },
    driver: {
        requiredIfFuction: requiredIf(() => item.value.tonar)
    },
    direction: {
        requiredIfFuction: requiredIf(() => item.value.tonar)
    },
}));

const v$ = useVuelidate(rules, {
    weight,
    driver,
    direction,
})

const bind_data = async () => {
    PolygonsAPI.get_directions(item.value.polygon_id).then((ref) => (directions.value = ref.data));
    DriversAPI.get(item.value.contragent_id).then((ref) => (drivers.value = ref.data));
};

const emit = defineEmits(['closed', 'get_out']);
const onHidden = () => emit('closed');
const close = () => {
    modal.hide();
    weight.value = '';
    driver.value = '';
    drivers.value = null;
    direction.value = '';
    directions.value = null;
    weight_error.value = false;
    emit('closed');
}
watch(() => props.isOpen, (n, _) => {
    if (n) {
        modal.show()
        bind_data()
    } else {
        modal.hide()
    };
});

const checkWeight = () => {
    const minWeight = item.value.tonar ? item.value.weight_in : item.value.tara - 1000;
    const maxWeight = item.value.tonar ? 60000 : item.value.weight_in;
    weight_error.value = !(minWeight <= weight.value && weight.value <= maxWeight);
};

const getOut = () => {
    const data = {
        visit_id: item.value.id,
        tonar: item.value.tonar,
        out_weight: Number(weight.value),
        driver: item.value.tonar ? Number(driver.value) : null,
        direction: item.value.tonar ? Number(direction.value) : null,
    };
    emit('get_out', data);
    close();
};
</script>

<template>
    <div class="modal fade" tabindex="-1" role="dialog" ref="finishVisitModal" aria-labelledby="finishVisit"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Выезд автомобиля</h5>
                    <button type="button" aria-label="Close" class="btn-close ms-4" @click="close"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label class="col-form-label" for="out_weight">Вес при выезде</label>
                            <input v-model="weight" type="number" id="out_weight" class="form-control form-control-lg"
                                :class="[weight_error ? 'is-invalid' : '']" v-on:input="checkWeight($event)" />
                            <div class="invalid-feedback">Недопустимый вес выезда</div>
                        </div>
                        <div v-show="item.tonar" class="mb-3">
                            <label class="col-form-label" for="out_weight">Водитель</label>
                            <select class="form-select form-select-lg" :disabled="!item.tonar" v-model="driver">
                                <option disabled>Выберите значение</option>
                                <option v-for="d in drivers" :value="d.id">{{ d.name }}</option>
                            </select>
                        </div>
                        <div v-show="item.tonar" class="mb-3">
                            <label class="col-form-label" for="out_weight">Направление</label>
                            <select class="form-select form-select-lg" :disabled="!item.tonar" v-model="direction">
                                <option selected disabled>Выберите значение</option>
                                <option v-for="d in directions" :value="d.id">{{ d.name }}</option>
                            </select>
                        </div>
                        <div class="d-flex justify-content-between pt-4 pb-2">
                            <button type="button" class="btn btn-danger me-auto" @click.prevent="close">Отменить</button>
                            <button :disabled="v$.$invalid" @click.prevent="getOut" class="btn btn-primary ms-auto">
                                Выпустить
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>