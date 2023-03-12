import { DefaultAPIInstance } from "@/api";

export const VisitsAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_all() {
        const url = 'visits/get';
        return DefaultAPIInstance.get(url);
    },
    /**Пометить визит как удаленный
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    delete(visit_id, reason) {
        const url = 'visits/delete'
        const data = { visit_id, reason };
        return DefaultAPIInstance.post(url, data);
    },
    /**Пометить визит как удаленный
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    finish(visit_id, weight, driver_id, contract_id) {
        const url = 'visits/finish'
        const data = { visit_id, weight, driver_id, contract_id };
        return DefaultAPIInstance.post(url, data);
    },
    /**Добавить визит
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    add(permission_id, weight) {
        const url = 'visits/add'
        const data = { permission_id, weight };
        return DefaultAPIInstance.post(url, data);
    }
}