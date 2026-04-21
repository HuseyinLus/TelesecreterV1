import axios from 'axios'
import { API_BASE_URL } from '../utils/constants'
import { attachLogInterceptor } from './logInterceptor'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10_000,
})

attachLogInterceptor(apiClient)

export default apiClient
