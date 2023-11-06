import { DefaultAPIInstance } from "@/api";

export const DriversAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get(partner_id) {
        const url = 'drivers/get_by_partner';
        return DefaultAPIInstance.get(url + '?partner_id=' + partner_id);
    },
    /** Получить всех водителей
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_all() {
        const url = 'drivers/get_all';
        return DefaultAPIInstance.get(url);
    },
    /** Обновить данные водителя
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    update(data) {
        const url = 'drivers/update';
        return DefaultAPIInstance.post(url, data);
    },
    /** Обновить данные пользователя
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    create(data) {
        const url = 'drivers/add';
        return DefaultAPIInstance.post(url, data);
    },
}