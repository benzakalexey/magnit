import { DriversAPI } from "@/api/driversAPI";

export const DriversModule = {
    namespaced: true,
    state() {
        return {
            drivers: [],
        }
    },

    getters: {
        drivers: (state) => state.drivers,
    },

    mutations: {
        setDrivers(state, data) {
            let drivers = []
            function formatPhoneNumber(tenDigitsPhone) {
                var inputNumbersValue = tenDigitsPhone.split(/\D/g).join('').slice(-10),
                    formattedInputValue = "";
            
                if (["7", "8", "9"].indexOf(inputNumbersValue[0]) > -1) {
                    if (inputNumbersValue[0] == "9") inputNumbersValue = "7" + inputNumbersValue;
                    var firstSymbols = (inputNumbersValue[0] == "8") ? "8" : "+7";
                    formattedInputValue = firstSymbols + " ";
                    if (inputNumbersValue.length > 1) {
                        formattedInputValue += '(' + inputNumbersValue.substring(1, 4);
                    }
                    if (inputNumbersValue.length >= 5) {
                        formattedInputValue += ') ' + inputNumbersValue.substring(4, 7);
                    }
                    if (inputNumbersValue.length >= 8) {
                        formattedInputValue += '-' + inputNumbersValue.substring(7, 9);
                    }
                    if (inputNumbersValue.length >= 10) {
                        formattedInputValue += '-' + inputNumbersValue.substring(9, 11);
                    }
                } else {
                    formattedInputValue = '+' + inputNumbersValue.substring(0, 16);
                }
                return formattedInputValue;
            }
            for (var u of data) {
                drivers.push(
                    {
                        first_name: u.surname,
                        last_name: u.name,
                        patronymic: u.patronymic,
                        driver_id: u.id,
                        full_name: u.full_name,
                        license: u.license,
                        employer: u.employer,
                        employer_id: u.employer_id,
                    }
                )
            };
            state.drivers = drivers
        },
    },

    actions: {
        async update({ commit }) {
            try {
                const res = await DriversAPI.get_all();
                commit('setVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async reset_password({ commit }) {
            try {
                const res = await DriversAPI.reset_password();
                commit('setVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async get_all({ commit }) {
            try {
                const res = await DriversAPI.get_all();
                commit('setDrivers', res.data);
            } catch (err) {
                throw err;
            }
        },
        async create({ commit }, { permission_id, weight, truck_number, service_contract_id }) {
            return await DriversAPI.add(permission_id, weight, truck_number, service_contract_id);
            // commit('deleteItem', id, reason);
        },
    },
}