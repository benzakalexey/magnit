import { VisitsAPI } from "@/api/visitsAPI";

export const VisitsModule = {
    namespaced: true,
    state() {
        return {
            visits: []
        }
    },

    getters: {
        visits: (state) => state.visits,
    },

    mutations: {
        setVisits(state, data) {
            state.visits = data;
        },

        deleteItem(state, id, reason) {
            let visit = state.visits.find(i => i.id == id);
            visit.status = 2
        },
    },

    actions: {
        async update({ commit }) {
            try {
                const res = await VisitsAPI.get_all();
                commit('setVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        
        async delete({commit}, { id, reason }) { 
            await VisitsAPI.delete(id, reason);
            return commit('deleteItem', id, reason);
        }
    },
}