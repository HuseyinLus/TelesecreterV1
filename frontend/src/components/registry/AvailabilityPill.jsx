import { useDoctorAvailability } from '../../hooks/useDoctorAvailability'

export default function AvailabilityPill({ doctorId }) {
  const dateStr = new Date().toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' }).replace('/', '.')
  const { data, isLoading } = useDoctorAvailability(doctorId, dateStr)

  if (isLoading) return (
    <span style={{ display: 'inline-block', width: 72, height: 22, borderRadius: 5, background: 'var(--color-border)', animation: 'pulse-sage 1.5s infinite' }} />
  )

  const available = data?.available
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', padding: '2px 8px', borderRadius: 5, fontSize: 11, fontWeight: 500,
      background: available ? 'var(--color-sage-soft)' : 'oklch(66% 0.11 20 / 0.1)',
      color: available ? 'var(--color-sage-ink)' : 'var(--color-rose)',
      border: `1px solid ${available ? 'oklch(62% 0.07 160 / 0.28)' : 'oklch(66% 0.11 20 / 0.25)'}`,
    }}>
      {available ? 'Available' : 'Booked'}
    </span>
  )
}
