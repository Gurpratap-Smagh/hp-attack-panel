import { useEffect, useMemo, useState } from 'react'

export function useLiveRequestLog() {
  const [entries, setEntries] = useState([])

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${protocol}://${window.location.host}/ws`)
    let pingIntervalId

    const append = (message) => {
      setEntries((current) => [...current, message])
    }

    ws.onopen = () => {
      append('[ws] connected')
      pingIntervalId = window.setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send('ping')
        }
      }, 15000)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        append(JSON.stringify(data, null, 2))
      } catch {
        append(event.data)
      }
    }

    ws.onclose = () => {
      append('[ws] disconnected')
    }

    return () => {
      if (pingIntervalId) {
        clearInterval(pingIntervalId)
      }
      ws.close()
    }
  }, [])

  const logText = useMemo(() => entries.join('\n'), [entries])

  const appendEntry = (message) => {
    setEntries((current) => [...current, message])
  }

  return { logText, appendEntry }
}
