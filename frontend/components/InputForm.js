"use client"

import { useState } from 'react'

export default function InputForm({ onSend }) {
  const [text, setText] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (text.trim() === '') return
    onSend(text)
    setText('')
  }

  return (
    <div style={{
      padding: '16px 20px 12px',
      background: 'white',
      borderTop: '1px solid #e2e8f0'
    }}>
      <form onSubmit={handleSubmit}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          background: '#f0f4f8',
          border: '1.5px solid #e2e8f0',
          borderRadius: '50px',
          padding: '8px 8px 8px 20px',
        }}>
          <input
            type="text"
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="Posez votre question médicale..."
            style={{
              flex: 1,
              border: 'none',
              background: 'transparent',
              fontFamily: 'DM Sans, sans-serif',
              fontSize: '14.5px',
              color: '#1a2332',
              outline: 'none'
            }}
          />
          <button
            type="submit"
            style={{
              width: '40px', height: '40px',
              background: text.trim() ? '#0a6e6e' : '#cbd5e0',
              border: 'none',
              borderRadius: '50%',
              cursor: text.trim() ? 'pointer' : 'default',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              transition: 'background 0.2s',
              flexShrink: 0
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
              <path d="M2 21l21-9L2 3v7l15 2-15 2z"/>
            </svg>
          </button>
        </div>
      </form>
    </div>
  )
}