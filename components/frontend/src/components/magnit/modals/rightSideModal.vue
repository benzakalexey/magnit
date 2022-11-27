<script setup>

import { ref } from 'vue'

const isOpen = ref(null);

const props = defineProps({
    modalTitle: false,
})

const checkPermit = (i) => {


    console.log(i.target.value)
}

</script>

<template>

    <teleport to="#breadcrumb">
        <div class="navbar-nav flex-row ms-auto">
            <button type="button" class="btn btn-primary me-4" @click="isOpen = !isOpen">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="feather feather-plus me-2" data-v-02c2cbc4="">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                {{ props.modalTitle }}
            </button>
        </div>
    </teleport>

    <div class="right-side-modal" :class="{ active: isOpen }">
        <div class="sidbarchat p-3" tag="div">
            <a class="btn-close" href="javascript:;" @click="isOpen = !isOpen"> </a>
            <h5 class="rs-modal-title"> {{ props.modalTitle }} </h5>

            <slot />

        </div>
    </div>

</template>