<script setup>
import { ref } from 'vue';
import { useMeta } from '@/composables/use-meta';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import '@/assets/sass/authentication/auth-boxed.scss';

useMeta({ title: 'Вход' });

const router = useRouter();
const route = useRoute();
const store = useStore();

const pwd_type = ref('password');

const set_pwd_type = () => {
    if (pwd_type.value === 'password') {
        pwd_type.value = 'text';
    } else {
        pwd_type.value = 'password';
    }
};

const login = ref('')
const password = ref('')
const err_show = ref(false)

const onSubmit = () => {
    const redirectTo = route.redirectedFrom || '/'
    store.dispatch('AuthModule/onLogin', {
        login: login.value,
        password: password.value,
    })
        .then(() => { router.push(redirectTo) })
        .catch(() => {
            err_show.value = true;
        })
}
</script>

<template>
    <div class="form auth-boxed">
        <div class="form-container outer">
            <div class="form-form">
                <div class="form-form-wrap">
                    <div class="form-container">
                        <div class="form-content">
                            <h1 class="">Вход</h1>
                            <p class="">Введите логин и пароль чтобы продолжить.</p>

                            <form class="text-start" novalidate @submit.prevent="onSubmit">
                                <div class="form">
                                    <div id="username-field" class="field-wrapper input">
                                        <label for="username">ТЕЛЕФОН</label>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                            stroke-linecap="round" stroke-linejoin="round" class="feather feather-user">
                                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                            <circle cx="12" cy="7" r="4"></circle>
                                        </svg>
                                        <input v-model="login" type="text" class="form-control"
                                            v-maska="'#(###) ###-####'" placeholder="(___) ___-____"
                                            :class="[err_show ? 'is-invalid' : '']" />
                                    </div>

                                    <div id="password-field" class="field-wrapper input mb-2">
                                        <div class="d-flex justify-content-between">
                                            <label for="password">ПАРОЛЬ</label>
                                            <router-link to="/auth/pass-recovery-boxed" class="forgot-pass-link">Забыли
                                                пароль?</router-link>
                                        </div>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                            stroke-linecap="round" stroke-linejoin="round" class="feather feather-lock">
                                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                                            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                                        </svg>
                                        <input :type="pwd_type" v-model="password" class="form-control"
                                            placeholder="Пароль" :class="[err_show ? 'is-invalid' : '']" />
                                        <div class="invalid-feedback">Неверный номер телефона или пароль!</div>
                                        <svg @click="set_pwd_type" xmlns="http://www.w3.org/2000/svg" width="24"
                                            height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                            stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                            id="toggle-password" class="feather feather-eye">
                                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                            <circle cx="12" cy="12" r="3"></circle>
                                        </svg>
                                    </div>
                                    <div class="d-sm-flex justify-content-between">
                                        <div class="field-wrapper">
                                            <button class="btn btn-primary">Войти</button>
                                        </div>
                                    </div>

                                    <p class="signup-link">Не зарегистрированы ? <router-link to="/auth/register">
                                            Создать аккаунт</router-link>
                                    </p>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
