<script setup>
import '@/assets/sass/apps/invoice-preview.scss';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue';

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
    }
)

const bind_data = () => {
    invoice.value = store.state.InvoiceModule.invoice
}

onMounted(
    store.dispatch('InvoiceModule/get', route.query)
        .then(() => bind_data())
        .then(() => { if (route.query.print === 'true') window.print() }),
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
                    <div class="table-responsive ">
                        <table class="table table-invoice mb-0" cellspacing="0" cellpadding="0">
                            <tbody>
                                <tr>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                    <td style="width:2px"></td>
                                </tr>
                                <tr style="height: 18px">
                                    <td colspan="57"></td>
                                    <td class="ps-2 text-center" colspan="54">Приложение № 4</td>
                                </tr>
                                <tr style="height: 18px">
                                    <td colspan="57"></td>
                                    <td class="ps-2 text-center" colspan="54">к Правилам перевозок грузов
                                        автомобильным транспортом</td>
                                </tr>
                                <tr style="height: 18px">
                                    <td colspan="57"></td>
                                    <td class="ps-2 text-center" colspan="54">
                                        (в ред. Постановления Правительства РФ от 30.11.2021 №
                                        2116)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header" colspan="111">Транспортная накладная</td>
                                </tr>
                                <tr class="bordered" style="height: 20px">
                                    <td class="header bordered" colspan="67">Транспортная
                                        накладная</td>
                                    <td class="header bordered" colspan="44">Заказ (заявка)</td>
                                </tr>
                                <tr class="bordered" style="height: 20px">
                                    <td class="ps-2" colspan="14">Дата</td>
                                    <td class="bordered ps-2" colspan="20">{{ invoice.date }}</td>
                                    <td class="ps-2" colspan="10">№</td>
                                    <td class="ps-2" colspan="23">{{ invoice.number }}</td>
                                    <td class="bordered ps-2" colspan="10">Дата</td>
                                    <td class="ps-2" colspan="12">-</td>
                                    <td class="bordered ps-2" colspan="10">№</td>
                                    <td class="ps-2" colspan="12">-</td>
                                </tr>
                                <tr class="bordered" style="height: 20px">
                                    <td class="ps-2" colspan="14">Экземпляр №</td>
                                    <td class="bordered ps-2" colspan="53"></td>
                                    <td class="bordered header ps-2" colspan="44">-</td>
                                </tr>
                                <tr class="bordered" style="height: 20px">
                                    <td class="header bordered" colspan="67">1. Грузоотправитель</td>
                                    <td class="header bordered" colspan="44" rowspan="2">
                                        1а. Заказчик услуг по организации
                                        перевозки груза (при наличии)
                                    </td>
                                </tr>
                                <tr class="bordered" style="height: 20px">
                                    <td class="px-2 text-center" colspan="37">является экспедитором</td>
                                    <td class="header bordered" colspan="30">-</td>
                                </tr>
                                <tr class="bordered" style="height: 20px">
                                    <td class="px-2 text-center" colspan="67">
                                        Общество с ограниченной
                                        ответственностью &quot;Магнит&quot;, ИНН
                                        5401381810, Адрес: 644024, Омская область, г. Омск, ул.
                                        Декабристов, дом 45, корп. 1, пом. 19, тел.
                                        8 (3812) 35-25-25
                                    </td>
                                    <td class="bordered header" colspan="44">-</td>
                                </tr>
                                <tr class="bordered" style="height: 12px">
                                    <td class="underrow" colspan="67">
                                        (реквизиты, позволяющие идентифицировать
                                        Грузоотправителя)
                                    </td>
                                    <td class="underrow" colspan="44">
                                        (реквизиты, позволяющие
                                        идентифицировать Заказчика услуг по организации
                                        перевозки груза)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered header" colspan="67">-</td>
                                    <td class="bordered header" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="bordered underrow" colspan="67">
                                        реквизиты документа, определяющего основания осуществления расчетов по
                                        договору перевозки иным лицом, отличным от грузоотправителя (при наличии)
                                    </td>
                                    <td class="bordered underrow" colspan="44">
                                        (реквизиты договора на выполнение услуг по организации перевозки груза)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        2. Грузополучатель
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="111">
                                        {{ invoice.receiver }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (реквизиты, позволяющие идентифицировать
                                        Грузополучателя)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="111">
                                        {{ invoice.direction }}
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="underrow bordered" colspan="111">
                                        (адрес места доставки груза)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        3. Груз
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered text-center px-2" colspan="67">
                                        {{ invoice.cargo_type }}
                                    </td>
                                    <td class="bordered text-center px-2" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (отгрузочное наименование груза
                                        (для опасных грузов - в соответствии с
                                        ДОПОГ), его состояние и другая необходимая информация о
                                        грузе)
                                    </td>
                                    <td class="underrow bordered" colspan="44">(количество
                                        грузовых мест,
                                        маркировка, вид тары и способ упаковки)</td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered text-center px-2" colspan="111">
                                        Объем груза - {{ invoice.volume }} м³, масса согласно акту
                                        взвешивания {{ invoice.number }} от {{ invoice.date }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (масса груза брутто в
                                        килограммах, масса груза нетто в килограммах (при
                                        возможности ее определения), размеры (высота, ширина,
                                        длина) в метрах (при перевозке
                                        крупногабаритного груза), объем груза в кубических
                                        метрах и плотность груза в соответствии с
                                        документацией на груз (при необходимости),
                                        дополнительные характеристики груза, учитывающие
                                        отраслевые особенности (при необходимости)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (в случае перевозки опасного
                                        груза - информация по каждому опасному
                                        веществу, материалу или изделию в соответствии с пунктом
                                        5.4.1 ДОПОГ)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (объявленная стоимость
                                        (ценность) груза (при необходимости)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        4. Сопроводительные документы на груз (при наличии)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (перечень прилагаемых к транспортной накладной
                                        документов,
                                        предусмотренных ДОПОГ, санитарными, таможенными (при
                                        наличии),
                                        карантинными, иными правилами в соответствии с
                                        законодательством Российской Федерации, либо
                                        регистрационные номера указанных документов, если такие
                                        документы (сведения о таких документах) содержатся
                                        в государственных информационных системах)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (перечень прилагаемых к грузу
                                        сертификатов, паспортов качества,
                                        удостоверений и других документов, наличие которых
                                        установлено законодательством Российской
                                        Федерации, либо регистрационные номера указанных
                                        документов, если такие документы (сведения о таких
                                        документах) содержатся в государственных
                                        информационных системах)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered text-center px-2" colspan="111">
                                        {{ invoice.number }} от {{ invoice.date }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (реквизиты, позволяющие
                                        идентифицировать документ(-ы), подтверждающий(-ие)
                                        отгрузку товаров) (при наличии), реквизиты
                                        сопроводительной ведомости (при перевозке груженых
                                        контейнеров или порожних контейнеров)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        5. Указания грузоотправителя по
                                        особым условиям перевозки
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (маршрут перевозки, дата и
                                        время/сроки доставки груза (при необходимости)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (контактная информация о лицах,
                                        по указанию которых может осуществляться
                                        переадресовка)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (указания, необходимые для
                                        выполнения фитосанитарных, санитарных,
                                        карантинных, таможенных и прочих требований,
                                        установленных законодательством Российской
                                        Федерации)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (температурный режим перевозки
                                        груза (при необходимости), сведения о
                                        запорно-пломбировочных устройствах (в случае их
                                        предоставления грузоотправителем), запрещение
                                        перегрузки груза)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        6. Перевозчик
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="67">
                                        {{ invoice.carrier }}
                                    </td>
                                    <td class="bordered px-2 text-center" colspan="44">
                                        {{ invoice.driver }}<br>ВУ - {{ invoice.driver_licence }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (реквизиты, позволяющие
                                        идентифицировать Перевозчика)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (реквизиты, позволяющие
                                        идентифицировать водителя(-ей)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        7. Транспортное средство
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="67">
                                        {{ invoice.truck }}
                                    </td>
                                    <td class="bordered px-2 text-center" colspan="44">
                                        {{ pretty_num(invoice.truck_number) }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (тип, марка, грузоподъемность
                                        (в тоннах), вместимость (в кубических метрах)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (регистрационный номер
                                        транспортного средства)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        Тип владения: 3 - аренда
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="underrow bordered" colspan="111">
                                        Тип владения:
                                        1 - собственность;
                                        2 - совместная собственность супругов;
                                        3 - аренда;
                                        4 - лизинг;
                                        5 - безвозмездное пользование;
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="67">
                                        {{ invoice.contract }}
                                    </td>
                                    <td class="bordered px-2 text-center" colspan="44">
                                        -
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="underrow bordered" colspan="67">
                                        (реквизиты документа(-ов), подтверждающего(-их) основание владения
                                        грузовым автомобилем<br>(тягачом, а также прицепом
                                        (полуприцепом) (для типов владения 3, 4, 5)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (номер, дата и срок действия специального разрешения, установленный маршрут
                                        движения тяжеловесного и (или) крупногабаритного
                                        транспортного средства или транспортного
                                        средства, перевозящего опасный груз) (при наличии)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        8. Прием груза
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="111">
                                        Общество с ограниченной
                                        ответственностью &quot;Магнит&quot;
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (реквизиты лица, осуществляющего погрузку
                                        груза в транспортное средство)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="111">
                                        Общество с ограниченной
                                        ответственностью &quot;Магнит&quot;
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (наименование (ИНН) владельца
                                        объекта инфраструктуры пункта погрузки)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="111">
                                        {{ invoice.polygon }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (адрес места погрузки)</td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="37">
                                        {{ invoice.date }} {{ invoice.planned_time }}
                                    </td>
                                    <td class="bordered px-2 text-center" colspan="37">
                                        {{ invoice.date }} {{ invoice.planned_time }}
                                    </td>
                                    <td class="bordered px-2 text-center" colspan="37">
                                        {{ invoice.date }} {{ invoice.time }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="37">
                                        (заявленные дата и время подачи
                                        транспортного средства под погрузку)
                                    </td>
                                    <td class="underrow bordered" colspan="37">
                                        (фактические дата и время прибытия под погрузку)
                                    </td>
                                    <td class="underrow bordered" colspan="37">
                                        (фактические дата и время убытия)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="111">
                                        Масса согласно акту взвешивания К-АПР.22-474-Т от
                                        07.04.2022
                                        способ - разница между массой ТС перед погрузкой и после
                                        погрузки
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (масса груза брутто в
                                        килограммах и метод ее определения (определение
                                        разницы между массой транспортного средства после
                                        погрузки и перед погрузкой по общей массе или
                                        взвешиванием поосно или расчетная масса груза)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (количество грузовых мест)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (тара, упаковка (при наличии)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (оговорки и замечания
                                        перевозчика (при наличии) о дате и времени
                                        прибытия/убытия, о состоянии, креплении груза, тары,
                                        упаковки, маркировки, опломбирования, о
                                        массе груза и количестве грузовых мест, о проведении
                                        погрузочных работ)
                                    </td>
                                </tr>
                                <tr style="height: 37px">
                                    <td class="bordered sign" colspan="67">
                                        Приказ ООО &quot;Магнит&quot; №168 от 31.12.20 г.
                                    </td>
                                    <td class="bordered sign" colspan="44">
                                        {{ invoice.driver }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (подпись, расшифровка подписи
                                        лица, осуществившего погрузку груза, с
                                        указанием реквизитов документа, подтверждающего
                                        полномочия лица на погрузку груза)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (подпись, расшифровка подписи
                                        водителя, принявшего груз для перевозки)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        9. Переадресовка (при наличии)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (дата, вид переадресовки на
                                        бумажном носителе или в электронном виде (с
                                        указанием вида доставки документа)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (адрес нового пункта выгрузки,
                                        новые дата и время подачи транспортного
                                        средства под выгрузку)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (реквизиты лица, от которого
                                        получено указание на переадресовку)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (при изменении получателя груза
                                        - реквизиты нового получателя)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        10. Выдача груза
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="67">
                                        {{ invoice.direction }}
                                    </td>
                                    <td class="bordered px-2 text-center" colspan="44"></td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (адрес места выгрузки)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (заявленные дата и время подачи
                                        транспортного средства под выгрузку)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67"></td>
                                    <td class="header bordered" colspan="44"></td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (фактические дата и время прибытия)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (фактические дата и время убытия)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (фактическое состояние груза,
                                        тары, упаковки, маркировки, опломбирования)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (количество грузовых мест)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="bordered px-2 text-center" colspan="67">
                                        масса согласно акту взвешивания {{ invoice.number }} от {{ invoice.date }}
                                    </td>
                                    <td class="bordered px-2 text-center" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (масса груза брутто в
                                        килограммах, масса груза нетто в килограммах
                                        (при возможности ее определения), плотность груза в
                                        соответствии с документацией на груз (при
                                        необходимости)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (оговорки и замечания
                                        перевозчика (при наличии) о дате и времени
                                        прибытия/убытия, о состоянии груза, тары, упаковки,
                                        маркировки, опломбирования, о массе груза и
                                        количестве грузовых мест)
                                    </td>
                                </tr>
                                <tr style="height: 37px">
                                    <td class="bordered sign" colspan="67">
                                    </td>
                                    <td class="bordered sign" colspan="44">
                                        {{ invoice.driver }}
                                    </td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (должность, подпись,
                                        расшифровка подписи грузополучателя или
                                        уполномоченного грузоотправителем лица)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (подпись, расшифровка подписи
                                        водителя, сдавшего груз грузополучателю
                                        или уполномоченному грузополучателем лицу)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        11. Отметки грузоотправителей,
                                        грузополучателей, перевозчиков (при
                                        необходимости)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="22">-</td>
                                    <td class="header bordered" colspan="22">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (краткое описание обстоятельств, послуживших основанием
                                        для отметки,
                                        сведения о коммерческих и иных актах, в том числе о
                                        погрузке/выгрузке груза)
                                    </td>
                                    <td class="underrow bordered" colspan="22">(расчет и размер
                                        штрафа)</td>
                                    <td class="underrow bordered" colspan="22">(подпись, дата)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">
                                        12. Стоимость перевозки груза
                                        (установленная плата) в рублях (при
                                        необходимости)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="28">-</td>
                                    <td class="header bordered" colspan="28">-</td>
                                    <td class="header bordered" colspan="28">-</td>
                                    <td class="header bordered" colspan="27">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="28">
                                        (стоимость перевозки без налога - всего)
                                    </td>
                                    <td class="underrow bordered" colspan="28">
                                        (налоговая ставка)
                                    </td>
                                    <td class="underrow bordered" colspan="28">
                                        (сумма налога, предъявляемая покупателю)
                                    </td>
                                    <td class="underrow bordered" colspan="27">
                                        (стоимость перевозки с налогом - всего)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="111">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="111">
                                        (порядок (механизм) расчета (исчислений) платы)
                                        (при наличии порядка (механизма)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (реквизиты, позволяющие
                                        идентифицировать Экономического субъекта,
                                        составляющего первичный учетный документ о факте
                                        хозяйственной жизни со стороны Перевозчика)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (реквизиты, позволяющие
                                        идентифицировать Экономического субъекта,
                                        составляющего первичный учетный документ о факте
                                        хозяйственной жизни со стороны
                                        Грузоотправителя)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (основание, по которому
                                        Экономический субъект является составителем <br>
                                        документа о факте хозяйственной жизни)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (основание, по которому
                                        Экономический субъект является составителем <br>
                                        документа о факте хозяйственной жизни)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">-</td>
                                    <td class="underrow bordered" colspan="44">
                                        (реквизиты, позволяющие
                                        идентифицировать лицо, от которого будут поступать
                                        денежные средства)</td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (подпись, расшифровка подписи
                                        лица, ответственного за оформление факта
                                        хозяйственной жизни со стороны Перевозчика
                                        (уполномоченного лица)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (подпись, расшифровка подписи
                                        лица, ответственного за оформление факта
                                        хозяйственной жизни со стороны Грузоотправителя
                                        (уполномоченного лица)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (должность, основание
                                        полномочий физического лица, уполномоченного
                                        Перевозчиком (уполномоченным лицом), дата подписания)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (должность, основание
                                        полномочий физического лица, уполномоченного
                                        Грузоотправителем (уполномоченным лицом), дата
                                        подписания)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (подпись, расшифровка
                                        подписи
                                        лица, ответственного за оформление факта
                                        хозяйственной жизни со стороны Перевозчика
                                        (уполномоченного лица)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (подпись, расшифровка
                                        подписи
                                        лица, ответственного за оформление факта
                                        хозяйственной жизни со стороны Грузоотправителя
                                        (уполномоченного лица)
                                    </td>
                                </tr>
                                <tr style="height: 20px">
                                    <td class="header bordered" colspan="67">-</td>
                                    <td class="header bordered" colspan="44">-</td>
                                </tr>
                                <tr style="height: 12px">
                                    <td class="underrow bordered" colspan="67">
                                        (должность, основание
                                        полномочий физического лица, уполномоченного
                                        Перевозчиком (уполномоченным лицом), дата подписания)
                                    </td>
                                    <td class="underrow bordered" colspan="44">
                                        (должность, основание
                                        полномочий физического лица, уполномоченного
                                        Грузоотправителем (уполномоченным лицом), дата
                                        подписания)
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
