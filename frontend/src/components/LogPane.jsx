import { useEffect, useRef } from 'react'

export function LogPane({ text }) {
  const logRef = useRef(null)

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight
    }
  }, [text])

  return (
    <pre
      ref={logRef}
      className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 h-96 overflow-y-auto text-sm"
    >
      {text}
    </pre>
  )
}
