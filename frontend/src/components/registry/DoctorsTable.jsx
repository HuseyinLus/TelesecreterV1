import { getDoctorColor } from '../../utils/constants'
import AvailabilityPill from './AvailabilityPill'

const COL_WIDTHS = '2fr 1.5fr 1.5fr 100px'

const HeadCell = ({ children }) => (
  <div style={{ fontSize: 10.5, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', fontWeight: 500 }}>{children}</div>
)

export default function DoctorsTable({ doctors }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'grid', gridTemplateColumns: COL_WIDTHS, gap: 14, padding: '10px 18px', background: 'var(--color-surface-2)', borderBottom: '1px solid var(--color-border)' }}>
        <HeadCell>Name</HeadCell>
        <HeadCell>Specialty</HeadCell>
        <HeadCell>Department</HeadCell>
        <HeadCell>Today</HeadCell>
      </div>
      {doctors.map((doc, i) => {
        const color = getDoctorColor(i)
        const initials = (doc.full_name ?? '?').split(' ').filter(w => w).slice(0, 2).map(w => w[0]).join('')
        return (
          <div key={doc.id} style={{ display: 'grid', gridTemplateColumns: COL_WIDTHS, gap: 14, padding: '10px 18px', borderBottom: '1px solid var(--color-border)', alignItems: 'center', fontSize: 12.5 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ width: 28, height: 28, borderRadius: '50%', background: `var(--color-${color})`, color: 'white', display: 'grid', placeItems: 'center', fontSize: 10, fontWeight: 600, flexShrink: 0 }}>{initials}</div>
              <span style={{ color: 'var(--color-ink)', fontWeight: 600 }}>{doc.full_name}</span>
            </div>
            <span style={{ color: 'var(--color-ink-2)' }}>{doc.specialty}</span>
            <span style={{ color: 'var(--color-ink-3)' }}>{doc.department_name ?? '—'}</span>
            <AvailabilityPill doctorId={doc.id} />
          </div>
        )
      })}
    </div>
  )
}
