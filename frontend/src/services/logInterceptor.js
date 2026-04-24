import { useLogStore } from '../store/logStore'

export function attachLogInterceptor(client) {
  client.interceptors.request.use((config) => {
    config._logStart = performance.now()
    config._logMethod = config.method?.toUpperCase()
    config._logPath   = config.url
    return config
  })

  client.interceptors.response.use(
    (response) => {
      useLogStore.getState().pushLog({
        timestamp:    new Date(),
        method:       response.config._logMethod,
        path:         response.config._logPath,
        statusCode:   response.status,
        requestBody:  response.config.data ? JSON.parse(response.config.data) : null,
        responseBody: response.data,
        durationMs:   Math.round(performance.now() - response.config._logStart),
      })
      return response
    },
    (error) => {
      useLogStore.getState().pushLog({
        timestamp:    new Date(),
        method:       error.config?._logMethod,
        path:         error.config?._logPath,
        statusCode:   error.response?.status ?? 0,
        requestBody:  error.config?.data ? JSON.parse(error.config.data) : null,
        responseBody: error.response?.data ?? { message: error.message },
        durationMs:   Math.round(performance.now() - (error.config?._logStart ?? performance.now())),
      })
      return Promise.reject(error)
    }
  )
}
