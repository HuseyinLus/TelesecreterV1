# Module 6 — DashboardShell + Sidebar + Header

## Goal
Build the persistent app shell: the `232px` sidebar with navigation and the topbar header. These are shared across all pages via React Router's `<Outlet />`. No real data yet — sidebar counts and user info are hardcoded.

## Files to create
- `src/components/layout/DashboardShell.jsx`
- `src/components/layout/Sidebar.jsx`
- `src/components/layout/Header.jsx`

## Files to modify
- `src/App.jsx` — wrap routes inside `DashboardShell`

---

## src/components/layout/Sidebar.jsx
```jsx
import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Calendar, Stethoscope, Users, Clock, Phone, Settings } from 'lucide-react'

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/calendar',  label: 'Calendar',  icon: Calendar },
  { to: '/doctors',   label: 'Doctors',   icon: Stethoscope },
  { to: '/patients',  label: 'Patients',  icon: Users },
  { to: '/slots',     label: 'Availability', icon: Clock },
  { to: '/calls',     label: 'Call log',  icon: Phone },
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
```

---

## src/components/layout/Header.jsx
```jsx
import { Search, Bell, HelpCircle, Plus } from 'lucide-react'

export default function Header() {
  const today = new Date().toLocaleDateString('en-US', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })

  return (
    <header style={{
      display: 'grid',
      gridTemplateColumns: '1fr auto 1fr',
      alignItems: 'center',
      padding: '18px 24px 16px',
      gap: 24,
      borderBottom: '1px solid var(--color-border)',
      background: 'var(--color-bg)',
      flexShrink: 0,
    }}>
      <div>
        <div style={{ fontSize: 11, color: 'var(--color-ink-3)', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 500, marginBottom: 4 }}>{today}</div>
        <h1 style={{ margin: 0, fontFamily: 'var(--font-serif)', fontSize: 26, fontWeight: 400, color: 'var(--color-ink)', letterSpacing: '-0.01em' }}>Good morning, Elif</h1>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 8, background: 'var(--color-surface)', border: '1px solid var(--color-border)', padding: '8px 12px', borderRadius: 10, width: 360 }}>
        <Search size={16} color="var(--color-ink-3)" />
        <input placeholder="Search patients, doctors, appointments…" style={{ border: 'none', outline: 'none', background: 'transparent', flex: 1, fontSize: 13, color: 'var(--color-ink)', fontFamily: 'var(--font-sans)' }} />
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'flex-end' }}>
        <button style={{ width: 34, height: 34, borderRadius: 9, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', border: '1px solid var(--color-border)', background: 'var(--color-surface)' }}>
          <Bell size={18} strokeWidth={1.6} />
        </button>
        <button style={{ width: 34, height: 34, borderRadius: 9, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', border: '1px solid var(--color-border)', background: 'var(--color-surface)' }}>
          <HelpCircle size={18} strokeWidth={1.6} />
        </button>
        <div style={{ width: 1, height: 22, background: 'var(--color-border)', margin: '0 4px' }} />
        <button style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '8px 14px', background: 'var(--color-ink)', color: 'var(--color-bg)', borderRadius: 9, fontSize: 12.5, fontWeight: 500 }}>
          <Plus size={14} strokeWidth={2} />
          New appointment
        </button>
      </div>
    </header>
  )
}
```

---

## src/components/layout/DashboardShell.jsx
```jsx
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'

export default function DashboardShell() {
  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <Sidebar />
      <div style={{ display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, overflow: 'hidden' }}>
        <Header />
        <main style={{ flex: 1, overflow: 'auto' }}>
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

---

## src/App.jsx (updated)
```jsx
import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardShell from './components/layout/DashboardShell'
import DashboardPage from './pages/DashboardPage'
import CalendarPage from './pages/CalendarPage'

export default function App() {
  return (
    <Routes>
      <Route element={<DashboardShell />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/calendar"  element={<CalendarPage />} />
      </Route>
    </Routes>
  )
}
```

---

## Test
1. Run `npm run dev`
2. Visit `http://localhost:5173/dashboard`

**Pass criteria:**
- Sidebar is visible on the left (232px wide)
- All 6 nav items render with icons
- "Dashboard" nav item is highlighted (accent color) when on `/dashboard`
- Clicking "Calendar" nav item navigates to `/calendar` and highlights "Calendar"
- Header shows today's date, greeting, search bar, and "New appointment" button
- AI agent card shows in sidebar with pulsing sage dot
- Layout fills the full viewport height with no scrollbars on the shell itself
