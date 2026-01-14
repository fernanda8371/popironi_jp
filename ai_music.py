import requests
import json
import numpy as np
import base64
from io import BytesIO

class MusicAI:
    """Cliente para generar audio con IA usando modelos de Hugging Face"""
    
    def __init__(self):
        # API gratuita de Hugging Face Inference (sin token para uso básico)
        self.musicgen_url = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
        self.text_gen_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        
    def generar_prompt_musical(self, sentimiento, lugar):
        """Genera un prompt optimizado para MusicGen basado en sentimiento y lugar de Tokio"""
        
        # Mapeo de sentimientos a descriptores musicales
        descriptores_sentimiento = {
            'feliz': 'upbeat, cheerful, bright melody, major key, energetic',
            'triste': 'melancholic, slow, minor key, emotional, contemplative',
            'enérgico': 'fast tempo, dynamic, powerful, driving rhythm, intense',
            'calmado': 'peaceful, slow, gentle, soft ambient, relaxing',
            'misterioso': 'mysterious, dark, atmospheric, enigmatic, suspenseful',
            'romántico': 'romantic, smooth, emotional, tender, warm melody',
            'melancólico': 'melancholic, nostalgic, bittersweet, reflective',
            'nostálgico': 'nostalgic, wistful, dreamy, reminiscent'
        }
        
        # Mapeo de lugares de Tokio a atmósferas sonoras
        descriptores_lugar = {
            'shibuya': 'urban electronic beats, busy city sounds, modern synth',
            'shinjuku': 'neon lights ambience, metropolitan pulse, jazzy undertones',
            'harajuku': 'pop music, colorful, playful synths, youthful energy',
            'asakusa': 'traditional Japanese instruments, temple bells, serene',
            'akihabara': 'chiptune, 8-bit sounds, electronic game music, retro',
            'ueno': 'nature sounds, birds chirping, park ambience, peaceful',
            'odaiba': 'seaside, ocean waves, coastal breeze, open space',
            'roppongi': 'nightclub vibes, bass-heavy, late night groove, sophisticated'
        }
        
        sentimiento_desc = descriptores_sentimiento.get(sentimiento, 'melodic')
        lugar_desc = descriptores_lugar.get(lugar, 'ambient')
        
        # Crear prompt para MusicGen
        prompt = f"{sentimiento_desc}, {lugar_desc}, instrumental, no vocals, 15 seconds"
        
        return prompt
    
    def generar_audio_con_ia(self, sentimiento, lugar):
        """
        Genera audio usando MusicGen de Meta/Facebook
        Retorna: audio_array (numpy), sample_rate, success_flag
        """
        
        prompt = self.generar_prompt_musical(sentimiento, lugar)
        
        try:
            print(f"🤖 Generando audio con IA: {prompt}")
            
            # Llamar a MusicGen API
            response = requests.post(
                self.musicgen_url,
                headers={"Content-Type": "application/json"},
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 15  # 15 segundos
                    }
                },
                timeout=30  # Puede tomar tiempo generar audio
            )
            
            if response.status_code == 200:
                # El audio viene como bytes
                audio_bytes = response.content
                
                # Convertir a numpy array (MusicGen retorna WAV)
                import wave
                import io
                
                with wave.open(io.BytesIO(audio_bytes), 'rb') as wav_file:
                    sample_rate = wav_file.getframerate()
                    frames = wav_file.readframes(wav_file.getnframes())
                    audio_array = np.frombuffer(frames, dtype=np.int16)
                
                print("✅ Audio generado con IA exitosamente")
                return audio_array, sample_rate, True
                
            elif response.status_code == 503:
                print("⏳ Modelo cargando, usando generación procedural como fallback")
                return None, None, False
            else:
                print(f"⚠️  API respondió con código {response.status_code}")
                return None, None, False
                
        except Exception as e:
            print(f"❌ Error al generar con IA: {e}")
            return None, None, False
    
    def generar_descripcion_musical(self, sentimiento, lugar):
        """Genera una descripción musical inteligente"""
        
        descripciones = {
            'feliz': 'Una melodía brillante y energética que refleja la vitalidad',
            'triste': 'Una composición melancólica con tonos suaves y contemplativos',
            'enérgico': 'Un ritmo dinámico y pulsante que inspira movimiento',
            'calmado': 'Una pieza serena que invita a la reflexión tranquila',
            'misterioso': 'Una atmósfera enigmática con texturas sonoras intrigantes',
            'romántico': 'Una melodía dulce y emotiva que evoca conexión',
            'melancólico': 'Un paisaje sonoro introspectivo y nostálgico',
            'nostálgico': 'Una pieza evocadora que recuerda momentos del pasado'
        }
        
        lugares_desc = {
            'shibuya': 'el icónico cruce de Shibuya',
            'shinjuku': 'las luces de neón de Shinjuku',
            'harajuku': 'la cultura juvenil de Harajuku',
            'asakusa': 'los templos tradicionales de Asakusa',
            'akihabara': 'el distrito electrónico de Akihabara',
            'ueno': 'el tranquilo parque de Ueno',
            'odaiba': 'la bahía de Odaiba',
            'roppongi': 'la vida nocturna de Roppongi'
        }
        
        base = descripciones.get(sentimiento, 'Una melodía única')
        lugar_desc = lugares_desc.get(lugar, 'Tokio')
        
        return f"{base} de {lugar_desc}."
    
    def analizar_emocion_avanzada(self, sentimiento, lugar):
        """Analiza y ajusta parámetros musicales con AI"""
        
        ajustes = {
            'intensidad': 0.5,
            'complejidad': 0.5,
            'variacion': 0.5
        }
        
        if sentimiento in ['enérgico', 'feliz']:
            ajustes['intensidad'] = 0.8
            ajustes['variacion'] = 0.7
        elif sentimiento in ['calmado', 'melancólico']:
            ajustes['intensidad'] = 0.3
            ajustes['complejidad'] = 0.6
        
        if lugar in ['shibuya', 'shinjuku', 'akihabara']:
            ajustes['complejidad'] = 0.8
            ajustes['variacion'] = 0.8
        elif lugar in ['asakusa', 'ueno']:
            ajustes['complejidad'] = 0.4
            ajustes['intensidad'] = 0.4
        
        return ajustes

