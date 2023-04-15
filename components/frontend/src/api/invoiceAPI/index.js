import { DefaultAPIInstance } from "@/api";

export const InvoiceAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get(visit_id) {
        const url = 'visits/get_invoice';
        const data = { visit_id };
        return DefaultAPIInstance.get(url + '?visit_id=' + visit_id);
    },
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_akt(visit_id) {
        const url = 'visits/get_akt';
        const data = { visit_id };
        return DefaultAPIInstance.get(url + '?visit_id=' + visit_id);
    },
}