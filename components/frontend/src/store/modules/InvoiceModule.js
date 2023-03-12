import { InvoiceAPI } from "@/api/invoiceAPI";

export const InvoiceModule = {
    namespaced: true,
    state() {
        return {
            invoice: null
        }
    },

    getters: {
        invoice: (state) => state.invoice,
    },

    mutations: {
        setInvoice(state, data) {
            state.invoice = {
                date: new Date(data.date).toLocaleDateString('ru'),
                planned_time: new Date(data.planned_date).toLocaleString('ru', {timeStyle: 'short'}),
                time: new Date(data.date).toLocaleString('ru', {timeStyle: 'short'}),
                number: data.number,
                cargo_type: data.cargo_type,
                receiver: data.receiver,
                direction: data.direction,
                volume: data.volume,
                carrier: data.carrier,
                driver: data.driver,
                driver_licence: data.driver_licence,
                truck: data.truck,
                truck_number: data.truck_number,
                truck_volume: data.truck_volume,
                truck_weight: data.truck_weight,
                contract: data.contract,
                polygon: data.polygon,
            }
        },

        deleteInvoice(state) {
            state.invoice = null
        },
    },

    actions: {
        async get({ commit }, { visit_id }) {
            try {
                const res = await InvoiceAPI.get(visit_id);
                commit('setInvoice', res.data);
            } catch (err) {
                throw err;
            }
        },
    },
}