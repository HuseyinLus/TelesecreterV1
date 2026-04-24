# Module 7 — DashboardPage Three-Zone Layout

## Goal
Build the three-zone grid skeleton for `DashboardPage`: Registry (`1fr`, left) | Pulse (`360px`, right) | LogTrace (`h-64`, full-width bottom). No real components yet — each zone is a labeled placeholder box.

## Files to modify
- `src/pages/DashboardPage.jsx`

---

## src/pages/DashboardPage.jsx
```jsx
export default function DashboardPage() {
  return (
    <div style={{
      display: 'grid',
      gridTemplateRows: '1fr 256px',
      gridTemplateColumns: '1fr 360px',
      height: '100%',
      overflow: 'hidden',
      gap: 0,
    }}>
      {/* Zone 2 — Registry (left, flex-grow) */}
      <div style={{
        gridRow: 1,
        gridColumn: 1,
        overflow: 'auto',
        padding: 24,
        borderRight: '1px solid var(--color-border)',
        borderBottom: '1px solid var(--color-border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--color-ink-3)',
        fontSize: 13,
      }}>
        Zone 2 — Registry
      </div>

      {/* Zone 1 — Pulse (right rail, 360px) */}
      <div style={{
        gridRow: 1,
        gridColumn: 2,
        overflow: 'auto',
        padding: 24,
        borderBottom: '1px solid var(--color-border)',
        background: 'var(--color-surface)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--color-ink-3)',
        fontSize: 13,
      }}>
        Zone 1 — Pulse
      </div>

      {/* Zone 3 — Logic Trace (full width bottom, 256px) */}
      <div style={{
        gridRow: 2,
        gridColumn: '1 / -1',
        overflow: 'hidden',
        borderTop: '1px solid var(--color-border)',
        background: 'var(--color-surface-2)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--color-ink-3)',
        fontSize: 13,
      }}>
        Zone 3 — Logic Trace
      </div>
    </div>
  )
}
```

---

## Test
1. Visit `http://localhost:5173/dashboard`

**Pass criteria:**
- Three zones are clearly visible
- Registry zone takes all available width on the left
- Pulse zone is exactly 360px wide on the right
- Logic Trace is pinned to the bottom, full width, ~256px tall
- No zone overflows or causes page-level scrollbar
- Zones have visible borders separating them
