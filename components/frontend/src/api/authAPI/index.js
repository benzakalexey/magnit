import { LoginAPIInstance, DefaultAPIInstance } from "@/api";

export const AuthAPI = {
    /**
     * 
     * @param {string} login 
     * @param {string} password 
     * @returns {Promise<AxiosResponse<any>>}
     */
    login(login, password) {
        const url = 'login';
        const data = { login, password };
        return LoginAPIInstance.post(url, data);
    },

    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    logout() {
        const url = 'login';
        return DefaultAPIInstance.post(url);
    },
}