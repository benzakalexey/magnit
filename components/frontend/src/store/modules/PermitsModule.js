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
                truck_model: null,
                truck_type: null,
                reg_number: null,
                contragent: null,
                expired_at: null,
                is_valid: null,
                tara: null,
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
                    permit_status: p.permit_status,
                    permission_id: p.permission_id,
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
                permit_status: data.permit_status,
                permission_id: data.permission_id,
                truck_model: data.truck_model,
                truck_type: data.truck_type,
                reg_number: data.reg_number,
                contragent: data.contragent_name,
                expired_at: data.expired_at,
                is_valid: data.is_valid,
                tara: data.tara,
                max_weight: data.max_weight,
            }
        },
        clearCheckPermitData(state) {
            state.check_permit.truck_model = null
            state.check_permit.permit_status = null
            state.check_permit.permission_id = null
            state.check_permit.truck_type = null
            state.check_permit.reg_number = null
            state.check_permit.contragent = null
            state.check_permit.expired_at = null
            state.check_permit.is_valid = null
            state.check_permit.tara = null
            state.check_permit.max_weight = null
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
        async check({ commit }, { number }) {
            return await PermitsAPI.check(number)
            .then((res) => commit('setCheckPermitData', res.data))
            .catch((err) => {
                commit('clearCheckPermitData');
                throw err;
            });
        },
    }
}
