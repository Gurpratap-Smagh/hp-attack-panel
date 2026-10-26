export async function fireRandomPayload() {
  const response = await fetch('/fire-random', { method: 'POST' })
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }
  return response.json()
}
