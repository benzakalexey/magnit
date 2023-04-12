import { DefaultAPIInstance } from "@/api";

export const PermitsAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_all() {
        const url = 'permits/get_all';
        return DefaultAPIInstance.get(url);
    },

    /**Получить информацию по номеру пропуска
     * 
     * @param {number} num 
     * @returns 
     */
    get_by_num(num) {
        const url = 'permits/get_all';
        return DefaultAPIInstance.get(url, {
            params: {
                num: { num }
            }
        });
    },

    /**Получить информацию по номеру пропуска
     * 
     * @param {number} num 
     * @returns 
     */
    async get_history(num) {
        const url = 'permits/history';
        const data = { num };
        return await DefaultAPIInstance.get(url, { params: data });
    },

    /**Получить информацию по номеру пропуска
     * 
     * @param {number} num 
     * @returns 
     */
    async check(number) {
        const url = 'permits/check';
        const data = { number };
        return await DefaultAPIInstance.get(url, { params: data });
    },

    /**Пометить визит как удаленный
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    delete(id, reason) {
        const url = 'permits/delete'
        const data = { id, reason };
        return DefaultAPIInstance.post(url, data);
    },

    /**Пометить визит как удаленный
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    add_permission(
        permit,
        permit_exp,
        carrier,
        trailer,
        is_tonar,
    ) {
        const url = 'permits/add_permission'
        const data = {
            permit,
            permit_exp,
            carrier,
            trailer,
            is_tonar,
        };
        return DefaultAPIInstance.post(url, data);
    }
}