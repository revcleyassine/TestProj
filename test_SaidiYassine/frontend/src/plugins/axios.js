import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // we need to change this in order to use envirnement variables to facilitate docker integration
  headers: {
    'Content-Type': 'application/json'
  }
})

export default axiosInstance