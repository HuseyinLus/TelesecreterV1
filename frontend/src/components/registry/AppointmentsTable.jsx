import { Calendar } from 'lucide-react'
import AppointmentRow from './AppointmentRow'
import EmptyState from '../shared/EmptyState'

const COL_WIDTHS = '1.2fr 1.5fr 90px 110px 90px 90px'

const HeadCell = ({ children }) => (
  <div style={{ fontSize: 10.5, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', fontWeight: 500 }}>{children}</div>
)

export default function AppointmentsTable({ appointments }) {
  if (!appointments.length) return <EmptyState icon={Calendar} title="No appointments booked yet" subtitle="They will appear here the moment the AI agent confirms a booking." />

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'grid', gridTemplateColumns: COL_WIDTHS, gap: 14, padding: '10px 18px', background: 'var(--color-surface-2)', borderBottom: '1px solid var(--color-border)' }}>
        <HeadCell>Patient ID</HeadCell>
        <HeadCell>Doctor ID</HeadCell>
        <HeadCell>Date</HeadCell>
        <HeadCell>Start</HeadCell>
        <HeadCell>End</HeadCell>
        <HeadCell>Status</HeadCell>
      </div>
      {appointments.map((appt) => <AppointmentRow key={appt.id} appt={appt} />)}
    </div>
  )
}
