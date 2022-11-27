import { DefaultAPIInstance } from "@/api";
import { AuthAPI } from "@/api/authAPI";

export const AuthModule = {
    namespaced: true,
    state() {
        return {
            credentials: {
                token: localStorage.getItem('token') || null,
                user_role: localStorage.getItem('user_role') || null,
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

        deleteToken(state) {
            state.credentials.token = null;
            localStorage.removeItem('token')
        },

        deleteUserRole(state) {
            state.credentials.user_role = null;
            localStorage.removeItem('user_role')
        },
    },

    actions: {
        onLogin({ commit }, { login, password }) {
            AuthAPI.login({ login, password }).then((res) => {
                commit('setToken', res.token);
                commit('setUserRole', res.user_role);
                DefaultAPIInstance.defaults.headers['authorization'] = `Bearer ${res.token}`;
            }).catch(
                () => {
                    commit('setToken', 'defaultSecurityToken');
                    commit('setUserRole', 'defaultSecurityUserRole');
                    DefaultAPIInstance.defaults.headers['authorization'] = 'Bearer defaultSecurityToken';
                }
            )
        },

        onLogout({ commit }) {
            commit('deleteToken');
            commit('deleteUserRole');
            delete DefaultAPIInstance.defaults.headers['authorization'];
        }
    }
}
