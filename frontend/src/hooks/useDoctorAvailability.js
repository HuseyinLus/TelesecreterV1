import { useQuery } from '@tanstack/react-query'
import apiClient from '../services/apiClient'
import { POLLING_INTERVAL_AVAILABILITY } from '../utils/constants'

export function useDoctorAvailability(doctorId, dateStr) {
  return useQuery({
    queryKey: ['availability', doctorId, dateStr],
    queryFn: () => apiClient.get(`/scheduales/${doctorId}/availability`, { params: { date_str: dateStr } }).then((r) => r.data),
    refetchInterval: POLLING_INTERVAL_AVAILABILITY,
    enabled: Boolean(doctorId && dateStr),
  })
}
