import { DefaultAPIInstance } from "@/api";
import { PermitsAPI } from "@/api/permitsAPI";

const pretty_num = (n) => {
    if (n) {
        let r = n.match(/[а-яА-Я]+|[0-9]+/g);
        return r.join(' ');
    }

    return n
}

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
                days_before_exp: null,
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
                service_contract_id: data.service_contract_id,
                truck_model: data.truck_model,
                truck_type: data.truck_type,
                reg_number: pretty_num(data.reg_number),
                contragent: data.contragent_name,
                expired_at: data.expired_at,
                days_before_exp: data.days_before_exp,
                is_valid: data.is_valid,
                is_tonar: data.is_tonar,
                tara: data.tara,
                max_weight: data.max_weight,
            }
        },
        clearCheckPermitData(state) {
            state.check_permit.permit_num = null
            state.check_permit.permit_status = null
            state.check_permit.permission_id = null
            state.check_permit.service_contract_id = null
            state.check_permit.truck_model = null
            state.check_permit.truck_type = null
            state.check_permit.reg_number = null
            state.check_permit.contragent = null
            state.check_permit.expired_at = null
            state.check_permit.days_before_exp = null
            state.check_permit.is_valid = null
            state.check_permit.is_tonar = null
            state.check_permit.tara = null
            state.check_permit.max_weight = null
        },
        setPermitHistory(state, data) {
            var histoty = []
            for (var i of data) {
                histoty.push(
                    {
                        contragent_name: i.contragent_name,
                        expired_at: new Date(i.expired_at),
                        added_at: new Date(i.added_at),
                        days_before_exp: i.days_before_exp,
                        permission_id: i.permission_id,
                        permit_status: i.permit_status,
                        is_valid: i.is_valid,
                        is_tonar: i.is_tonar,
                    }
                )
            };
            state.permit_histoty = histoty;
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
            return await PermitsAPI.get_history(num)
                .then((res) => commit('setPermitHistory', res.data))
                .catch((err) => {
                    commit('clearPermitHistory')
                    throw err;
                });
        },
        async check({ commit }, { number }) {
            return await PermitsAPI.check(number)
                .then((res) => commit('setCheckPermitData', res.data))
                .catch((err) => {
                    commit('clearCheckPermitData');
                    throw err;
                });
        },
        async clear_check({ commit }) {
            commit('clearCheckPermitData');
        },
        async add_permission({ commit }, {
            permit,
            permit_exp,
            carrier,
            trailer,
            is_tonar,
            truck_type,
            tara,
            max_weight,
            body_volume,
        }) {
            return await PermitsAPI.add_permission(
                permit,
                permit_exp,
                carrier,
                trailer,
                is_tonar,
                truck_type,
                tara,
                max_weight,
                body_volume,
            );
            // commit('deleteItem', id, reason);
        }
    }
}
