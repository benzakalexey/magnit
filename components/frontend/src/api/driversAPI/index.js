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
}