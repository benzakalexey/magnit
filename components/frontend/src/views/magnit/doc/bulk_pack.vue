<script setup>
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { onMounted, ref } from 'vue';

import aktTemplate from '@/components/magnit/docs/aktTemplate'
import invoiceTemplate from '@/components/magnit/docs/invoiceTemplate'

useMeta({ title: 'Транспортные накладные' });

const store = useStore();
const packs = ref({})
const bind_data = () => {
    let data = JSON.parse(localStorage.getItem('akts')) || [];
    for (let d of data) {
        packs.value[d.id] = {
            invoice: {
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
            },
            akt: {
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
            },
        }

        store.dispatch('InvoiceModule/get', { visit_id: d.id })
            .then(() => packs.value[d.id].invoice = store.state.InvoiceModule.invoice);

        store.dispatch('InvoiceModule/get_akts', { visit_id: d.id })
            .then(() => packs.value[d.id].akt = store.state.InvoiceModule.akt)
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
                    <div v-for="(pack, key, index) of packs">
                        <invoiceTemplate :invoice="pack.invoice" />

                        <div class="pagebreak"></div>

                        <invoiceTemplate :invoice="pack.invoice" />

                        <div class="pagebreak"></div>

                        <invoiceTemplate :invoice="pack.invoice" />

                        <div class="pagebreak"></div>

                        <aktTemplate :akt="pack.akt" />

                        <div v-if="index != packs.length - 1" class="pagebreak" />

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
