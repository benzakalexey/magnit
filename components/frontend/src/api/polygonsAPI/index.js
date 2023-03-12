import { DefaultAPIInstance } from "@/api";

export const PolygonsAPI = {
    /**
     * 
     * @returns {Promise<AxiosResponse<any>>}
     */
    get_directions(polygon_id) {
        const url = 'polygons/directions';
        return DefaultAPIInstance.get(url + '?polygon_id=' + polygon_id);
    },
}