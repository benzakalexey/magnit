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
    garbage_trucks: ['Супервайзер', 'Аналитик мусоровозов', 'Аналитик тонаров', 'Логист'],
    visits: ['Супервайзер'],
    users: ['Супервайзер'],
    contragents: ['Супервайзер'],
    polygons: ['Супервайзер'],
    drivers_single: ['Логист', 'Аналитик тонаров', 'Редактор тонаров'],
    drivers: ['Супервайзер'],
    contracts: ['Супервайзер'],
    catalog: ['Супервайзер'],
    fill_invoice: ['Супервайзер', 'Печать ТН'],
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
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-map-pin" data-v-5522efca="">
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
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-home" data-v-5522efca="">
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
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-truck" data-v-5522efca="">
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
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-layers">
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
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-box" data-v-5522efca="">
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

                <li v-show="links.drivers_single.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/drivers" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-users">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="9" cy="7" r="4"></circle>
                                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                            </svg>
                            <span>{{ $t('drivers') }}</span>
                        </div>
                    </router-link>
                </li>

                <li v-show="links.catalog.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <a class="dropdown-toggle" data-bs-toggle="collapse" data-bs-target="#components"
                        aria-controls="components" aria-expanded="false">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-list" data-v-5522efca="">
                                <line x1="8" y1="6" x2="21" y2="6"></line>
                                <line x1="8" y1="12" x2="21" y2="12"></line>
                                <line x1="8" y1="18" x2="21" y2="18"></line>
                                <line x1="3" y1="6" x2="3.01" y2="6"></line>
                                <line x1="3" y1="12" x2="3.01" y2="12"></line>
                                <line x1="3" y1="18" x2="3.01" y2="18"></line>
                            </svg>
                            <span>{{ $t('catalog') }}</span>
                        </div>
                        <div>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-chevron-right">
                                <polyline points="9 18 15 12 9 6"></polyline>
                            </svg>
                        </div>
                    </a>

                    <ul id="components" class="collapse submenu list-unstyled" data-bs-parent="#sidebar">
                        <li v-show="links.users.includes(store.state.AuthModule.credentials.user_role)">
                            <router-link to="/users" class="dropdown-toggle" @click="toggleMobileMenu">
                                {{ $t('users') }}
                            </router-link>
                        </li>
                        <li v-show="links.drivers.includes(store.state.AuthModule.credentials.user_role)">
                            <router-link to="/drivers" class="dropdown-toggle" @click="toggleMobileMenu">
                                {{ $t('drivers') }}
                            </router-link>
                        </li>
                        <li v-show="links.contragents.includes(store.state.AuthModule.credentials.user_role)">
                            <router-link to="/contragents" class="dropdown-toggle" @click="toggleMobileMenu">
                                {{ $t('contragents') }}
                            </router-link>
                        </li>
                        <li v-show="links.polygons.includes(store.state.AuthModule.credentials.user_role)">
                            <router-link to="/polygons" class="dropdown-toggle" @click="toggleMobileMenu">
                                {{ $t('polygons') }}
                            </router-link>
                        </li>
                    </ul>
                </li>

                <li v-show="links.fill_invoice.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/fill_invoice" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="feather feather-printer" data-v-5522efca="">
                                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2">
                                </path>
                                <rect x="6" y="14" width="12" height="8"></rect>
                            </svg>
                            <span>{{ $t('fill_invoice') }}</span>
                        </div>
                    </router-link>
                </li>

                <!--

                <li v-show="links.users.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/users" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-users" data-v-5522efca="">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="9" cy="7" r="4"></circle>
                                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                            </svg>
                            <span>{{ $t('users') }}</span>
                        </div>
                    </router-link>
                </li>

                <li v-show="links.contragents.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/contragents" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-shield" data-v-5522efca="">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                            </svg>
                            <span>{{ $t('contragents') }}</span>
                        </div>
                    </router-link>
                </li>

                <li v-show="links.polygons.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/polygons" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-grid" data-v-5522efca="">
                                <rect x="3" y="3" width="7" height="7"></rect>
                                <rect x="14" y="3" width="7" height="7"></rect>
                                <rect x="14" y="14" width="7" height="7"></rect>
                                <rect x="3" y="14" width="7" height="7"></rect>
                            </svg>
                            <span>{{ $t('polygons') }}</span>
                        </div>
                    </router-link>
                </li>

                <li v-show="links.drivers.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/drivers" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-github" data-v-5522efca="">
                                <path
                                    d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22">
                                </path>
                            </svg>
                            <span>{{ $t('drivers') }}</span>
                        </div>
                    </router-link>
                </li> 
                <li v-show="links.contracts.includes(store.state.AuthModule.credentials.user_role)" class="menu">
                    <router-link to="/contracts" class="dropdown-toggle" @click="toggleMobileMenu">
                        <div class="">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="feather feather-clipboard" data-v-5522efca="">
                                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                                <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                            </svg>
                            <span>{{ $t('contracts') }}</span>
                        </div>
                    </router-link>
                </li> -->

            </perfect-scrollbar>
        </nav>
    </div>
    <!--  END SIDEBAR  -->
</template>