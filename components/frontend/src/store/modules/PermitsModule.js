import { DefaultAPIInstance } from "@/api";
import { PermitsAPI } from "@/api/permitsAPI";

export const PermitsModule = {
    namespaced: true,
    state() {
        return {
            permits: [],
            permit_histoty: [],
            check_permit: {
                permit_num: null,
                vehicle_num: null,
                vehicle_type: null,
                vehicle_mark: null,
                contragent: null,
                expired_at: null,
                is_active: null,
                days_before_exp: null,
                min_weight: null,
                max_weight: null,
            }
        }
    },

    getters: {
        getPermits: (state) => state.permits,
    },

    mutations: {
        setPermitsData(state, data) {
            for (var p of data) {
                state.permits.push({
                    permit_num: p.permit_num,
                    vehicle_num: p.vehicle_num,
                    vehicle_type: p.vehicle_type,
                    vehicle_mark: p.vehicle_mark,
                    contragent: p.contragent,
                    expired_at: p.expired_at,
                    is_active: p.is_active,
                    days_before_exp: p.days_before_exp,
                    min_weight: p.min_weight,
                    max_weight: p.max_weight,
                });
            };
        },
        clearPermitsData(state) {
            state.permits = []
        },
        setCheckPermitData(state, data) {
            state.check_permit = {
                permit_num: data.permit_num,
                vehicle_num: data.vehicle_num,
                vehicle_type: data.vehicle_type,
                vehicle_mark: data.vehicle_mark,
                contragent: data.contragent,
                expired_at: data.expired_at,
                is_active: data.is_active,
                days_before_exp: data.days_before_exp,
                min_weight: data.min_weight,
                max_weight: data.max_weight,
            }
        },
        clearCheckPermitData(state) {
            state.check_permit = {
                permit_num: null,
                vehicle_num: null,
                vehicle_type: null,
                vehicle_mark: null,
                contragent: null,
                expired_at: null,
                is_active: null,
                days_before_exp: null,
                min_weight: null,
                max_weight: null,
            }
        },
        setPermitHistory(state, data) {
            for (var i in data) {
                state.permit_histoty.push(
                    {
                        added_at: i.added_at,
                        expired_at: i.expired_at,
                        contragent: i.contragent,
                    }
                )
            }
        },
        clearPermitHistory(state) {
            state.permit_histoty = []
        },
    },

    actions: {
        async get_all({ commit }) {
            try {
                const res = await PermitsAPI.get_all();
                commit('setPermitsData', res.data);
            } catch (err) {
                commit('clearPermitsData');
                throw err;
            }
        },
        async get_history({ commit }, { num }) {
            try {
                const res = await PermitsAPI.get_history(num);
                commit('setPermitHistory', res.data);
            } catch (err) {
                commit('clearPermitHistory')
                throw err;
            }

        },
    }
}
