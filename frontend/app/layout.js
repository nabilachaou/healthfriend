import '../styles/globals.css'

export const metadata = {
  title: 'HealthFriend',
  description: 'Chatbot médical basé sur PubMed',
}

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body style={{
        minHeight: '100vh',
        height: '100vh',
        margin: 0,
        padding: 0,
        background: 'radial-gradient(circle at 20% 20%, rgba(10,110,110,0.06) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(10,110,110,0.04) 0%, transparent 50%), #f0f4f8',
        display: 'flex',
        alignItems: 'stretch',
        justifyContent: 'center',
        overflow: 'hidden'
      }}>
        {children}
      </body>
    </html>
  )
}