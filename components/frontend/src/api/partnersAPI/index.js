import { DefaultAPIInstance } from "@/api";

export const PartnersAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_all() {
        const url = 'partners/get_all';
        return DefaultAPIInstance.get(url);
    },
    
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_models() {
        const url = 'partners/get_models';
        return DefaultAPIInstance.get(url);
    },
    
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_types() {
        const url = 'partners/get_types';
        return DefaultAPIInstance.get(url);
    },
    
    /**Получить информацию по номеру пропуска
     * 
     * @param {number} num 
     * @returns 
     */
    get_by_num(num) {
        const url = 'partners/get_all';
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
    get_history(num) {
        const url = 'partners/history';
        return DefaultAPIInstance.get(url, {
            params: {
                num: num
            }
        });
    },
    /** Обновить данные водителя
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    update(data) {
        const url = 'partners/update';
        return DefaultAPIInstance.post(url, data);
    },
    /** Обновить данные пользователя
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    create(data) {
        const url = 'partners/add';
        return DefaultAPIInstance.post(url, data);
    },
}