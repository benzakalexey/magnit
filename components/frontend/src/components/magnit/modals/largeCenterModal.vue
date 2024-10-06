<script setup>

import { onMounted, watch, ref } from 'vue'
import { Modal } from 'bootstrap';

const modalElement = ref(null)
let modal = null;
onMounted(
    () => initPopup(),
);

const initPopup = () => {
    modal = new Modal(modalElement.value)
    modalElement.value.addEventListener("hidden.bs.modal", onHidden)
};

const props = defineProps({
    modalTitle: false,
    isOpen: false,
    status: false,
})
const onHidden = () => emit('closed');
const emit = defineEmits(['closed'])
const close = () => {
    modal.hide();
    emit('closed');
}
watch(() => props.isOpen, (n, _) => {
    if (n) { modal.show() } else { modal.hide() }
})

</script>

<template>
    <div class="modal fade" tabindex="-1" role="dialog" ref="modalElement" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">{{ props.modalTitle }}</h5>
                    <span v-if="props.status == 0" class="badge inv-status badge-warning ms-auto">На полигоне</span>
                    <span v-if="props.status == 1" class="badge inv-status badge-success ms-auto">Выехал</span>
                    <span v-if="props.status == 2" class="badge inv-status badge-dark ms-auto">Удален</span>
                    <button type="button" aria-label="Close" class="btn-close ms-4" @click="close"></button>
                </div>
                <div class="modal-body">
                    <div class="col-lg-12 col-12 layout-spacing">
                        <slot name="form" />
                    </div>
                </div>
                <div class="modal-footer px-4">
                    <slot name="removeButton" />
                    <!-- <button type="button" class="btn" @click="close">Закрыть</button> -->
                    <slot name="submitButton" />
                </div>
            </div>
        </div>
    </div>
</template>