import { DefaultAPIInstance } from "@/api";

export const UsersAPI = {
    /** Получить всех пользователей
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get() {
        const url = 'users/get_all';
        return DefaultAPIInstance.get(url);
    },
    /** Получить роли пользователей
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_user_roles() {
        const url = 'users/get_user_roles';
        return DefaultAPIInstance.get(url);
    },
    /** Обновить данные пользователя
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    update(data) {
        const url = 'users/update';
        return DefaultAPIInstance.post(url, data);
    },
    /** Обновить данные пользователя
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    create(data) {
        const url = 'users/add';
        return DefaultAPIInstance.post(url, data);
    },
    /** Обновить
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    updp(data) {
        const url = 'users/updp';
        return DefaultAPIInstance.post(url, data);
    },
}