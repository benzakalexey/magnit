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

<template>
    <div class="invoice-container">
        <div class="invoice-inbox">
            <div id="ct" class="">
                <div class="content-section">
                    <div class="table-responsive">
                        <table class="table mb-0" cellspacing="0" cellpadding="0">
                            <tbody>
                                <tr>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                    <td style="width:6px"></td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header" colspan="32">
                                        {{ akt.polygon }} полигон ООО «Магнит»
                                    </td>
                                </tr>
                                <tr style="height: 20px"></tr>
                                <tr style="height: 20px">
                                    <td colspan="2"></td>
                                    <td class="header" colspan="28">
                                        Акт взвешивания № {{ akt.number }} от {{ akt.date.toLocaleDateString('ru') }} г.
                                    </td>
                                    <td colspan="2"></td>
                                </tr>
                                <tr style="height: 32px"></tr>
                                <tr style="height: 20px">
                                    <td colspan="4"></td>
                                    <td class="text-start" colspan="6">
                                        Перевозчик
                                    </td>
                                    <td class="header text-start" colspan="4">
                                        {{ akt.carrier }}
                                    </td>
                                    <td colspan="18"></td>
                                </tr>
                                <tr style="height: 20px">
                                    <td colspan="4"></td>
                                    <td class="text-start" colspan="6">
                                        Марка машины
                                    </td>
                                    <td class="header text-start" colspan="4">
                                        {{ akt.truck_mark }}
                                    </td>
                                    <td colspan="18"></td>
                                </tr>
                                <tr style="height: 20px">
                                    <td colspan="4"></td>
                                    <td class="text-start" colspan="6">
                                        Гос. номер
                                    </td>
                                    <td class="header text-start" colspan="4">
                                        {{ akt.truck_number }}
                                    </td>
                                    <td colspan="18"></td>
                                </tr>
                                <tr style="height: 32px"></tr>
                                <tr style="height: 32px">
                                    <td colspan="2"></td>
                                    <td class="bordered header" colspan="2">
                                        Номер<br>пропуска
                                    </td>
                                    <td class="bordered header" colspan="10">
                                        Вид услуги
                                    </td>
                                    <td class="bordered header" colspan="5">
                                        ТАРА
                                    </td>
                                    <td class="bordered header" colspan="5">
                                        БРУТТО
                                    </td>
                                    <td class="bordered header" colspan="5">
                                        НЕТТО
                                    </td>
                                    <td colspan="2"></td>
                                </tr>
                                <tr style="height: 32px">
                                    <td colspan="2"></td>
                                    <td class="bordered text-center px-2" colspan="2">
                                        {{ akt.permit_number }}
                                    </td>
                                    <td class="bordered text-center px-2" colspan="10">
                                        {{ akt.service_type }}
                                    </td>
                                    <td class="bordered text-center px-2" colspan="5">
                                        {{ akt.tara / 1000 }} тонн.
                                    </td>
                                    <td class="bordered text-center px-2" colspan="5">
                                        {{ akt.brutto / 1000 }} тонн.
                                    </td>
                                    <td class="bordered text-center px-2" colspan="5">
                                        {{ akt.netto / 1000 }} тонн.
                                    </td>
                                    <td colspan="2"></td>
                                </tr>
                                <tr style="height: 32px"></tr>
                                <tr style="height: 32px">
                                    <td class="text-start px-2" colspan="16">
                                        Представитель<br>ООО «Магнит»
                                    </td>
                                    <td class="text-start px-2" colspan="16">
                                        Представитель<br>{{ akt.carrier }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
