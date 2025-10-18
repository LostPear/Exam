import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'

export const api = axios.create({
  baseURL,
  withCredentials: true,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (error) => {
    const message = error?.response?.data?.detail || error?.response?.data?.message || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)
