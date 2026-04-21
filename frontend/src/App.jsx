export default function App() {
  return (
    <div style={{ padding: 24 }}>
      <p className="text-[var(--color-accent)] font-semibold">Tailwind v4 token test</p>
      <p className="text-[var(--color-ink-3)] text-xs mt-1">If this text is teal-blue, tokens are working.</p>
      <div className="mt-4 w-8 h-8 rounded-full bg-[var(--color-sage)] animate-[pulse-sage_2s_infinite]" />
    </div>
  )
}
