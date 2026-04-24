import { useQuery } from '@tanstack/react-query'
import apiClient from '../services/apiClient'
import { POLLING_INTERVAL_DOCTORS } from '../utils/constants'

export function useDoctors() {
  return useQuery({
    queryKey: ['doctors'],
    queryFn: () => apiClient.get('/doctors/').then((r) => r.data),
    refetchInterval: POLLING_INTERVAL_DOCTORS,
  })
}
