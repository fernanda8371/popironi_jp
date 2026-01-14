from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import wave
import struct
import os
from datetime import datetime
import json
from ai_music import MusicAI

app = Flask(__name__)

# Inicializar AI
music_ai = MusicAI()

# Crear carpeta para archivos generados
if not os.path.exists('generated_audio'):
    os.makedirs('generated_audio')

# Mapeo de sentimientos a características musicales
SENTIMIENTOS = {
    'feliz': {'tempo': 'rápido', 'tonalidad': 'mayor', 'frecuencias': [523, 659, 784, 880]},  # C, E, G, A
    'triste': {'tempo': 'lento', 'tonalidad': 'menor', 'frecuencias': [440, 493, 523, 587]},  # A, B, C, D
    'enérgico': {'tempo': 'muy_rápido', 'tonalidad': 'mayor', 'frecuencias': [659, 783, 880, 987]},  # E, G, A, B
    'calmado': {'tempo': 'muy_lento', 'tonalidad': 'mayor', 'frecuencias': [261, 329, 392, 440]},  # C, E, G, A
    'misterioso': {'tempo': 'lento', 'tonalidad': 'menor', 'frecuencias': [440, 466, 523, 554]},  # A, A#, C, C#
    'romántico': {'tempo': 'medio', 'tonalidad': 'mayor', 'frecuencias': [349, 440, 523, 659]},  # F, A, C, E
    'melancólico': {'tempo': 'lento', 'tonalidad': 'menor', 'frecuencias': [293, 349, 440, 493]},  # D, F, A, B
    'nostálgico': {'tempo': 'medio', 'tonalidad': 'menor', 'frecuencias': [392, 440, 523, 587]}   # G, A, C, D
}

# Mapeo de lugares de Tokio a características ambientales
LUGARES = {
    'shibuya': {'ambiente': 'urbano_vibrante', 'reverb': 'bajo', 'ruido': 'multitud'},
    'shinjuku': {'ambiente': 'metropolitano', 'reverb': 'bajo', 'ruido': 'neón'},
    'harajuku': {'ambiente': 'juvenil', 'reverb': 'medio', 'ruido': 'moderno'},
    'asakusa': {'ambiente': 'tradicional', 'reverb': 'medio', 'ruido': 'templo'},
    'akihabara': {'ambiente': 'electrónico', 'reverb': 'bajo', 'ruido': 'digital'},
    'ueno': {'ambiente': 'parque', 'reverb': 'medio', 'ruido': 'naturaleza'},
    'odaiba': {'ambiente': 'costero', 'reverb': 'alto', 'ruido': 'bahía'},
    'roppongi': {'ambiente': 'nocturno', 'reverb': 'bajo', 'ruido': 'urbano'}
}

def generar_onda(frecuencia, duracion, sample_rate=44100, forma='seno'):
    """Genera una onda de audio"""
    t = np.linspace(0, duracion, int(sample_rate * duracion))
    
    if forma == 'seno':
        return np.sin(2 * np.pi * frecuencia * t)
    elif forma == 'cuadrada':
        return np.sign(np.sin(2 * np.pi * frecuencia * t))
    elif forma == 'triangular':
        return 2 * np.abs(2 * (frecuencia * t - np.floor(frecuencia * t + 0.5))) - 1
    else:
        return np.sin(2 * np.pi * frecuencia * t)

def aplicar_envolvente(audio, ataque=0.1, sostenimiento=0.7, liberacion=0.2):
    """Aplica envolvente ADSR simplificada"""
    n = len(audio)
    envolvente = np.ones(n)
    
    ataque_samples = int(n * ataque)
    liberacion_samples = int(n * liberacion)
    
    # Ataque
    envolvente[:ataque_samples] = np.linspace(0, 1, ataque_samples)
    # Liberación
    envolvente[-liberacion_samples:] = np.linspace(1, 0, liberacion_samples)
    
    return audio * envolvente

def generar_ruido_ambiente(lugar, duracion, sample_rate=44100):
    """Genera ruido ambiente según el lugar de Tokio"""
    ruido = LUGARES[lugar]['ruido']
    t = np.linspace(0, duracion, int(sample_rate * duracion))
    
    if ruido == 'multitud':
        # Ruido de multitud en Shibuya
        ruido_audio = np.random.normal(0, 0.04, len(t))
        modulacion = 0.4 + 0.2 * np.sin(2 * np.pi * 0.5 * t)
        return ruido_audio * modulacion
    elif ruido == 'neón':
        # Sonido urbano de Shinjuku
        audio = np.zeros(len(t))
        for _ in range(3):
            inicio = np.random.randint(0, len(t) - 8000)
            freq = np.random.randint(200, 600)
            audio[inicio:inicio+5000] += 0.08 * np.sin(2 * np.pi * freq * t[inicio:inicio+5000])
        return audio
    elif ruido == 'moderno':
        # Ambiente juvenil de Harajuku
        return np.random.normal(0, 0.03, len(t))
    elif ruido == 'templo':
        # Sonido tranquilo de templo en Asakusa
        audio = np.zeros(len(t))
        for _ in range(2):
            inicio = np.random.randint(0, len(t) - 10000)
            freq = 440  # Nota A
            audio[inicio:inicio+8000] += 0.06 * np.sin(2 * np.pi * freq * t[inicio:inicio+8000])
        return audio
    elif ruido == 'digital':
        # Sonidos electrónicos de Akihabara
        audio = np.zeros(len(t))
        for _ in range(4):
            inicio = np.random.randint(0, len(t) - 3000)
            freq = np.random.randint(800, 1600)
            audio[inicio:inicio+1000] += 0.1 * np.sin(2 * np.pi * freq * t[inicio:inicio+1000])
        return audio
    elif ruido == 'naturaleza':
        # Parque de Ueno con pájaros
        audio = np.zeros(len(t))
        for _ in range(4):
            inicio = np.random.randint(0, len(t) - 5000)
            freq = np.random.randint(2000, 3500)
            audio[inicio:inicio+2000] += 0.08 * np.sin(2 * np.pi * freq * t[inicio:inicio+2000])
        return audio
    elif ruido == 'bahía':
        # Sonido de la bahía en Odaiba
        ruido_audio = np.random.normal(0, 0.05, len(t))
        modulacion = 0.3 + 0.15 * np.sin(2 * np.pi * 0.15 * t)
        return ruido_audio * modulacion
    elif ruido == 'urbano':
        # Ambiente nocturno de Roppongi
        return np.random.normal(0, 0.035, len(t))
    else:
        return np.zeros(len(t))

def obtener_duracion_nota(tempo):
    """Obtiene la duración de una nota según el tempo"""
    tempos = {
        'muy_lento': 1.5,
        'lento': 1.0,
        'medio': 0.7,
        'rápido': 0.5,
        'muy_rápido': 0.3
    }
    return tempos.get(tempo, 0.7)

def guardar_wav(filename, audio, sample_rate=44100):
    """Guarda audio en formato WAV sin scipy"""
    audio = np.clip(audio, -32767, 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())

def generar_melodia(sentimiento, lugar, duracion_total=15):
    """Genera una melodía basada en sentimiento y lugar usando AI"""
    sample_rate = 44100
    
    # Usar AI para analizar y ajustar parámetros
    ajustes_ai = music_ai.analizar_emocion_avanzada(sentimiento, lugar)
    
    # Obtener características base
    caracteristicas = SENTIMIENTOS[sentimiento]
    frecuencias = caracteristicas['frecuencias']
    tempo = caracteristicas['tempo']
    duracion_nota = obtener_duracion_nota(tempo)
    
    # Aplicar ajustes de AI
    duracion_nota = duracion_nota * (1.0 + (ajustes_ai['variacion'] - 0.5) * 0.3)
    
    # Generar secuencia de notas
    audio_total = np.array([])
    tiempo_transcurrido = 0
    
    while tiempo_transcurrido < duracion_total:
        # Seleccionar frecuencia aleatoria del conjunto
        freq = np.random.choice(frecuencias)
        
        # Generar nota
        nota = generar_onda(freq, duracion_nota, sample_rate)
        
        # Aplicar envolvente
        nota = aplicar_envolvente(nota)
        
        # Agregar armónicos sutiles
        armonico = 0.2 * generar_onda(freq * 2, duracion_nota, sample_rate)
        nota += armonico
        
        audio_total = np.concatenate([audio_total, nota])
        tiempo_transcurrido += duracion_nota
    
    # Agregar ambiente del lugar
    ambiente = generar_ruido_ambiente(lugar, len(audio_total) / sample_rate, sample_rate)
    
    # Mezclar melodía con ambiente (ajustado por AI)
    intensidad_melodia = 0.5 + ajustes_ai['intensidad'] * 0.3
    intensidad_ambiente = 0.5 - ajustes_ai['intensidad'] * 0.2
    audio_final = intensidad_melodia * audio_total + intensidad_ambiente * ambiente[:len(audio_total)]
    
    # Normalizar
    audio_final = audio_final / np.max(np.abs(audio_final))
    audio_final = (audio_final * 32767).astype(np.int16)
    
    return audio_final, sample_rate

@app.route('/')
def index():
    return render_template('index.html', 
                         sentimientos=list(SENTIMIENTOS.keys()),
                         lugares=list(LUGARES.keys()))

@app.route('/generar', methods=['POST'])
def generar():
    try:
        data = request.json
        sentimiento = data.get('sentimiento', 'calmado')
        lugar = data.get('lugar', 'shibuya')
        
        # Validar inputs
        if sentimiento not in SENTIMIENTOS:
            return jsonify({'error': 'Sentimiento no válido'}), 400
        if lugar not in LUGARES:
            return jsonify({'error': 'Lugar no válido'}), 400
        
        # Intentar generar con IA primero
        print("🎵 Intentando generar audio con IA...")
        audio_ai, sample_rate_ai, success = music_ai.generar_audio_con_ia(sentimiento, lugar)
        
        if success and audio_ai is not None:
            # IA funcionó! Usar audio generado por IA
            audio = audio_ai
            sample_rate = sample_rate_ai
            metodo = "IA (MusicGen)"
            print("✅ Usando audio generado por IA")
        else:
            # Fallback: generar con síntesis procedural
            print("🔧 Usando generación procedural como fallback")
            audio, sample_rate = generar_melodia(sentimiento, lugar)
            metodo = "Síntesis Procedural"
        
        # Generar descripción con AI
        descripcion_ai = music_ai.generar_descripcion_musical(sentimiento, lugar)
        
        # Guardar archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'melodia_{sentimiento}_{lugar}_{timestamp}.wav'
        filepath = os.path.join('generated_audio', filename)
        
        guardar_wav(filepath, audio, sample_rate)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'prompt': f'Melodía {sentimiento} en {lugar}',
            'descripcion_ai': descripcion_ai,
            'metodo_generacion': metodo,
            'caracteristicas': {
                'sentimiento': SENTIMIENTOS[sentimiento],
                'lugar': LUGARES[lugar]
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def descargar_audio(filename):
    try:
        filepath = os.path.join('generated_audio', filename)
        return send_file(filepath, mimetype='audio/wav')
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/limpiar', methods=['POST'])
def limpiar():
    """Limpia archivos antiguos"""
    try:
        archivos = os.listdir('generated_audio')
        for archivo in archivos:
            os.remove(os.path.join('generated_audio', archivo))
        return jsonify({'success': True, 'mensaje': 'Archivos limpiados'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
