import { DefaultAPIInstance, UploadFileInstance } from "@/api";

export const VisitsAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_all() {
        const url = 'visits/get';
        return DefaultAPIInstance.get(url);
    },
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_tonars(after, before) {
        const url = 'visits/get_tonars';
        const data = { after, before };
        return DefaultAPIInstance.get(url, { params: data });
    },
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_garbage_trucks(after, before) {
        const url = 'visits/get_garbage_trucks';
        const data = { after, before };
        return DefaultAPIInstance.get(url, { params: data });
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
    },
    /**Добавить визит
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    update(
        weight_in,
        weight_out,
        visit_id,
        driver_id,
        contract_id,
    ) {
        const url = 'visits/update'
        const data = {
            weight_in,
            weight_out,
            visit_id,
            driver_id,
            contract_id,
        };
        // console.log(data)
        return DefaultAPIInstance.post(url, data);
    },
    /**Добавить визит
     *      
     * @param {number} id 
     * @param {string} reason 
     * @returns {Promise<AxiosResponse<any>>}
     */
    bulk_tonars_update(data) {
        const url = 'visits/bulk_tonars_update'
        // const data = {
        //     weight_in,
        //     weight_out,
        //     visit_id,
        //     driver_id,
        //     contract_id,
        // };
        // console.log(data)
        return DefaultAPIInstance.post(url, data);
    },
    upload_tonars_data(file) {
        const url = 'visits/upload_tonars_data'
        return UploadFileInstance.post(url, {data: file});
    },
}