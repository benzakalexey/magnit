<script setup>
import { onMounted, ref } from 'vue';
import { useStore } from 'vuex';
const store = useStore();

const menu_collapse = ref('dashboard');

onMounted(() => {
    const selector = document.querySelector('#sidebar a[href="' + window.location.pathname + '"]');
    if (selector) {
        const ul = selector.closest('ul.collapse');
        if (ul) {
            let ele = ul.closest('li.menu').querySelectorAll('.dropdown-toggle');
            if (ele) {
                ele = ele[0];
                setTimeout(() => {
                    ele.click();
                });
            }
        } else {
            selector.click();
        }
    }
});

const toggleMobileMenu = () => {
    if (window.innerWidth < 991) {
        store.commit('toggleSideBar', !store.state.is_show_sidebar);
    }
};
const links = {
    polygon: ['Контролер'],
    trucks: ['Супервайзер', 'Логист'],
    tonars: ['Супервайзер', 'Аналитик тонаров', 'Редактор тонаров'],
    garbage_trucks: ['Супервайзер', 'Аналитик мусоровозов'],
    visits: ['Супервайзер'],
};

</script>

<template>
    <!--  BEGIN SIDEBAR  -->
    <div class="sidebar-wrapper sidebar-theme">
        <nav ref="menu" id="sidebar">
            <div class="shadow-bottom"></div>

            <perfect-scrollbar class="list-unstyled menu-categories" tag="ul"
                :options="{ wheelSpeed: 0.5, swipeEasing: !0, minScrollbarLength: 40, maxScrollbarLength: 300, suppressScrollX: true }">
                <div class="pt-4"></div>
                <li v-show="links.polygon.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/polygon" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-map-pin" data-v-5522efca="">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            <span>{{ $t('polygon') }}</span>
                        </div>
                    </router-link>
                </li>

                <li v-show="links.visits.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/visits" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-home" data-v-5522efca="">
                                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                                <polyline points="9 22 9 12 15 12 15 22"></polyline>
                            </svg>
                            <span>{{ $t('visits') }}</span>
                        </div>
                    </router-link>
                </li>

                <li v-show="links.trucks.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/trucks" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-truck" data-v-5522efca="">
                                <rect x="1" y="3" width="15" height="13"></rect>
                                <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                                <circle cx="5.5" cy="18.5" r="2.5"></circle>
                                <circle cx="18.5" cy="18.5" r="2.5"></circle>
                            </svg>
                            <span>{{ $t('trucks') }}</span>
                        </div>
                    </router-link>
                </li>

                <li v-show="links.tonars.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/tonars" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-layers">
                                <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                                <polyline points="2 17 12 22 22 17"></polyline>
                                <polyline points="2 12 12 17 22 12"></polyline>
                            </svg>
                            <span>{{ $t('tonars') }}</span>
                        </div>
                    </router-link>
                </li>

                <li v-show="links.garbage_trucks.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/garbage_trucks" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-box" data-v-5522efca="">
                                <path
                                    d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z">
                                </path>
                                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                                <line x1="12" y1="22.08" x2="12" y2="12"></line>
                            </svg>
                            <span>{{ $t('garbage_trucks') }}</span>
                        </div>
                    </router-link>
                </li>

        </perfect-scrollbar>
    </nav>
</div>
<!--  END SIDEBAR  --></template>