import { DefaultAPIInstance } from "@/api";

export const VisitsAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_all() {
        const url = 'visits.json';
        return DefaultAPIInstance.get(url);
    },
    /**Пометить визит как удаленный
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    delete(id, reason) {
        const url = 'visits/delete'
        const data = { id, reason };
        return DefaultAPIInstance.post(url, data);
    }
}