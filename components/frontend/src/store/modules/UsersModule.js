import { UsersAPI } from "@/api/usersAPI";

export const UsersModule = {
    namespaced: true,
    state() {
        return {
            users: [],
        }
    },

    getters: {
        users: (state) => state.users,
    },

    mutations: {
        setUsers(state, data) {
            let users = []
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
                users.push(
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
            state.users = users
        },
    },

    actions: {
        async update({ commit }) {
            try {
                const res = await UsersAPI.get_all();
                commit('setVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async reset_password({ commit }) {
            try {
                const res = await UsersAPI.reset_password();
                commit('setVisits', res.data);
            } catch (err) {
                throw err;
            }
        },
        async get({ commit }) {
            try {
                const res = await UsersAPI.get();
                commit('setUsers', res.data);
            } catch (err) {
                throw err;
            }
        },
        async create({ commit }, { permission_id, weight, truck_number, service_contract_id }) {
            return await UsersAPI.add(permission_id, weight, truck_number, service_contract_id);
            // commit('deleteItem', id, reason);
        },
    },
}