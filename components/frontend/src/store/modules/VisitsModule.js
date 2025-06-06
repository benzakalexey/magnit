import { VisitsAPI } from "@/api/visitsAPI";

export const VisitsModule = {
    namespaced: true,
    state() {
        return {
            visits: [],
            tonar_visits: [],
            garbage_truck_visits: [],
            akts: [],
            polygon: null,
        }
    },

    getters: {
        visits: (state) => state.visits,
        polygon: (state) => state.polygon,
        tonar_visits: (state) => state.tonar_visits,
        garbage_truck_visits: (state) => state.garbage_truck_visits,
        akts: (state) => state.akts,
    },

    mutations: {
        setVisits(state, data) {
            let visits = []
            const pretty_num = (n) => {
                let r = n.match(/[а-яА-Я]+|[0-9]+/g);
                return r.join(' ');
            }
            if (data.length > 0) state.polygon = data[0].polygon + ' полигон'

            for (var v of data) {

                visits.push(
                    {
                        id: v.id,
                        permit: v.permit,
                        is_deleted: v.is_deleted,
                        delete_reason: v.delete_reason,
                        contragent_id: v.contragent_id,
                        polygon: v.polygon,
                        polygon_id: v.polygon_id,
                        scale_accuracy: v.scale_accuracy,
                        tonar: v.tonar,
                        carrier: v.carrier,
                        invoice_num: v.invoice_num,
                        truck_model: v.truck_model,
                        truck_type: v.truck_type,
                        tara: v.tara,
                        netto: v.netto,
                        lot: v.lot,
                        lot_id: v.lot ? v.lot.id : v.lot,
                        brutto: v.brutto,
                        max_weight: v.max_weight,
                        reg_number: pretty_num(v.reg_number),
                        weight_in: v.weight_in,
                        checked_in: new Date(v.checked_in),
                        weight_out: v.weight_out,
                        checked_out: v.checked_out ? new Date(v.checked_out) : v.checked_out,
                        driver_name: v.driver_name,
                        destination: v.destination,
                        driver_id: v.driver_id,
                        contract_id: v.contract_id,
                        status: v.status
                    }
                )
            };
            state.visits = visits
        },
        setTonarVisits(state, data) {
            let visits = []
            const pretty_num = (n) => {
                let r = n.match(/[а-яА-Я]+|[0-9]+/g);
                return r.join(' ');
            };
            for (var v of data) {

                visits.push(
                    {
                        id: v.id,
                        permit: v.permit,
                        is_deleted: v.is_deleted,
                        delete_reason: v.delete_reason,
                        contragent_id: v.contragent_id,
                        polygon_id: v.polygon_id,
                        polygon: v.polygon,
                        scale_accuracy: v.scale_accuracy,
                        tonar: v.tonar,
                        carrier: v.carrier,
                        invoice_num: v.invoice_num,
                        truck_model: v.truck_model,
                        truck_type: v.truck_type,
                        tara: v.tara,
                        netto: v.netto,
                        brutto: v.brutto,
                        max_weight: v.max_weight,
                        reg_number: pretty_num(v.reg_number),
                        weight_in: v.weight_in,
                        checked_in: new Date(v.checked_in),
                        weight_out: v.weight_out,
                        checked_out: v.checked_out ? new Date(v.checked_out) : v.checked_out,
                        driver_name: v.driver_name,
                        driver_id: v.driver_id,
                        contract_id: v.contract_id,
                        destination: v.destination,
                        status: v.status
                    }
                )
            };
            state.tonar_visits = visits
        },
        setGarbageTruckVisits(state, data) {
            let visits = []
            const pretty_num = (n) => {
                let r = n.match(/[а-яА-Я]+|[0-9]+/g);
                return r.join(' ');
            };
            for (var v of data) {

                visits.push(
                    {
                        id: v.id,
                        permit: v.permit,
                        is_deleted: v.is_deleted,
                        delete_reason: v.delete_reason,
                        contragent_id: v.contragent_id,
                        polygon_id: v.polygon_id,
                        polygon: v.polygon,
                        scale_accuracy: v.scale_accuracy,
                        tonar: v.tonar,
                        carrier: v.carrier,
                        invoice_num: v.invoice_num,
                        truck_model: v.truck_model,
                        truck_type: v.truck_type,
                        tara: v.tara,
                        netto: v.netto,
                        lot: v.lot,
                        lot_id: v.lot ? v.lot.id : v.lot,
                        brutto: v.brutto,
                        max_weight: v.max_weight,
                        reg_number: pretty_num(v.reg_number),
                        weight_in: v.weight_in,
                        checked_in: new Date(v.checked_in),
                        weight_out: v.weight_out,
                        checked_out: v.checked_out ? new Date(v.checked_out) : v.checked_out,
                        driver_name: v.driver_name,
                        destination: v.destination,
                        frozen: v.frozen,
                        status: v.status
                    }
                )
            };
            state.garbage_truck_visits = visits
        },
        setAkts(state, data) {
            console.log(data)
            localStorage.setItem('akts', JSON.stringify(data));
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
        async get_visits({ commit }, { after, before }) {

            try {
                const res = await VisitsAPI.get_visits(after, before);
                commit('setVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async update_tonars({ commit }, { after, before }) {

            try {
                const res = await VisitsAPI.get_tonars(after, before);
                commit('setTonarVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async update_garbage_trucks({ commit }, { after, before }) {

            try {
                const res = await VisitsAPI.get_garbage_trucks(after, before);
                commit('setGarbageTruckVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async delete({ commit }, { visit_id, reason }) {
            return await VisitsAPI.delete(visit_id, reason);
            // commit('deleteItem', id, reason);
        },
        async finish({ commit }, { visit_id, weight_out, driver_id, contract_id }) {
            return await VisitsAPI.finish(visit_id, weight_out, driver_id, contract_id);
            // commit('deleteItem', id, reason);
        },
        async add({ commit }, { permission_id, weight, truck_number, lot, service_contract_id }) {
            return await VisitsAPI.add(permission_id, weight, truck_number, lot, service_contract_id);
            // commit('deleteItem', id, reason);
        },
        async update_visit({ commit }, data) {
            return await VisitsAPI.update(data);
        },
        async bulk_tonars_update({ commit }, data) {
            return await VisitsAPI.bulk_tonars_update(data);
        },
        async bulk_update({ commit }, data) {
            return await VisitsAPI.bulk_update(data);
        },
        async upload_tonars_data({ commit }, file) {
            return await VisitsAPI.upload_tonars_data(file);
        },
        setAkts({ commit }, data) {
            commit('setAkts', data);
        }
    },
}