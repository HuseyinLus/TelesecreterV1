// "2026-04-16T10:30:00" → "Thu · Apr 16, 2026"
export function formatDate(isoString) {
  const d = new Date(isoString)
  return d.toLocaleDateString('en-US', {
    weekday: 'short', month: 'short', day: 'numeric', year: 'numeric'
  }).replace(',', ' ·')
}

// "10:30:00" → "10:30"
export function formatTime(hhmmss) {
  return hhmmss?.slice(0, 5) ?? '—'
}

// "3fa85f64-5717-4562-b3fc-2c963f66afa6" → "3fa85f64…"
export function truncateUUID(uuid) {
  return uuid ? uuid.slice(0, 8) + '…' : '—'
}

// "2026-04-16" → true/false
export function isToday(dateString) {
  const today = new Date().toISOString().slice(0, 10)
  return dateString === today
}

// "10:30:00" → 630 (minutes since midnight)
export function toMinutes(hhmmss) {
  const [h, m] = (hhmmss ?? '00:00').split(':').map(Number)
  return h * 60 + m
}

// "10:30:00" + 45 → "11:15"
export function addMinutes(hhmmss, mins) {
  const total = toMinutes(hhmmss) + mins
  const h = Math.floor(total / 60).toString().padStart(2, '0')
  const m = (total % 60).toString().padStart(2, '0')
  return `${h}:${m}`
}
