<script setup>
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue';

import invoiceTemplateHandMade from '@/components/magnit/docs/invoiceTemplateHandMade'

useMeta({ title: 'Транспортная накладная' });

const route = useRoute()
const store = useStore();
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
        weight_txt: '',
    }
)

const bind_data = () => {
    invoice.value = route.query
}

onMounted(
    () => {
        console.log(route.query);
        bind_data();
        if (route.query.print === 'true') window.print()
    },
    // store.dispatch('InvoiceModule/get', route.query)
    //     .then(() => bind_data())
    //     .then(() => { if (route.query.print === 'true') window.print() }),
);

</script>

<template>
    <div class="invoice-container">
        <div class="invoice-inbox">
            <div id="ct" class="">
                <div class="content-section">
                    <div class="table-responsive ">

                        <invoiceTemplateHandMade :invoice="invoice" />

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
