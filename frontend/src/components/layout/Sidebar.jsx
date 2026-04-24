import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Calendar, Stethoscope, Users, Phone, Settings } from 'lucide-react'

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/calendar',  label: 'Calendar',  icon: Calendar },
  { to: '/doctors',   label: 'Doctors',   icon: Stethoscope },
  { to: '/patients',  label: 'Patients',  icon: Users },
]

export default function Sidebar() {
  return (
    <aside style={{
      width: 232,
      display: 'flex',
      flexDirection: 'column',
      padding: '18px 14px',
      background: 'var(--color-surface)',
      borderRight: '1px solid var(--color-border)',
      gap: 4,
      height: '100vh',
      flexShrink: 0,
    }}>
      {/* Brand */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '6px 8px 14px', marginBottom: 6, borderBottom: '1px solid var(--color-border)' }}>
        <div style={{ width: 32, height: 32, background: 'var(--color-accent)', color: 'white', borderRadius: 9, display: 'grid', placeItems: 'center' }}>
          <Phone size={16} />
        </div>
        <div>
          <div style={{ fontWeight: 600, fontSize: 13.5, color: 'var(--color-ink)' }}>Telesecreter</div>
          <div style={{ fontSize: 11, color: 'var(--color-ink-3)' }}>Riverside Clinic</div>
        </div>
      </div>

      {/* Nav */}
      <div style={{ fontSize: 10, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-4)', padding: '10px 10px 6px', fontWeight: 500 }}>
        Workspace
      </div>
      <nav style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            style={({ isActive }) => ({
              display: 'flex', alignItems: 'center', gap: 10,
              padding: '8px 10px', borderRadius: 8,
              fontSize: 13, fontWeight: 500,
              textDecoration: 'none',
              color: isActive ? 'var(--color-accent-ink)' : 'var(--color-ink-2)',
              background: isActive ? 'var(--color-accent-soft)' : 'transparent',
              transition: 'background 0.15s, color 0.15s',
            })}
          >
            <Icon size={18} strokeWidth={1.6} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div style={{ flex: 1 }} />

      {/* AI agent status card */}
      <div style={{ border: '1px solid var(--color-border)', background: 'var(--color-surface-2)', padding: '10px 12px', borderRadius: 10, margin: '8px 2px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11.5, color: 'var(--color-ink-2)', fontWeight: 500 }}>
          <span style={{ width: 7, height: 7, borderRadius: '50%', background: 'var(--color-sage)', display: 'inline-block', animation: 'pulse-sage 2s infinite' }} />
          AI Agent online
        </div>
        <div style={{ display: 'flex', gap: 14, marginTop: 6 }}>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <b style={{ fontSize: 15, color: 'var(--color-ink)' }}>—</b>
            <span style={{ fontSize: 10.5, color: 'var(--color-ink-3)' }}>calls today</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <b style={{ fontSize: 15, color: 'var(--color-ink)' }}>—</b>
            <span style={{ fontSize: 10.5, color: 'var(--color-ink-3)' }}>booked</span>
          </div>
        </div>
      </div>

      {/* Bottom settings */}
      <NavLink to="/settings" style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 10px', borderRadius: 8, fontSize: 13, fontWeight: 500, textDecoration: 'none', color: 'var(--color-ink-2)' }}>
        <Settings size={18} strokeWidth={1.6} />
        Settings
      </NavLink>

      {/* User */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: 8, borderRadius: 8, marginTop: 6, border: '1px solid var(--color-border)', background: 'var(--color-surface-2)' }}>
        <div style={{ width: 30, height: 30, background: 'var(--color-accent)', color: 'white', borderRadius: '50%', display: 'grid', placeItems: 'center', fontSize: 11, fontWeight: 600 }}>EK</div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--color-ink)' }}>Elif Kaya</div>
          <div style={{ fontSize: 10.5, color: 'var(--color-ink-3)' }}>Receptionist</div>
        </div>
      </div>
    </aside>
  )
}
