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
            let visits = []
            for (var v of data) {
                visits.push(
                    {
                        id: v['id'],
                        permit: v['permit'],
                        is_deleted: v['is_deleted'],
                        delete_reason: v['delete_reason'],
                        contragent_id: v['contragent_id'],
                        tonar: v['tonar'],
                        carrier: v['carrier'],
                        invoice_num: v['invoice_num'],
                        truck_model: v['truck_model'],
                        truck_type: v['truck_type'],
                        tara: v['tara'],
                        netto: v['netto'],
                        brutto: v['brutto'],
                        max_weight: v['max_weight'],
                        reg_number: v['reg_number'],
                        weight_in: v['weight_in'],
                        checked_in: new Date(v['checked_in']).toLocaleString('ru'),
                        weight_out: v['weight_out'],
                        checked_out: new Date(v['checked_out']).toLocaleString('ru'),
                        driver_name: v['driver_name'],
                        destination: v['destination'],
                        status: v['status']
                    }
                )
            };   
            state.visits = visits         
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
        
        async delete({commit}, { visit_id, reason }) { 
            return await VisitsAPI.delete(visit_id, reason);
            // commit('deleteItem', id, reason);
        },
        
        async add({commit}, { permission_id, weight }) { 
            return await VisitsAPI.add(permission_id, weight);
            // commit('deleteItem', id, reason);
        }
    },
}