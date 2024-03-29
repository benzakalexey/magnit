<script setup>

import { ref, watch } from 'vue'

const isOpen = ref(null);

const props = defineProps({
    modalTitle: false,
    isOpen: false,
})

watch(() => props.isOpen, (n, _) => isOpen.value = false)

const weightingButton = async () => {
    const steps = ['1', '2', '3'];

    const weighingSwal = window.Swal.mixin({
        icon: 'info',
        title: 'Выберите ТС',
        progressSteps: steps,
        html: `<select class="form-select form-select-lg">
            <option selected disabled>Выберите значение</option>
            <option>Корнет (К 479 КЕ 186)</option>
            <option>Корнет (К 475 МВ 186)</option>
            <option>Самосвал (М 962 АМ 186)</option>
            <option>Самосвал (Е 019 АЕ 186)</option>
            <option>Самосвал (М 975 АМ 186)</option>
            <option>Самосвал (М 964 АМ 186)</option>
            <option>Мультилифт (К 500 МР 186) + № 1</option>
            <option>Мультилифт (К 500 МР 186) + № 2</option>
            <option>Мультилифт (К 500 МР 186) + № 3</option>
            <option>Мультилифт (К 500 МР 186) + № 4</option>
            <option>Мультилифт (К 500 МР 186) + КГО</option>
            <option>Мультилифт (Х 348 ЕМ 186) + № 1</option>
            <option>Мультилифт (Х 348 ЕМ 186) + № 2</option>
            <option>Мультилифт (Х 348 ЕМ 186) + № 3</option>
            <option>Мультилифт (Х 348 ЕМ 186) + № 4</option>
            <option>Мультилифт (Х 348 ЕМ 186) + КГО</option>
            <option>Мультилифт (У 820 НУ 55) + № 1</option>
            <option>Мультилифт (У 820 НУ 55) + № 2</option>
            <option>Мультилифт (У 820 НУ 55) + № 3</option>
            <option>Мультилифт (У 820 НУ 55) + № 4</option>
            <option>Мультилифт (У 820 НУ 55) + № 6</option>
            <option>Мультилифт (У 820 НУ 55) + КГО</option>
            <option>Мультилифт (У 152 ОВ 55) + № 1</option>
            <option>Мультилифт (У 152 ОВ 55) + № 2</option>
            <option>Мультилифт (У 152 ОВ 55) + № 3</option>
            <option>Мультилифт (У 152 ОВ 55) + № 4</option>
            <option>Мультилифт (У 152 ОВ 55) + № 6</option>
            <option>Мультилифт (У 152 ОВ 55) + КГО</option>
        </select>`,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: '<i class="flaticon-checked-1"></i> Далее →',
        cancelButtonText: '<i class="flaticon-cancel-circle"></i> Отмена',
        padding: '2em'
    });

    const weighingSwal2 = window.Swal.mixin({
        icon: 'info',
        title: 'Выберите тип отходов',
        progressSteps: steps,
        html: `<select class="form-select form-select-lg">
            <option selected disabled>Выберите значение</option>
            <option>Остатки сортировки ТКО при совместном сборе 4-й класс (отсев)</option>
            <option>Остатки сортировки ТКО при совместном сборе практически неопасные 5-й класс (Хвосты)</option>
            <option>Остатки сортировки ТКО при совместном сборе практически неопасные 5-й класс (ТКО на захоронение)</option>
            <option>Измельченные КГО</option>
        </select>`,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: '<i class="flaticon-checked-1"></i> Далее →',
        cancelButtonText: '<i class="flaticon-cancel-circle"></i> Отмена',
        padding: '2em'
    });

    const swalQueueStep = window.Swal.mixin({
        confirmButtonText: '<i class="flaticon-checked-1"></i> Далее →',
        cancelButtonText: '<i class="flaticon-cancel-circle"></i> Отмена',
        showCancelButton: true,
        progressSteps: steps,
        input: 'number',
        inputAttributes: {
            required: true,
            min: '0',
        },
        validationMessage: 'Обязательно для заполнения!',
        padding: '2em'
    });

    const values = [];
    let currentStep;

    for (currentStep = 0; currentStep < steps.length;) {
        if (currentStep == 0) {
            const result = await weighingSwal.fire(
                {
                    currentProgressStep: currentStep
                }
            );
            if (result.dismiss === window.Swal.DismissReason.cancel) break;
            currentStep++
            continue
        } else if (currentStep == 1) {
            const result = await weighingSwal2.fire(
                {
                    currentProgressStep: currentStep
                }
            );
            if (result.dismiss === window.Swal.DismissReason.cancel) break;
            currentStep++
            continue
        } else {
            const result = await swalQueueStep.fire({
                title: `Введите вес`,
                text: currentStep == 0 ? 'Chaining swal2 modals is easy.' : '',
                inputValue: values[currentStep],
                showCancelButton: currentStep > 0,
                currentProgressStep: currentStep
            });
            if (result.value) {
                values[currentStep] = result.value;
                currentStep++;
                new window.Swal('Взвешивание', 'Данные успешно сохранены.', 'success');
            } else if (result.dismiss === window.Swal.DismissReason.cancel) {
                break;
            }
        }
    };

}

</script>

<template>
    <teleport to="#breadcrumb">
        <div class="navbar-nav flex-row ms-auto">
            <button type="button" class="btn btn-outline-primary me-4" @click="weightingButton">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="feather feather-download me-2" data-v-5522efca="">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Взвешивание
            </button>
            <button type="button" class="btn btn-primary me-4" @click="isOpen = !isOpen">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="feather feather-plus me-2" data-v-02c2cbc4="">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                {{ props.modalTitle }}
            </button>
        </div>
    </teleport>

    <div class="right-side-modal" :class="{ active: isOpen }">
        <div class="sidbarchat p-3" tag="div">
            <a class="btn-close" href="javascript:;" @click="isOpen = !isOpen"> </a>
            <h5 class="rs-modal-title"> {{ props.modalTitle }} </h5>

            <slot />

        </div>
    </div>
</template>