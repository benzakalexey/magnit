import { DefaultAPIInstance } from "@/api";
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
        update({ commit }) {
            VisitsAPI.get_all()
                .then((res) => {
                    commit('setVisits', res.data)
                }).catch((err) => {
                    console.error(err.message)
                })
        },
        
        async delete({commit}, { id, reason }) { 
            await VisitsAPI.delete(id, reason);
            return commit('deleteItem', id, reason);
        }
    },
}