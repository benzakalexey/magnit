<script setup>
import '@/assets/sass/visits/visits.scss';
import { ref, computed, toRefs } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { minLength, required, numeric } from '@vuelidate/validators';
import largeCenterModal from '@/components/magnit/modals/largeCenterModal';
import '@/assets/sass/font-icons/fontawesome/css/regular.css';
import '@/assets/sass/font-icons/fontawesome/css/fontawesome.css';

const modalTitle = 'Информация о визите';
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
const { item } = toRefs(props)
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

const v$ = useVuelidate(rules, { permit_num, weight });
const emit = defineEmits(['closed']);
const close = () => {
    emit('closed');
};
const deleteVisit = () => {
    new window.Swal({
        icon: 'warning',
        title: 'Уверены что хотите удалить?',
        text: "Информацию о визите невозможно восстановить!",
        showCancelButton: true,
        cancelButtonText: 'Отменить',
        confirmButtonText: 'Удалить',
        padding: '2em',
    }).then((result) => {
        if (result.value) {
            new window.Swal('Удалено!', 'Данные помечены как удаленные.', 'success');
            item.value.status = 2
        }
    });
}

</script>

<template>
    <largeCenterModal :modalTitle="modalTitle" :status="item.status" :isOpen="props.isOpen" @closed="close">

        <template #form>
            <form>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="col-form-label" for="permit_num">Пропуск</label>
                        <input v-model="item.permit_num" type=text readonly="true" class="form-control"
                            id="permit_num" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="reg_num">Рег. номер</label>
                        <input v-model="item.reg_num" type="text" readonly="true" class="form-control" id="reg_num" />
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="col-form-label" for="vehicle_type">Тип ТС</label>
                        <input v-model="item.vehicle_type" type="text" readonly="true" class="form-control"
                            id="vehicle_type" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="vehicle_mark">Марка ТС</label>
                        <input v-model="item.vehicle_mark" type="text" readonly="true" class="form-control"
                            id="vehicle_mark" />
                    </div>
                </div>
                <div class="mb-3">
                    <label for="contragent_name">Контрагент</label>
                    <input v-model="item.contragent_name" type="text" readonly="true" class="form-control"
                        id="contragent_name" />
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="col-form-label" for="checked_in">Дата въезда</label>
                        <input v-model="item.checked_in" type="text" readonly="true" class="form-control"
                            id="checked_in" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="weight_in">Масса при въезде</label>
                        <input v-model="item.weight_in" type="text" readonly="true" class="form-control"
                            id="weight_in" />
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
                        <input v-model="item.weight_out" type="text" readonly="true" class="form-control"
                            id="weight_out" />
                    </div>
                </div>
            </form>
        </template>

        <template #removeButton>
            <button type="button" class="btn btn-danger me-auto" @click="deleteVisit">Удалить</button>
        </template>

        <template #submitButton>
            <button type="button" class="btn btn-primary">Сохранить</button>
        </template>

    </largeCenterModal>
</template>
