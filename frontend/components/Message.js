"use client"

export default function Message({ sender, text, time }) {

  // Message d'urgence
  if (sender === 'emergency') {
    return (
      <div style={{
        background: 'linear-gradient(135deg, #e63946, #c1121f)',
        color: 'white',
        borderRadius: '18px',
        padding: '16px 20px',
        maxWidth: '85%',
        boxShadow: '0 4px 20px rgba(230,57,70,0.35)',
        animation: 'fadeUp 0.3s ease'
      }}>
        <div style={{ fontWeight: 600, fontSize: '15px', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          🚨 URGENCE MÉDICALE DÉTECTÉE
        </div>
        <div style={{
          background: 'rgba(255,255,255,0.2)',
          borderRadius: '8px',
          padding: '6px 14px',
          fontSize: '22px',
          fontWeight: 700,
          textAlign: 'center',
          margin: '10px 0',
          letterSpacing: '2px'
        }}>15 · 112</div>
        <p style={{ fontSize: '13px', opacity: 0.9, lineHeight: 1.5 }}>
          Vos symptômes peuvent indiquer une situation grave. Appelez immédiatement le SAMU ou les secours. Ne restez pas seul(e).
        </p>
        {time && <div style={{ fontSize: '10px', opacity: 0.6, marginTop: '8px', textAlign: 'right' }}>{time}</div>}
      </div>
    )
  }

  const isUser = sender === 'user'

  // Parser le texte pour afficher les éléments markdown basiques
  const renderText = (text) => {
    if (!text) return null

    // Détecter si c'est une réponse d'urgence backend
    if (text.includes('URGENCE MÉDICALE')) {
      return (
        <div style={{
          background: 'linear-gradient(135deg, #e63946, #c1121f)',
          color: 'white',
          borderRadius: '18px',
          padding: '16px 20px',
          maxWidth: '85%',
          boxShadow: '0 4px 20px rgba(230,57,70,0.35)',
        }}>
          <div style={{ fontWeight: 600, fontSize: '15px', marginBottom: '8px' }}>🚨 URGENCE MÉDICALE DÉTECTÉE</div>
          <div style={{
            background: 'rgba(255,255,255,0.2)', borderRadius: '8px',
            padding: '6px 14px', fontSize: '22px', fontWeight: 700,
            textAlign: 'center', margin: '10px 0', letterSpacing: '2px'
          }}>15 · 112</div>
          <p style={{ fontSize: '13px', opacity: 0.9, lineHeight: 1.5 }}>
            Vos symptômes peuvent indiquer une situation grave. Appelez immédiatement le SAMU ou les secours.
          </p>
        </div>
      )
    }

    // Parser les sections de la réponse bot
    const lines = text.split('\n').filter(l => l.trim())
    const infoLines = []
    const specialistLine = lines.find(l => l.includes('Consulter') || l.includes('Consult'))
    const disclaimerLine = lines.find(l => l.includes('⚠️'))
    const contentLines = lines.filter(l =>
      !l.includes('Consulter') && !l.includes('Consult') &&
      !l.includes('⚠️') && !l.includes('Informations médicales') &&
      !l.includes('Medical Information') && l.trim()
    )

    return (
      <div>
        {/* Carte info médicale */}
        {contentLines.length > 0 && (
          <div style={{
            background: '#e6f4f4',
            border: '1px solid rgba(10,110,110,0.15)',
            borderRadius: '12px',
            padding: '12px 14px',
            marginBottom: '10px'
          }}>
            <div style={{
              fontSize: '11px', fontWeight: 600,
              color: '#0a6e6e', textTransform: 'uppercase',
              letterSpacing: '0.8px', marginBottom: '8px',
              display: 'flex', alignItems: 'center', gap: '6px'
            }}>📋 Informations médicales</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {contentLines.map((line, i) => {
                const clean = line.replace(/^[•\-\*]\s*/, '').replace(/\*\*/g, '')
                if (!clean.trim()) return null
                return (
                  <div key={i} style={{
                    fontSize: '13.5px', color: '#1a2332',
                    paddingLeft: '14px', position: 'relative', lineHeight: 1.55
                  }}>
                    <span style={{ position: 'absolute', left: 0, color: '#0a6e6e', fontWeight: 'bold' }}>•</span>
                    {clean}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Badge spécialiste */}
        {specialistLine && (
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: '6px',
            background: 'white', border: '1px solid #e2e8f0',
            borderRadius: '20px', padding: '5px 12px',
            fontSize: '12px', fontWeight: 500, color: '#1a2332',
            marginBottom: '6px'
          }}>
            👨‍⚕️ {specialistLine.replace(/[*_]/g, '').replace(/Consult(er)?:?\s*/i, 'Consulter : ')}
          </div>
        )}

        {/* Disclaimer */}
        {disclaimerLine && (
          <div style={{ fontSize: '11.5px', color: '#6b7a8d', display: 'flex', alignItems: 'center', gap: '4px' }}>
            {disclaimerLine.replace(/\*/g, '')}
          </div>
        )}

        {/* Texte simple (message de bienvenue etc.) */}
        {!specialistLine && !disclaimerLine && contentLines.length === 0 && (
          <span>{text}</span>
        )}
      </div>
    )
  }

  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-end',
      gap: '10px',
      flexDirection: isUser ? 'row-reverse' : 'row',
      animation: 'fadeUp 0.3s ease'
    }}>
      {/* Avatar */}
      <div style={{
        width: '34px', height: '34px',
        borderRadius: '50%',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '16px', flexShrink: 0,
        background: isUser ? '#0a6e6e' : '#e6f4f4',
        border: isUser ? '2px solid #0a6e6e' : '2px solid rgba(10,110,110,0.15)'
      }}>
        {isUser ? '👤' : '🤖'}
      </div>

      {/* Bubble */}
      <div style={{
        maxWidth: '72%',
        padding: isUser ? '12px 16px' : '14px 18px',
        borderRadius: '18px',
        borderBottomLeftRadius: isUser ? '18px' : '6px',
        borderBottomRightRadius: isUser ? '6px' : '18px',
        background: isUser ? '#0a6e6e' : '#ffffff',
        color: isUser ? 'white' : '#1a2332',
        border: isUser ? 'none' : '1px solid #e2e8f0',
        boxShadow: isUser
          ? '0 2px 12px rgba(10,110,110,0.25)'
          : '0 2px 12px rgba(0,0,0,0.06)',
        fontSize: '14.5px',
        lineHeight: 1.65
      }}>
        {isUser ? text : renderText(text)}
        {time && (
          <div style={{
            fontSize: '10px',
            color: isUser ? 'rgba(255,255,255,0.6)' : '#6b7a8d',
            textAlign: 'right',
            marginTop: '6px'
          }}>{time}</div>
        )}
      </div>
    </div>
  )
}