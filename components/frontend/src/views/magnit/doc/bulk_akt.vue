<script setup>
import '@/assets/sass/apps/invoice-preview.scss';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue';
import { async } from 'file-upload-with-preview';

useMeta({ title: 'Акт взвешивания' });

const route = useRoute()
const store = useStore();
const akts = ref([])
const service_type = 'Транспортирование ТКО (IV-V)'
const bind_data = () => {
    let data = JSON.parse(localStorage.getItem('akts')) || [];
    for (let d of data) {
        store.dispatch('InvoiceModule/get_akts', { visit_id: d.id })
            .then(() => akts.value.push(store.state.InvoiceModule.akt))
    }
}

onMounted(
    () => {
        bind_data()
    },
);

const pretty_num = (n) => {
    let r = n.match(/[а-яА-Я]+|[0-9]+/g);
    return r ? r.join(' ') : '';
};

</script>

<template>
    <div class="invoice-container">
        <div class="invoice-inbox">
            <div id="ct" class="">
                <div class="content-section">
                    <div v-for="akt in akts">
                        <div class="table-responsive">
                            <table class="table table-invoice mb-0" cellspacing="0" cellpadding="0">
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
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Перевозчик
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.carrier }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Марка машины
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.truck_mark }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Гос. номер
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.truck_number }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 24px">
                                        <td colspan="2"></td>
                                        <td class="bordered header" colspan="6">Пропуск</td>
                                        <td class="bordered header" colspan="10">
                                            Вид услуги
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            ТАРА
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            БРУТТО
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            НЕТТО
                                        </td>
                                        <td colspan="2"></td>
                                    </tr>
                                    <tr style="height: 24px">
                                        <td colspan="2"></td>
                                        <td class="bordered text-center" colspan="6">
                                            {{ akt.permit_number }}
                                        </td>
                                        <td class="bordered text-center" colspan="10">
                                            {{ akt.service_type }}
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.tara / 1000 }} тонн
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.brutto / 1000 }} тонн
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.netto / 1000 }} тонн
                                        </td>
                                        <td colspan="2"></td>
                                    </tr>
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 24px">
                                        <td colspan="4"></td>
                                        <td class="text-start px-2" colspan="12">
                                            Представитель<br>ООО «Магнит»
                                        </td>
                                        <td class="text-start px-2" colspan="12">
                                            Представитель<br>{{ akt.carrier }}
                                        </td>
                                        <td colspan="4"></td>
                                    </tr>
                                    <tr style="height: 32px">
                                        <td colspan="4"></td>
                                        <td class="underline" colspan="10"></td>
                                        <td colspan="2"></td>
                                        <td class="underline" colspan="12"></td>
                                        <td colspan="4"></td>
                                    </tr>
                                    <tr style="height: 42px;">
                                        <td colspan="2"></td>
                                        <td class="dashedline" colspan="28"></td>
                                        <td colspan="2"></td>
                                    </tr>

                                    <tr style="height: 24px"></tr>

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
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Перевозчик
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.carrier }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Марка машины
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.truck_mark }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Гос. номер
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.truck_number }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 24px">
                                        <td colspan="2"></td>
                                        <td class="bordered header" colspan="6">Пропуск</td>
                                        <td class="bordered header" colspan="10">
                                            Вид услуги
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            ТАРА
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            БРУТТО
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            НЕТТО
                                        </td>
                                        <td colspan="2"></td>
                                    </tr>
                                    <tr style="height: 24px">
                                        <td colspan="2"></td>
                                        <td class="bordered text-center" colspan="6">
                                            {{ akt.permit_number }}
                                        </td>
                                        <td class="bordered text-center" colspan="10">
                                            {{ akt.service_type }}
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.tara / 1000 }} тонн
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.brutto / 1000 }} тонн
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.netto / 1000 }} тонн
                                        </td>
                                        <td colspan="2"></td>
                                    </tr>
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 24px">
                                        <td colspan="4"></td>
                                        <td class="text-start px-2" colspan="12">
                                            Представитель<br>ООО «Магнит»
                                        </td>
                                        <td class="text-start px-2" colspan="12">
                                            Представитель<br>{{ akt.carrier }}
                                        </td>
                                        <td colspan="4"></td>
                                    </tr>
                                    <tr style="height: 32px">
                                        <td colspan="4"></td>
                                        <td class="underline" colspan="10"></td>
                                        <td colspan="2"></td>
                                        <td class="underline" colspan="12"></td>
                                        <td colspan="4"></td>
                                    </tr>
                                    <tr style="height: 42px;">
                                        <td colspan="2"></td>
                                        <td class="dashedline" colspan="28"></td>
                                        <td colspan="2"></td>
                                    </tr>

                                    <tr style="height: 24px"></tr>

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
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Перевозчик
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.carrier }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Марка машины
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.truck_mark }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 20px">
                                        <td colspan="4"></td>
                                        <td class="text-start" colspan="6">
                                            Гос. номер
                                        </td>
                                        <td class="header text-start" colspan="12">
                                            {{ akt.truck_number }}
                                        </td>
                                        <td colspan="10"></td>
                                    </tr>
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 24px">
                                        <td colspan="2"></td>
                                        <td class="bordered header" colspan="6">Пропуск</td>
                                        <td class="bordered header" colspan="10">
                                            Вид услуги
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            ТАРА
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            БРУТТО
                                        </td>
                                        <td class="bordered header" colspan="4">
                                            НЕТТО
                                        </td>
                                        <td colspan="2"></td>
                                    </tr>
                                    <tr style="height: 24px">
                                        <td colspan="2"></td>
                                        <td class="bordered text-center" colspan="6">
                                            {{ akt.permit_number }}
                                        </td>
                                        <td class="bordered text-center" colspan="10">
                                            {{ akt.service_type }}
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.tara / 1000 }} тонн
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.brutto / 1000 }} тонн
                                        </td>
                                        <td class="bordered text-center" colspan="4">
                                            {{ akt.netto / 1000 }} тонн
                                        </td>
                                        <td colspan="2"></td>
                                    </tr>
                                    <tr style="height: 24px"></tr>
                                    <tr style="height: 24px">
                                        <td colspan="4"></td>
                                        <td class="text-start px-2" colspan="12">
                                            Представитель<br>ООО «Магнит»
                                        </td>
                                        <td class="text-start px-2" colspan="12">
                                            Представитель<br>{{ akt.carrier }}
                                        </td>
                                        <td colspan="4"></td>
                                    </tr>
                                    <tr style="height: 32px">
                                        <td colspan="4"></td>
                                        <td class="underline" colspan="10"></td>
                                        <td colspan="2"></td>
                                        <td class="underline" colspan="12"></td>
                                        <td colspan="4"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="pagebreak"></div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
