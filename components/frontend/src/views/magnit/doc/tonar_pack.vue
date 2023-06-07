<script setup>
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue';

import invoiceTemplate from '@/components/magnit/docs/invoiceTemplate'
import aktTemplate from '@/components/magnit/docs/aktTemplate'


useMeta({ title: 'Пакет документов тонар' });

const route = useRoute()
const store = useStore();
const akt = ref(
    {
        date: new Date(),
        polygon: null,
        number: null,
        carrier: null,
        truck_mark: null,
        truck_number: null,
        permit_number: null,
        service_type: null,
        netto: null,
        tara: null,
        brutto: null,
    }
);
const invoice = ref(
    {
        date: '',
        time: '',
        planned_time: '',
        number: '',
        cargo_type: '',
        receiver: '',
        direction: '',
        volume: '',
        carrier: '',
        driver: '',
        driver_licence: '',
        truck: '',
        truck_number: '',
        trailer_number: '',
        truck_volume: '',
        trailer_weight: '',
        truck_weight: '',
        contract: '',
        polygon: '',
    }
);

const bind_data = () => {
    akt.value = store.state.InvoiceModule.akt;
    invoice.value = store.state.InvoiceModule.invoice;
};

onMounted(
    () => {
        store.dispatch('InvoiceModule/get_akt', route.query)
            .then(() => {
                store.dispatch('InvoiceModule/get', route.query)
                    .then(() => bind_data())
                    .then(() => { if (route.query.print === 'true') window.print() });
            })
    }
);

</script>

<template>
    <div class="invoice-container">
        <div class="invoice-inbox">
            <div id="ct" class="">
                <div class="content-section">

                    <invoiceTemplate :invoice="invoice" />

                    <div class="pagebreak"></div>

                    <invoiceTemplate :invoice="invoice" />

                    <div class="pagebreak"></div>

                    <invoiceTemplate :invoice="invoice" />

                    <div class="pagebreak"></div>

                    <aktTemplate :akt="akt" />

                </div>
            </div>
        </div>
    </div>
</template>
