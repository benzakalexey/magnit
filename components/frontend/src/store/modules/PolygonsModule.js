import { PolygonsAPI } from "@/api/polygonsAPI";

export const PolygonsModule = {
    namespaced: true,
    state() {
        return {
            polygons: [],
        }
    },

    getters: {
        polygons: (state) => state.polygons,
    },

    mutations: {
        setPolygons(state, data) {
            let polygons = []
            for (var u of data) {
                polygons.push(
                    {
                        polygon_id: u.id,
                        name: u.name,
                        address: u.address,
                        scale_accuracy: u.scale_accuracy,
                        valid_from: u.valid_from ? new Date(u.valid_from) : null,
                        valid_to: u.valid_to ? new Date(u.valid_to) : null,
                    }
                )
            };
            state.polygons = polygons
        },
    },

    actions: {
        async update({ commit }) {
            try {
                const res = await PolygonsAPI.get_all();
                commit('setVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async reset_password({ commit }) {
            try {
                const res = await PolygonsAPI.reset_password();
                commit('setVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async get({ commit }) {
            try {
                const res = await PolygonsAPI.get_all();
                commit('setPolygons', res.data);
            } catch (err) {
                throw err;
            }
        },
        async create({ commit }, { permission_id, weight, truck_number, service_contract_id }) {
            return await PolygonsAPI.add(permission_id, weight, truck_number, service_contract_id);
            // commit('deleteItem', id, reason);
        },
    },
}