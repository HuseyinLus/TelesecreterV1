import { useState } from 'react'
import { useDoctors } from '../hooks/useDoctors'
import { useAppointments } from '../hooks/useAppointments'
import CalendarToolbar from '../components/calendar/CalendarToolbar'
import WeekCalendar from '../components/calendar/WeekCalendar'
import DoctorLegend from '../components/calendar/DoctorLegend'

function getWeekLabel() {
  const now = new Date()
  const mon = new Date(now)
  mon.setDate(now.getDate() - ((now.getDay() + 6) % 7))
  const sun = new Date(mon)
  sun.setDate(mon.getDate() + 6)
  const fmt = (d) => d.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })
  return `${fmt(mon)} – ${fmt(sun).split(' ')[1]}, ${sun.getFullYear()}`
}

export default function CalendarPage() {
  const [view, setView]         = useState('week')
  const [filters, setFilters]   = useState({ doctorId: 'all' })
  const [selected, setSelected] = useState(null)

  const { data: doctors = [] }      = useDoctors()
  const { data: appointments = [] } = useAppointments()

  return (
    <div style={{ padding: '0 24px 24px', overflow: 'auto', height: '100%' }}>
      <CalendarToolbar
        view={view} onView={setView}
        filters={filters} setFilters={setFilters}
        doctors={doctors}
        weekLabel={getWeekLabel()}
      />

      {view === 'week' && (
        <WeekCalendar
          appointments={appointments}
          doctors={doctors}
          filters={filters}
          selectedId={selected?.id}
          onSelect={setSelected}
        />
      )}
      {view !== 'week' && (
        <div style={{ padding: 32, textAlign: 'center', color: 'var(--color-ink-3)', fontSize: 13 }}>
          {view === 'day' ? 'Day view — Module 13' : 'List view — Module 13'}
        </div>
      )}

      <DoctorLegend doctors={doctors} />
    </div>
  )
}
