import { useQuery } from '@tanstack/react-query'
import apiClient from '../services/apiClient'

export function useToday() {
  return useQuery({
    queryKey: ['today'],
    queryFn: () => apiClient.get('/today').then((r) => r.data.date),
    staleTime: 60_000 * 60,
  })
}
