<script setup>
import '@/assets/sass/visits/visits.scss';
import { ref, computed, toRefs, watch, watchEffect } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { minLength, required, numeric } from '@vuelidate/validators';
import largeCenterModal from '@/components/magnit/modals/largeCenterModal';
import '@/assets/sass/font-icons/fontawesome/css/regular.css';
import '@/assets/sass/font-icons/fontawesome/css/fontawesome.css';

const form = ref({
    name: '',
    email: '',
    password: '',
    passwordRepeat: '',
    hasWebsite: false,
    websiteURL: '',
});

const props = defineProps({
    isOpen: false,
    item: false,
});
const { item } = toRefs(props);
const modalTitle = 'Информация о визите';

const isOpen = ref(false);
watchEffect(() => (isOpen.value = props.isOpen))


const requiredNameLength = ref(3);
const rules = computed(() => ({
    permit_num: {
        required,
        numeric,
        minLength: minLength(requiredNameLength.value),
    },
    weight: {
        required,
        numeric,
        minLength: minLength(requiredNameLength.value),
    },
}));

// const v$ = useVuelidate(rules, { permit_num, weight });
const emit = defineEmits(['closed', 'deleted']);
const close = () => {
    emit('closed');
};
const deleteVisit = async () => {
    close();
    const deleteReasonQ = window.Swal.mixin({
        confirmButtonText: 'Далее →',
        showCancelButton: true,
        input: 'text',
        inputAttributes: {
            required: true,
        },
        validationMessage: 'Обязательно для заполнения!',
        padding: '2em',
    });
    const deleteConfirmQ = window.Swal.mixin({
        icon: 'warning',
        title: 'Уверены что хотите удалить?',
        text: "Информацию о визите невозможно восстановить!",
        showCancelButton: true,
        cancelButtonText: 'Отменить',
        confirmButtonText: 'Удалить',
        padding: '2em',
    });

    let delete_reason;
    for (let step = 0; step < 2; step++) {
        if (step === 0) {
            const result = await deleteReasonQ.fire({
                title: 'Удаление визита',
                text: 'Укажите причину удаления',
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

            delete_reason = result.value;
            continue;
        };

        const result = await deleteConfirmQ.fire();
        if (result.value) {
            emit('deleted', item.value.id, delete_reason)
        };
    };
}

</script>

<template>
    <largeCenterModal :modalTitle="item.invoice_num" :status="item.status" @closed="close" :isOpen="isOpen">

        <template #form>
            <form>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="col-form-label" for="permit_num">Пропуск</label>
                        <input v-model="item.permit" type=text readonly="true" class="form-control" id="permit_num" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="reg_num">Рег. номер</label>
                        <input v-model="item.reg_number" type="text" readonly="true" class="form-control" id="reg_num" />
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="col-form-label" for="vehicle_type">Тип ТС</label>
                        <input v-model="item.truck_type" type="text" readonly="true" class="form-control"
                            id="vehicle_type" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="vehicle_mark">Марка ТС</label>
                        <input v-model="item.truck_model" type="text" readonly="true" class="form-control"
                            id="vehicle_mark" />
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="col-form-label" for="contragent_name">Контрагент</label>
                        <input v-model="item.carrier" type="text" readonly="true" class="form-control" id="carrier" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="invoice_num">Номер накладной</label>
                        <input v-model="item.invoice_num" type="text" readonly="true" class="form-control"
                            id="invoice_num" />
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="col-form-label" for="checked_in">Дата въезда</label>
                        <input v-model="item.checked_in" type="text" readonly="true" class="form-control" id="checked_in" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="weight_in">Масса при въезде</label>
                        <input v-model="item.weight_in" type="text" readonly="true" class="form-control" id="weight_in" />
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="col-form-label" for="checked_out">Дата выезда</label>
                        <input v-model="item.checked_out" type="text" readonly="true" class="form-control"
                            id="checked_out" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="weight_out">Масса при выезде</label>
                        <input v-model="item.weight_out" type="text" readonly="true" class="form-control" id="weight_out" />
                    </div>
                </div>
            </form>
        </template>

        <template #removeButton>
            <button :disabled="item.is_deleted" type="button" class="btn btn-danger me-auto" @click.prevent="deleteVisit">Удалить</button>
        </template>

        <template #submitButton>
            <button type="button" class="btn btn-primary" @click="test">Сохранить</button>
        </template>

    </largeCenterModal>
</template>
