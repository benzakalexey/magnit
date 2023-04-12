import { DefaultAPIInstance } from "@/api";

export const TrucksAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_all() {
        const url = 'trucks/get_all';
        return DefaultAPIInstance.get(url);
    },

    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_models() {
        const url = 'trucks/get_models';
        return DefaultAPIInstance.get(url);
    },

    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_types() {
        const url = 'trucks/get_types';
        return DefaultAPIInstance.get(url);
    },

    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_trailers() {
        const url = 'trucks/get_trailers';
        return DefaultAPIInstance.get(url);
    },

    /**Получить информацию по номеру пропуска
     * 
     * @param {number} num 
     * @returns 
     */
    get_by_num(num) {
        const url = 'trucks/get_all';
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
        const url = 'trucks/history';
        return DefaultAPIInstance.get(url, {
            params: {
                num: num
            }
        });
    },
    /**Добавить визит
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    add(
        model,
        reg_number,
        type,
        tara,
        max_weight,
        production_year,
        body_volume,
        compress_ratio,
        permit_exp,
        carrier,
        trailer,
        is_tonar,
    ) {
        const url = 'trucks/add'
        const data = {
            model,
            reg_number,
            type,
            tara,
            max_weight,
            production_year,
            body_volume,
            compress_ratio,
            permit_exp,
            carrier,
            trailer,
            is_tonar,
        };
        return DefaultAPIInstance.post(url, data);
    }
}