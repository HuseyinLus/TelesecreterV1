import { useQuery } from '@tanstack/react-query'
import { useRef, useEffect } from 'react'
import apiClient from '../services/apiClient'
import { POLLING_INTERVAL_APPOINTMENTS } from '../utils/constants'

export function useAppointments(onNewEntry) {
  const prevLengthRef = useRef(null)

  const query = useQuery({
    queryKey: ['appointments'],
    queryFn: () => apiClient.get('/appointments/').then((r) => r.data),
    refetchInterval: POLLING_INTERVAL_APPOINTMENTS,
  })

  useEffect(() => {
    if (!query.data) return
    const len = query.data.length
    if (prevLengthRef.current !== null && len > prevLengthRef.current) {
      onNewEntry?.()
    }
    prevLengthRef.current = len
  }, [query.data])

  return query
}
