import axios from "axios";

const LoginConfig = {
    baseURL: process.env.VUE_APP_API_URL,
    headers: {
        'ContentType': 'application/json',
    }
}

export const LoginAPIInstance = axios.create(LoginConfig);

const defaultConfig = {
    baseURL: process.env.VUE_APP_API_URL,
    headers: {
        'Content-Type': 'application/json',
    }
}

// const token = localStorage.getItem('token');
// if (token) defaultConfig.headers['authorization'] = `Bearer ${token}`

export const DefaultAPIInstance = axios.create(defaultConfig);

