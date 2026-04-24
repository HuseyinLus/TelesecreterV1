import { useState } from 'react'
import { Database } from 'lucide-react'
import { useDoctors } from '../../hooks/useDoctors'
import { useAppointments } from '../../hooks/useAppointments'
import DoctorsTable from './DoctorsTable'
import AppointmentsTable from './AppointmentsTable'

export default function RegistryPanel() {
  const [tab, setTab] = useState('doctors')
  const [newFlash, setNewFlash] = useState(false)

  const { data: doctors = [], isLoading: loadingDoctors } = useDoctors()
  const { data: appointments = [], isLoading: loadingAppts } = useAppointments(() => {
    setNewFlash(true)
    setTimeout(() => setNewFlash(false), 2000)
  })

  const Tab = ({ id, label, count }) => (
    <button
      onClick={() => setTab(id)}
      style={{
        padding: '6px 14px', borderRadius: 7, fontSize: 12.5, fontWeight: 500, border: 'none', cursor: 'pointer',
        background: tab === id ? 'var(--color-bg-subtle)' : 'transparent',
        color: tab === id ? 'var(--color-ink)' : 'var(--color-ink-3)',
        boxShadow: tab === id ? '0 1px 2px oklch(20% 0.04 240 / 0.05)' : 'none',
        outline: id === 'appointments' && newFlash ? '2px solid var(--color-accent)' : 'none',
        transition: 'all 0.15s',
      }}
    >
      {label}
      {count != null && (
        <span style={{ marginLeft: 6, background: 'var(--color-accent)', color: 'white', fontSize: 10, fontWeight: 600, padding: '1px 6px', borderRadius: 10 }}>{count}</span>
      )}
    </button>
  )

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 18px', borderBottom: '1px solid var(--color-border)', flexShrink: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Database size={15} color="var(--color-ink-3)" />
          <span style={{ fontSize: 12, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-3)' }}>Registry</span>
        </div>
        <div style={{ display: 'flex', background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 9, padding: 3, gap: 2 }}>
          <Tab id="doctors"      label="Doctors"      count={doctors.length} />
          <Tab id="appointments" label="Appointments" count={appointments.length} />
        </div>
      </div>

      <div style={{ flex: 1, overflowY: 'auto' }}>
        {tab === 'doctors' && (
          loadingDoctors
            ? <div style={{ padding: 24, color: 'var(--color-ink-3)', fontSize: 12 }}>Loading doctors…</div>
            : <DoctorsTable doctors={doctors} />
        )}
        {tab === 'appointments' && (
          loadingAppts
            ? <div style={{ padding: 24, color: 'var(--color-ink-3)', fontSize: 12 }}>Loading appointments…</div>
            : <AppointmentsTable appointments={appointments} />
        )}
      </div>
    </div>
  )
}
