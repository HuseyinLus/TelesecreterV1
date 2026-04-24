import { toMinutes, formatTime } from '../../utils/formatters'
import { HOUR_HEIGHT, GRID_START_HOUR } from '../../utils/constants'

const COLOR_STYLES = {
  teal:   { bg: 'var(--color-teal-soft)',   stripe: 'var(--color-teal)',   border: 'oklch(58% 0.09 200 / 0.18)' },
  sage:   { bg: 'var(--color-sage-soft)',   stripe: 'var(--color-sage)',   border: 'oklch(62% 0.07 160 / 0.20)' },
  amber:  { bg: 'var(--color-amber-soft)',  stripe: 'var(--color-amber)',  border: 'oklch(72% 0.11 70 / 0.24)'  },
  indigo: { bg: 'var(--color-indigo-soft)', stripe: 'var(--color-indigo)', border: 'oklch(56% 0.11 270 / 0.20)' },
  rose:   { bg: 'var(--color-rose-soft)',   stripe: 'var(--color-rose)',   border: 'oklch(66% 0.11 20 / 0.22)'  },
}

export default function AppointmentBlock({ appt, color, doctorName, onClick, isSelected }) {
  const startMins = toMinutes(appt.start_time)
  const endMins   = toMinutes(appt.end_time)
  const dur       = endMins - startMins
  const topPx     = (startMins - GRID_START_HOUR * 60) / 60 * HOUR_HEIGHT + 8
  const heightPx  = Math.max(dur / 60 * HOUR_HEIGHT - 3, 22)
  const c         = COLOR_STYLES[color] ?? COLOR_STYLES.teal
  const isShort   = dur <= 30

  return (
    <button
      onClick={() => onClick?.(appt)}
      style={{
        position: 'absolute', left: 4, right: 4, top: topPx, height: heightPx,
        borderRadius: 7, background: c.bg, border: `1px solid ${c.border}`,
        display: 'flex', overflow: 'hidden', cursor: 'pointer', textAlign: 'left',
        boxShadow: isSelected ? `0 0 0 2px var(--color-accent)` : 'none',
        borderStyle: appt.status === 'pending' ? 'dashed' : 'solid',
        transition: 'box-shadow 0.15s, transform 0.1s',
        minHeight: 26,
      }}
    >
      <div style={{ width: 3, flexShrink: 0, background: c.stripe }} />
      <div style={{ flex: 1, padding: '4px 7px', minWidth: 0 }}>
        <div style={{ fontSize: 10, fontWeight: 600, color: 'var(--color-ink-2)', fontVariantNumeric: 'tabular-nums' }}>{formatTime(appt.start_time)}</div>
        <div style={{ fontSize: 11.5, fontWeight: 600, color: 'var(--color-ink)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {appt.user_id?.slice(0, 6)}…
        </div>
        {!isShort && <div style={{ fontSize: 10, color: 'var(--color-ink-3)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{doctorName?.replace('Dr. ', '')}</div>}
        {appt.status === 'pending' && <div style={{ fontSize: 9.5, color: 'var(--color-amber)', fontWeight: 500 }}>Pending</div>}
      </div>
    </button>
  )
}
