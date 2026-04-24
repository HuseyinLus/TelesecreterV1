import { useDoctors } from '../hooks/useDoctors'
import { useDepartments } from '../hooks/useDepartments'

const COL = '1fr 1fr 1fr 1fr 1fr 1fr'

const HeadCell = ({ children }) => (
  <div style={{ fontSize: 10.5, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', fontWeight: 500 }}>
    {children}
  </div>
)

export default function DoctorsPage() {
  const { data: doctors = [], isLoading: loadingDoctors } = useDoctors()
  const { data: departments = [], isLoading: loadingDepts } = useDepartments()

  const deptById = Object.fromEntries(departments.map((d) => [d.id, d.name]))

  const loading = loadingDoctors || loadingDepts

  return (
    <div style={{ padding: '24px', height: '100%', overflow: 'auto' }}>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ margin: 0, fontFamily: 'var(--font-serif)', fontSize: 24, fontWeight: 400, color: 'var(--color-ink)', letterSpacing: '-0.01em' }}>Doctors</h2>
        <p style={{ margin: '4px 0 0', fontSize: 13, color: 'var(--color-ink-3)' }}>{doctors.length} registered</p>
      </div>

      <div style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 14, overflow: 'hidden' }}>
        <div style={{ display: 'grid', gridTemplateColumns: COL, gap: 14, padding: '10px 18px', background: 'var(--color-surface-2)', borderBottom: '1px solid var(--color-border)' }}>
          <HeadCell>ID</HeadCell>
          <HeadCell>Name</HeadCell>
          <HeadCell>Surname</HeadCell>
          <HeadCell>Phone</HeadCell>
          <HeadCell>Email</HeadCell>
          <HeadCell>Department</HeadCell>
        </div>

        {loading && (
          <div style={{ padding: '32px', textAlign: 'center', color: 'var(--color-ink-4)', fontSize: 13 }}>Loading…</div>
        )}

        {!loading && doctors.length === 0 && (
          <div style={{ padding: '32px', textAlign: 'center', color: 'var(--color-ink-4)', fontSize: 13 }}>No doctors found</div>
        )}

        {!loading && doctors.map((doc) => {
          const parts = (doc.full_name ?? '').trim().split(' ')
          const name = parts[0] ?? '—'
          const surname = parts.slice(1).join(' ') || '—'

          return (
            <div
              key={doc.id}
              style={{ display: 'grid', gridTemplateColumns: COL, gap: 14, padding: '11px 18px', alignItems: 'center', fontSize: 13, borderBottom: '1px solid var(--color-border)', transition: 'background 0.1s' }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'var(--color-bg-subtle)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
            >
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--color-ink-3)' }} title={doc.id}>{String(doc.id).slice(0, 8)}…</div>
              <div style={{ fontWeight: 600, color: 'var(--color-ink)' }}>{name}</div>
              <div style={{ color: 'var(--color-ink-2)' }}>{surname}</div>
              <div style={{ color: 'var(--color-ink-2)', fontVariantNumeric: 'tabular-nums' }}>{doc.phone_number || '—'}</div>
              <div style={{ color: 'var(--color-ink-2)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{doc.email}</div>
              <div style={{ color: 'var(--color-ink-2)' }}>{deptById[doc.department_id] ?? '—'}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
