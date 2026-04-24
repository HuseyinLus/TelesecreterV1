import { useState } from 'react'
import { useDoctors } from '../hooks/useDoctors'
import { useAppointments } from '../hooks/useAppointments'
import CalendarToolbar from '../components/calendar/CalendarToolbar'
import WeekCalendar from '../components/calendar/WeekCalendar'
import DayView from '../components/calendar/DayView'
import ListView from '../components/calendar/ListView'
import DoctorLegend from '../components/calendar/DoctorLegend'
import AppointmentDrawer from '../components/calendar/AppointmentDrawer'
import TodayAgenda from '../components/calendar/TodayAgenda'
import AIStatsCard from '../components/calendar/AIStatsCard'

function getMondayOf(date) {
  const d = new Date(date)
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7))
  return d
}

function getLabel(view, baseDate) {
  if (view === 'week') {
    const mon = getMondayOf(baseDate)
    const sun = new Date(mon)
    sun.setDate(mon.getDate() + 6)
    const fmt = (d) => d.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })
    return `${fmt(mon)} – ${fmt(sun).split(' ')[1]}, ${sun.getFullYear()}`
  }
  return baseDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })
}

export default function CalendarPage() {
  const [view, setView]         = useState('week')
  const [filters, setFilters]   = useState({ doctorId: 'all' })
  const [selected, setSelected] = useState(null)
  const [baseDate, setBaseDate] = useState(new Date())

  const { data: doctors = [] }      = useDoctors()
  const { data: appointments = [] } = useAppointments()

  const navigate = (delta) => {
    setBaseDate((prev) => {
      const d = new Date(prev)
      d.setDate(d.getDate() + (view === 'week' ? delta * 7 : delta))
      return d
    })
  }

  const handleViewChange = (v) => {
    setView(v)
    setBaseDate(new Date())
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 360px', height: '100%', overflow: 'hidden' }}>
      {/* Main calendar area */}
      <div style={{ overflow: 'auto', padding: '0 24px 24px' }}>
        <CalendarToolbar
          view={view} onView={handleViewChange}
          filters={filters} setFilters={setFilters}
          doctors={doctors}
          label={getLabel(view, baseDate)}
          onPrev={() => navigate(-1)}
          onNext={() => navigate(1)}
          onToday={() => setBaseDate(new Date())}
        />

        {view === 'week' && <WeekCalendar appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} baseDate={baseDate} />}
        {view === 'day'  && <DayView     appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} baseDate={baseDate} />}
        {view === 'list' && <ListView    appointments={appointments} doctors={doctors} filters={filters} selectedId={selected?.id} onSelect={setSelected} />}

        <DoctorLegend doctors={doctors} />
      </div>

      {/* Right rail */}
      <div style={{ overflow: 'auto', borderLeft: '1px solid var(--color-border)', display: 'flex', flexDirection: 'column', gap: 14, padding: '18px 16px' }}>
        <TodayAgenda appointments={appointments} doctors={doctors} selectedId={selected?.id} onSelect={setSelected} />
        <AIStatsCard />
      </div>

      <AppointmentDrawer appt={selected} doctors={doctors} onClose={() => setSelected(null)} />
    </div>
  )
}
