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
                        'added_at': u.added_at ? new Date(u.added_at) : '',
                        'added_by': u.added_by,
                        'full_name': u.full_name,
                        'id': u.id,
                        'is_active': u.is_active,
                        'is_staff': u.is_staff,
                        'first_name': u.name,
                        'patronymic': u.patronymic,
                        'phone': formatPhoneNumber(u.phone),
                        'polygon': u.polygon,
                        'polygon_id': u.polygon_id,
                        'role': u.role,
                        'surname': u.surname,
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
                const res = await PolygonsAPI.get();
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