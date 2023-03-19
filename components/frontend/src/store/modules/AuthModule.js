import { DefaultAPIInstance } from "@/api";
import { AuthAPI } from "@/api/authAPI";

export const AuthModule = {
    namespaced: true,
    state() {
        return {
            credentials: {
                token: localStorage.getItem('token') || null,
                user_role: localStorage.getItem('user_role') || null,
            },
            user: {
                first_name: localStorage.getItem('first_name') || null,
                last_name: localStorage.getItem('last_name') || null,
                phone_number: localStorage.getItem('phone_number') || null,
                polygon: localStorage.getItem('polygon') || null,
            }
        }
    },

    getters: {
        getUserRole: (state) => state.credentials.user_role,
    },

    mutations: {
        setToken(state, token) {
            state.credentials.token = token;
            localStorage.setItem('token', token);
        },

        setUserRole(state, user_role) {
            state.credentials.user_role = user_role;
            localStorage.setItem('user_role', user_role);
        },

        setUserData(state, first_name, last_name, phone_number) {
            state.user.first_name = first_name;
            state.user.last_name = last_name;
            state.user.phone = phone_number;
            localStorage.setItem('first_name', first_name);
            localStorage.setItem('last_name', last_name);
            localStorage.setItem('phone_number', phone_number);
        },

        deleteToken(state) {
            state.credentials.token = null;
            localStorage.removeItem('token')
        },

        deleteUserRole(state) {
            state.credentials.user_role = null;
            localStorage.removeItem('user_role')
        },

        deleteUserData(state) {
            state.user.first_name = null;
            state.user.last_name = null;
            state.user.phone = null;
            localStorage.removeItem('first_name');
            localStorage.removeItem('last_name');
            localStorage.removeItem('phone');
        },
    },

    actions: {
        onLogin({ commit }, { login, password }) {
            return AuthAPI.login(login, password)
                .then((res) => {
                    commit('setToken', res.data.token);
                    commit('setUserRole', res.data.user_role);
                    commit('setUserData', res.data.first_name, res.data.last_name, res.data.phone_number);
                    DefaultAPIInstance.defaults.headers['Authorization'] = `Bearer ${res.data.token}`;
                })
                .catch(
                    () => {
                        commit('deleteToken');
                        commit('deleteUserRole');
                        commit('deleteUserData');
                        delete DefaultAPIInstance.defaults.headers['Authorization'];
                        throw 'Authentication error' // TODO implement specify error 
                    }
                )
        },

        onLogout({ commit }) {
            commit('deleteToken');
            commit('deleteUserRole');
            commit('deleteUserData');
            delete DefaultAPIInstance.defaults.headers['Authorization'];
        }
    }
}
