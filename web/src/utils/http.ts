import axios from 'axios'

const http = axios.create({
  baseURL: '/api/'
})

http.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
  }
  return config
}, error => {
  return Promise.reject(error)
})

http.interceptors.response.use(res => {
  return res
}, error => {
  return Promise.reject(error)
})

export default http