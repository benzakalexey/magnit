import { DefaultAPIInstance } from "@/api";
import { PartnersAPI } from "@/api/partnersAPI";

const pretty_num = (n) => {
    let r = n.match(/[а-яА-Я]+|[0-9]+/g);
    return r.join(' ');
}

export const PartnersModule = {
    namespaced: true,
    state() {
        return {
            partners: [],
            models: [],
        }
    },

    getters: {
        partners: (state) => state.partners,
    },

    mutations: {
        setPartnersData(state, data) {
            let partners = []
            for (var p of data) {
                partners.push({
                    id: p.id,
                    inn: p.inn,
                    ogrn: p.ogrn,
                    name: p.name,
                    short_name: p.short_name,
                    kpp: p.kpp,
                    address: p.address,
                    phone: p.phone,
                    bank: p.bank,
                    settlement_account: p.settlement_account,
                    correspondent_account: p.correspondent_account,
                    e_mail: p.e_mail,
                    valid_from: p.valid_from ? new Date(p.valid_from) : null,
                    valid_to: p.valid_to ? new Date(p.valid_to) : null,
                });
            };
            state.partners = partners;
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
    },

    actions: {
        async update({ commit }) {
            try {
                const res = await PartnersAPI.get_all();
                commit('setPartnersData', res.data);
            } catch (err) {
                throw err;
            }
        },
        async update_models({ commit }) {
            try {
                const res = await PartnersAPI.get_models();
                commit('setModelsData', res.data);
            } catch (err) {
                throw err;
            }
        },
        async update_types({ commit }) {
            try {
                const res = await PartnersAPI.get_types();
                commit('setTypesData', res.data);
            } catch (err) {
                throw err;
            }
        },
        async get({ commit }) {
            try {
                const res = await PartnersAPI.get_all();
                commit('setPartnersData', res.data);
            } catch (err) {
                throw err;
            }
        },
        async create({ commit }, data) {
            return await PartnersAPI.add(data);
        },
    }
}
