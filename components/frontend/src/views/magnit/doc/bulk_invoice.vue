<script setup>
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { onMounted, ref } from 'vue';

import invoiceTemplate from '@/components/magnit/docs/invoiceTemplate'

useMeta({ title: 'Транспортные накладные' });

const store = useStore();
const invoices = ref([])
const bind_data = () => {
    let data = JSON.parse(localStorage.getItem('akts')) || [];
    for (let d of data) {
        store.dispatch('InvoiceModule/get', { visit_id: d.id })
        .then(() => invoices.value.push(store.state.InvoiceModule.invoice))
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
                    <div v-for="invoice in invoices">
                        <invoiceTemplate :invoice="invoice" />

                        <div class="pagebreak" />

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
