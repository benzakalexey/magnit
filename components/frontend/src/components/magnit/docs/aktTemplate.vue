<script setup>

import '@/assets/sass/apps/invoice-preview.scss';

const props = defineProps({
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
});

const pretty_num = (n) => {
    let r = n.match(/[а-яА-Я]+|[0-9]+/g);
    return r ? r.join(' ') : '';
};
</script>

<template>
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
                        {{ akt.polygon }} полигон
                    </td>
                </tr>
                <tr style="height: 20px"></tr>
                <tr style="height: 20px">
                    <td colspan="2"></td>
                    <td class="header" colspan="28">
                        Акт взвешивания № {{ akt.number }} от {{ akt.date.toLocaleString('ru') }}.
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
                    <td class="bordered header fw-bold" colspan="6">
                        Пропуск
                    </td>
                    <td class="bordered header fw-bold" colspan="10">
                        Вид услуги
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        ТАРА, тонн
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        БРУТТО, тонн
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        НЕТТО, тонн
                    </td>
                    <td colspan="2"></td>
                </tr>
                <tr style="height: 24px">
                    <td colspan="2"></td>
                    <td class="bordered text-center fs-6" colspan="6">
                        {{ akt.permit_number }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="10">
                        {{ akt.service_type }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.tara / 1000 }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.brutto / 1000 }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.netto / 1000 }}
                    </td>
                    <td colspan="2"></td>
                </tr>
                <tr style="height: 24px"></tr>
                <tr style="height: 24px">
                    <td colspan="4"></td>
                    <td class="text-start px-2" colspan="12">
                        Представитель<br>полигона
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
                        {{ akt.polygon }} полигон
                    </td>
                </tr>
                <tr style="height: 20px"></tr>
                <tr style="height: 20px">
                    <td colspan="2"></td>
                    <td class="header" colspan="28">
                        Акт взвешивания № {{ akt.number }} от {{ akt.date.toLocaleString('ru') }}.
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
                    <td class="bordered header fw-bold" colspan="6">
                        Пропуск
                    </td>
                    <td class="bordered header fw-bold" colspan="10">
                        Вид услуги
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        ТАРА, тонн
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        БРУТТО, тонн
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        НЕТТО, тонн
                    </td>
                    <td colspan="2"></td>
                </tr>
                <tr style="height: 24px">
                    <td colspan="2"></td>
                    <td class="bordered text-center fs-6" colspan="6">
                        {{ akt.permit_number }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="10">
                        {{ akt.service_type }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.tara / 1000 }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.brutto / 1000 }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.netto / 1000 }}
                    </td>
                    <td colspan="2"></td>
                </tr>
                <tr style="height: 24px"></tr>
                <tr style="height: 24px">
                    <td colspan="4"></td>
                    <td class="text-start px-2" colspan="12">
                        Представитель<br>полигона
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
                        {{ akt.polygon }} полигон
                    </td>
                </tr>
                <tr style="height: 20px"></tr>
                <tr style="height: 20px">
                    <td colspan="2"></td>
                    <td class="header" colspan="28">
                        Акт взвешивания № {{ akt.number }} от {{ akt.date.toLocaleString('ru') }}.
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
                    <td class="bordered header fw-bold" colspan="6">
                        Пропуск
                    </td>
                    <td class="bordered header fw-bold" colspan="10">
                        Вид услуги
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        ТАРА, тонн
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        БРУТТО, тонн
                    </td>
                    <td class="bordered header fw-bold" colspan="4">
                        НЕТТО, тонн
                    </td>
                    <td colspan="2"></td>
                </tr>
                <tr style="height: 24px">
                    <td colspan="2"></td>
                    <td class="bordered text-center fs-6" colspan="6">
                        {{ akt.permit_number }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="10">
                        {{ akt.service_type }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.tara / 1000 }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.brutto / 1000 }}
                    </td>
                    <td class="bordered text-center fs-6" colspan="4">
                        {{ akt.netto / 1000 }}
                    </td>
                    <td colspan="2"></td>
                </tr>
                <tr style="height: 24px"></tr>
                <tr style="height: 24px">
                    <td colspan="4"></td>
                    <td class="text-start px-2" colspan="12">
                        Представитель<br>полигона
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
</template>
