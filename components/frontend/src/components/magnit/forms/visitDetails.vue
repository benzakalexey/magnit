<script setup>
import '@/assets/sass/visits/visits.scss';
import { ref, toRefs, watchEffect } from 'vue';
import largeCenterModal from '@/components/magnit/modals/largeCenterModal';
import finishVisit from '@/components/magnit/forms/finishVisit';

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
const emit = defineEmits(['closed', 'deleted', 'get_out', 'print_invoice', 'print_akt', 'print_pack']);
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
const getOut = (data) => {
    emit('get_out', data);
};
const finishModal = ref(false)
const polygonOut = () => {
    close();
    finishModal.value = true
};
const closeFinish = () => {
    finishModal.value = false;
};
const print_invoice = () => {
    close();
    emit('print_invoice', item.value.id)
};
const print_akt = () => {
    close();
    emit('print_akt', item.value.id, item.value.tonar)
};
const print_pack = () => {
    close();
    emit('print_pack', item.value.id)
};
watchEffect(() => (isOpen.value = props.isOpen));

</script>
<template>
    <largeCenterModal :modalTitle="item.invoice_num" :status="item.status" @closed="close" :isOpen="isOpen">
        <template #form>
            <form>
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="row">
                            <div class="col-md-6">
                                <label class="col-form-label" for="permit_num">Пропуск</label>
                                <input v-model="item.permit" type=text readonly="true" class="form-control"
                                    id="permit_num" />
                            </div>
                            <div class="col-md-6">
                                <label class="col-form-label" for="lot">Лот</label>
                                <input v-model="item.lot" type=text readonly="true" class="form-control" id="lot" />
                            </div>
                        </div>
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
                        <input :value="item.checked_in.toLocaleString('ru')" type="text" readonly="true"
                            class="form-control" id="checked_in" />
                    </div>
                    <div class="col-md-6">
                        <label class="col-form-label" for="checked_out">Дата выезда</label>
                        <input :value="item.checked_out ? item.checked_out.toLocaleString('ru') : ''" type="text"
                            readonly="true" class="form-control" id="checked_out" />
                    </div>
                </div>
                <div v-show="item.is_deleted" class="row mb-3">
                    <div class="col-md-12">
                        <label class="col-form-label" for="delete_reason">Причина удаления</label>
                        <input v-model="item.delete_reason" type="text" readonly="true" class="form-control"
                            id="delete_reason" />
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

            <div v-else :disabled="!(item.status == 1)" class="btn-group custom-dropdown" role="group">
                <button type="button" class="btn btn-primary dropdown-toggle" :disabled="!(item.status == 1)"
                    data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="feather feather-printer me-3">
                        <polyline points="6 9 6 2 18 2 18 9"></polyline>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                        <rect x="6" y="14" width="12" height="8"></rect>
                    </svg>
                    Печать
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="feather feather-chevron-down">
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                </button>
                <ul class="dropdown-menu" aria-labelledby="btndefault">
                    <li v-show="item.tonar">
                        <a @click="print_pack()" href="javascript:void(0);" class="dropdown-item"><i
                                class="flaticon-home-fill-1 me-1"></i>
                            Пакет документов
                        </a>
                    </li>
                    <li>
                        <a @click="print_akt()" href="javascript:void(0);" class="dropdown-item"><i
                                class="flaticon-gear-fill me-1"></i>
                            Акт взвешивания
                        </a>
                    </li>
                    <li v-show="item.tonar">
                        <a @click="print_invoice()" href="javascript:void(0);" class="dropdown-item"><i
                                class="flaticon-bell-fill-2 me-1"></i>
                            Транспортная накладная
                        </a>
                    </li>
                </ul>
            </div>


            <!-- <button v-else :disabled="!(item.status == 1 && item.tonar)" type="button" class="btn btn-primary"
                            @click="print()">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-printer me-3">
                                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                                <rect x="6" y="14" width="12" height="8"></rect>
                            </svg>
                            Печать ТН
                        </button> -->
        </template>
    </largeCenterModal>
    <finishVisit :item="item" :isOpen="finishModal" @closed="closeFinish" @get_out="getOut"></finishVisit>
</template>
