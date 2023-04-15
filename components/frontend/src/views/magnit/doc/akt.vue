<script setup>
import '@/assets/sass/apps/invoice-preview.scss';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue';

useMeta({ title: 'Акт взвешивания' });

const route = useRoute()
const store = useStore();
const akt = ref(
    {
        date: null,
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

const pretty_num = (n) => {
    let r = n.match(/[а-яА-Я]+|[0-9]+/g);
    return r ? r.join('\u2009') : '';
};

</script>

<style type="text/css">
table {
    page-break-inside: auto;
    border-collapse: collapse;
}

.table>tbody>tr>td {
    font-size: 12px;
    padding: 0rem 0rem;
    border: 0px;
    letter-spacing: 0px;
}

.table .bordered {
    border: 1px solid;
}

.table .underrow {
    font-size: 6px;
    text-align: center;
    vertical-align: text-top;
    padding-inline: 2em;
}

.table .header {
    font-weight: bold;
    text-align: center;
}

.table .sign {
    font-weight: 600;
    text-align: right;
    padding-inline: 2em;
    vertical-align: bottom;
}

tr {
    page-break-inside: avoid;
    page-break-after: auto;
}

thead {
    display: table-header-group
}

tfoot {
    display: table-footer-group
}

.invoice-container {
    max-width: 210mm;
}

@page {
    size: A4 portrait;
    margin: 24px 24px;
}

@media print {
    .table .bordered {
        border: solid #000 !important;
        border-width: 1pt !important;
        border-collapse: collapse;
        color: #000
    }

    .table>tbody>tr>td {
        color: #000
    }

    .dark .table>tbody>tr>td {
        color: #000
    }
    .pagebreak {
        clear: both;
        page-break-after: always;
    }
}
</style>

<template>
    <div class="invoice-container">
        <div class="invoice-inbox">
            <div id="ct" class="">
                <div class="invoice-00001">
                    <div class="content-section">

                        <div class="table-responsive">
                            <table class="table mb-0" cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                        <td style="width:8px"></td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td class="header" colspan="32">
                                            {{ akt.polygon }} полигон ООО «Магнит»
                                        </td>
                                    </tr>
                                    <tr style="height: 20px"></tr>
                                    <tr style="height: 20px">
                                        <td colspan="7"></td>
                                        <td class="header" colspan="6">
                                            Акт взвешивания №
                                        </td>
                                        <td class="header" colspan="7">
                                            {{ akt.number }}
                                        </td>
                                        <td class="header" colspan="1">
                                            от
                                        </td>
                                        <td class="header" colspan="4">
                                            {{ akt.date.toLocaleDateString('ru') }} г.
                                        </td>
                                        <td colspan="7"></td>
                                    </tr>
                                    <tr style="height: 40px"></tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Перевозчик
                                        </td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Марка машины
                                        </td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Гос. номер
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
