<script setup>
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue';

import aktTemplate from '@/components/magnit/docs/aktTemplate'

useMeta({ title: 'Акт взвешивания' });

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
)

const bind_data = () => {
    akt.value = store.state.InvoiceModule.akt
}

onMounted(
    store.dispatch('InvoiceModule/get_akt', route.query)
        .then(() => bind_data())
        .then(() => { if (route.query.print === 'true') window.print() }),
);

</script>

<template>
    <div class="invoice-container">
        <div class="invoice-inbox">
            <div id="ct" class="">
                <div class="content-section">
                    <aktTemplate :akt="akt" />
                </div>
            </div>
        </div>
    </div>
</template>
