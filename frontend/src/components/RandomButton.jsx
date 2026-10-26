export function RandomButton({ onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="w-full md:w-80 h-24 text-3xl font-semibold rounded-xl bg-emerald-500 hover:bg-emerald-400 text-zinc-950 transition"
    >
      Random
    </button>
  )
}
