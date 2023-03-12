<script setup>
import '@/assets/sass/visits/visits.scss';
import { ref, computed, toRefs, onMounted, watchEffect } from 'vue';
import largeCenterModal from '@/components/magnit/modals/largeCenterModal';
import '@/assets/sass/font-icons/fontawesome/css/regular.css';
import '@/assets/sass/font-icons/fontawesome/css/fontawesome.css';
import { DriversAPI } from "@/api/driversAPI";
import { PolygonsAPI } from "@/api/polygonsAPI"

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
const isOpen = ref(false);
const emit = defineEmits(['closed', 'deleted']);
const close = () => {
    emit('closed');
};
const deleteVisit = async () => {
    close();
    const deleteReasonQ = window.Swal.mixin({
        confirmButtonText: 'Удалить',
        showCancelButton: true,
        input: 'text',
        inputAttributes: {
            required: true,
        },
        validationMessage: 'Обязательно для заполнения!',
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
            if (result.value) {
                emit('deleted', item.value.id, delete_reason)
            };
            continue;
        };

    };
};


const polygonOut = async () => {
    close();
    const drivers = await DriversAPI.get(item.value.contragent_id);
    const directions = await PolygonsAPI.get_directions(item.value.polygon_id);
    
    let drivers_options = [`<option disabled selected>Выберите водителя</option>`];
    for (var d of drivers.data) {
        drivers_options.push(
            `<option value="${d.id}">${d.name}</option>`
        )
    };

    let directions_options = [`<option disabled selected>Выберите направление</option>`];
    for (var d of directions.data) {
        directions_options.push(
            `<option value="${d.id}">${d.name}</option>`
        )
    };

    const outData = {
        true: `<label class="col-form-label swal2-wide" for="out_weight">Вес при выезде</label>
            <input type="number" id="out_weight" class="swal2-input swal2-wide my-1">
            <label class="col-form-label swal2-wide" for="driver">Водитель</label>
            <select type="number" id="driver" required class="swal2-input swal2-wide my-1">
                ${drivers_options}
            </select>
            <label class="col-form-label swal2-wide" for="direction">Направление</label>
            <select type="number" id="direction" required class="swal2-input swal2-wide my-1">
                ${directions_options}
            </select>`,
        false: `<label class="col-form-label swal2-wide" for="out_weight">Вес при выезде</label>
            <input type="number" id="out_weight" class="swal2-input swal2-wide my-1">`,
    }
    const outDataQ = window.Swal.mixin({
        confirmButtonText: 'Далее →',
        showCancelButton: true,
        html: outData[item.value.tonar],
        preConfirm: () => {
            return {
                visit_id: item.value.id,
                tonar: item.value.tonar,
                out_weight: document.getElementById('out_weight') ? Number(document.getElementById('out_weight').value) : null,
                driver: document.getElementById('driver') ? Number(document.getElementById('driver').value) : null,
                direction: document.getElementById('direction') ? Number(document.getElementById('direction').value) : null,
            }
        },
        inputAttributes: {
            required: true,
        },
        validationMessage: 'Обязательно для заполнения!',
        padding: '2em',
        customClass: 'swal-wide',
    });

    const result = await outDataQ.fire({
        title: 'Выезд автомобиля',
        showCancelButton: true,
        cancelButtonText: 'Отменить',
    });
    if (result.value) {
        emit('get_out', result.value)
    };
};


const print = () => {
    emit('print', item.value.id)
    close();
};
watchEffect(() => (isOpen.value = props.isOpen));

</script>
<style>
.swal-wide {
    width: 850px !important;
}
.swal2-wide {
    width: 640px !important;
}
</style>
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
                        <label class="col-form-label" for="checked_out">Дата выезда</label>
                        <input v-model="item.checked_out" type="text" readonly="true" class="form-control"
                            id="checked_out" />
                    </div>
                </div>
            </form>
        </template>

        <template #removeButton>
            <button :disabled="item.is_deleted" type="button" class="btn btn-danger me-auto"
                @click.prevent="deleteVisit">Удалить</button>
        </template>

        <template #submitButton>
            <button v-if="item.status == 0" type="button" class="btn btn-primary" @click="polygonOut()">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="feather feather-arrow-up-right me-3">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                </svg>
                Выпустить
            </button>
            <button v-else :disabled="!(item.status == 1 && item.tonar)" type="button" class="btn btn-primary"
                @click="print()">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="feather feather-printer me-3">
                    <polyline points="6 9 6 2 18 2 18 9"></polyline>
                    <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                    <rect x="6" y="14" width="12" height="8"></rect>
                </svg>
                Печать ТН
            </button>
        </template>

    </largeCenterModal>
</template>
