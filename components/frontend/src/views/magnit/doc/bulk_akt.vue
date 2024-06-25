<script setup>
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { onMounted, ref } from 'vue';

import aktTemplate from '@/components/magnit/docs/aktLotTemplate'

useMeta({ title: 'Акт взвешивания' });

const store = useStore();
const akts = ref([])
const bind_data = () => {
    let data = JSON.parse(localStorage.getItem('akts')) || [];
    for (let d of data) {
        store.dispatch('InvoiceModule/get_akts', { visit_id: d.id })
        .then(() => akts.value.push(store.state.InvoiceModule.akt))
    }
};

onMounted(
    () => {
        bind_data()
    },
);

</script>

<template>
    <div class="invoice-container">
        <div class="invoice-inbox">
            <div id="ct" class="">
                <div class="content-section">
                    <div v-for="akt in akts">
                        <aktTemplate :akt="akt" />

                        <div class="pagebreak"></div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
