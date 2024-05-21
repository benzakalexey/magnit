import { DefaultAPIInstance } from "@/api";

export const PolygonsAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_directions(polygon_id, contragent_id) {
        const url = 'polygons/directions';
        return DefaultAPIInstance.get(url + '?polygon_id=' + polygon_id + '&contragent_id=' + contragent_id);
    },
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_all() {
        const url = 'polygons/get_all';
        return DefaultAPIInstance.get(url);
    },
    /** Обновить данные водителя
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    update(data) {
        const url = 'polygons/update';
        return DefaultAPIInstance.post(url, data);
    },
    /** Обновить данные пользователя
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    create(data) {
        const url = 'polygons/add';
        return DefaultAPIInstance.post(url, data);
    },
}