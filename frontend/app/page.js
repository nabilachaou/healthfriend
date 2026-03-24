"use client"

import { useState } from 'react'
import ChatBox from '../components/ChatBox'
import InputForm from '../components/InputForm'

export default function Page() {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: "Bonjour ! Je suis votre assistant médical. Posez-moi vos questions de santé — je m'appuie sur des articles scientifiques PubMed pour vous répondre.",
      time: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    }
  ])
  const [loading, setLoading] = useState(false)

  const handleSend = async (text) => {
    const time = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    setMessages(prev => [...prev, { sender: 'user', text, time }])
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text })
      })
      if (!res.ok) throw new Error("Erreur backend")
      const data = await res.json()
      setMessages(prev => [...prev, {
        sender: 'bot',
        text: data.response,
        time: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      }])
    } catch (err) {
      setMessages(prev => [...prev, {
        sender: 'bot',
        text: "❌ Erreur de connexion au backend.",
        time: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleEmergency = () => {
    const time = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    setMessages(prev => [...prev,
      { sender: 'user', text: "🚨 URGENCE", time },
      { sender: 'emergency', text: '', time }
    ])
  }

  return (
    <div style={{
      width: '100%',
      maxWidth: '860px',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      background: '#ffffff',
      boxShadow: '0 0 60px rgba(10,110,110,0.12)',
    }}>

      {/* HEADER */}
      <header style={{
        background: 'linear-gradient(135deg, #0a6e6e 0%, #0d8a8a 100%)',
        padding: '18px 32px',
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        flexShrink: 0
      }}>
        <div style={{
          width: '48px', height: '48px',
          background: 'rgba(255,255,255,0.15)',
          borderRadius: '14px',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '24px',
          border: '1px solid rgba(255,255,255,0.2)',
          flexShrink: 0
        }}>🩺</div>

        <div>
          <h1 style={{
            fontFamily: 'Playfair Display, serif',
            color: 'white', fontSize: '22px', fontWeight: 600
          }}>HealthFriend</h1>
          <p style={{
            color: 'rgba(255,255,255,0.75)',
            fontSize: '13px', marginTop: '2px', fontWeight: 300
          }}>Basé sur des articles scientifiques PubMed</p>
        </div>

        <div style={{
          marginLeft: 'auto', display: 'flex',
          alignItems: 'center', gap: '6px',
          color: 'rgba(255,255,255,0.85)', fontSize: '13px'
        }}>
          <div style={{
            width: '8px', height: '8px',
            background: '#4ade80', borderRadius: '50%',
            boxShadow: '0 0 8px #4ade80',
            animation: 'pulse 2s infinite'
          }}></div>
          En ligne
        </div>
      </header>

      {/* MESSAGES — prend tout l'espace restant */}
      <ChatBox messages={messages} loading={loading} />

      {/* INPUT */}
      <InputForm onSend={handleSend} onEmergency={handleEmergency} />

      {/* FOOTER */}
      <footer style={{
        textAlign: 'center', fontSize: '11px',
        color: '#6b7a8d', padding: '6px 20px 10px',
        background: 'white', flexShrink: 0,
        borderTop: '1px solid #f0f4f8'
      }}>
        ⚠️ Ce chatbot fournit des informations générales basées sur PubMed · Ne remplace pas un médecin
      </footer>
    </div>
  )
}