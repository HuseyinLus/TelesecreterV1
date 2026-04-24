import { useQuery } from '@tanstack/react-query'
import apiClient from '../services/apiClient'

export function useDepartments() {
  return useQuery({
    queryKey: ['departments'],
    queryFn: () => apiClient.get('/departments/').then((r) => r.data),
  })
}
