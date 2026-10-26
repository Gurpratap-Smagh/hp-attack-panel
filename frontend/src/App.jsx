import { RandomButton } from './components/RandomButton'
import { LogPane } from './components/LogPane'
import { useLiveRequestLog } from './hooks/useLiveRequestLog'
import { fireRandomPayload } from './services/api'

export default function App() {
  const { logText, appendEntry } = useLiveRequestLog()

  const handleRandomClick = async () => {
    try {
      const data = await fireRandomPayload()
      appendEntry(`[http] fired payload ${data.payload_id} (${data.status_code})`)
    } catch (error) {
      appendEntry(`[error] ${error}`)
    }
  }

  return (
    <main className="mx-auto max-w-4xl p-6 md:p-10 bg-zinc-950 text-zinc-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-8">hp-attack-panel</h1>
      <RandomButton onClick={handleRandomClick} />

      <section className="mt-8">
        <h2 className="text-lg font-semibold mb-2">Live Request Log</h2>
        <LogPane text={logText} />
      </section>
    </main>
  )
}
