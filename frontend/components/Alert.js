export default function Alert({ message }) {
  return (
    <div className="bg-red-200 text-red-800 p-2 rounded my-2">
      ⚠️ {message}
    </div>
  )
}