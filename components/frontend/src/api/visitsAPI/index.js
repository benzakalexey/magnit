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
}