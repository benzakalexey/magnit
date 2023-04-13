import { DefaultAPIInstance } from "@/api";
import { TrucksAPI } from "@/api/trucksAPI";

const pretty_num = (n) => {
    let r = n.match(/[а-яА-Я]+|[0-9]+/g);
    return r.join('\u2009');
}

export const TrucksModule = {
    namespaced: true,
    state() {
        return {
            trucks: [],
            models: [],
            types: [],
            trailers: [],
        }
    },

    getters: {
        trucks: (state) => state.trucks,
    },

    mutations: {
        setTrucksData(state, data) {
            let trucks = []
            for (var t of data) {
                trucks.push({
                    id: t.id,
                    truck_model: t.truck_model,
                    reg_number: pretty_num(t.reg_number),
                    truck_type: t.truck_type,
                    tara: t.tara,
                    trailer: t.trailer,
                    tonar: t.tonar,
                    max_weight: t.max_weight,
                    permit: t.permit,
                    permission_owner: t.permission_owner,
                    started_at: t.started_at ? new Date(t.started_at) : t.started_at,
                    expired_at: t.expired_at ? new Date(t.expired_at) : t.expired_at,
                    days_before_exp: t.days_before_exp,
                    body_volume: t.body_volume,
                    status: t.status,
                });
            };
            state.trucks = trucks;
        },
        setModelsData(state, data) {
            let models = []
            for (var m of data) {
                models.push({
                    id: m.id,
                    name: m.name,
                });
            };
            state.models = models;
        },
        setTypesData(state, data) {
            state.types = data;
        },
        setTrailersData(state, data) {
            let trailers = []
            for (var m of data) {
                trailers.push({
                    model: m.model,
                    reg_number: m.reg_number,
                    tara: m.tara,
                    id: m.id,
                });
            };
            state.trailers = trailers;
        },
    },

    actions: {
        async update({ commit }) {
            try {
                const res = await TrucksAPI.get_all();
                commit('setTrucksData', res.data);
            } catch (err) {
                throw err;
            }
        },
        async update_models({ commit }) {
            try {
                const res = await TrucksAPI.get_models();
                commit('setModelsData', res.data);
            } catch (err) {
                throw err;
            }
        },
        async update_types({ commit }) {
            try {
                const res = await TrucksAPI.get_types();
                commit('setTypesData', res.data);
            } catch (err) {
                throw err;
            }
        },
        async update_trailers({ commit }) {
            try {
                const res = await TrucksAPI.get_trailers();
                commit('setTrailersData', res.data);
            } catch (err) {
                throw err;
            }
        },
        async add({ commit }, {
            model,
            reg_number,
            type,
            tara,
            max_weight,
            production_year,
            body_volume,
            permit_exp,
            carrier,
            trailer,
            is_tonar,
        }) {
            return await TrucksAPI.add(
                model,
                reg_number,
                type,
                tara,
                max_weight,
                production_year,
                body_volume,
                permit_exp,
                carrier,
                trailer,
                is_tonar,
            );
        }
    }
}
