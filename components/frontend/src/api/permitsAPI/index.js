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
                num: num
            }
        });
    },
    
    /**Получить информацию по номеру пропуска
     * 
     * @param {number} num 
     * @returns 
     */
    get_history(num) {
        const url = 'permits/history';
        return DefaultAPIInstance.get(url, {
            params: {
                num: num
            }
        });
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
    }
}