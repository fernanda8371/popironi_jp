# 🎵 Generador de Melodías IA - Popironi

Sistema de generación de melodías basado en sentimientos y lugares usando IA y síntesis de audio.

## 🌟 Características

- **Generación de melodías únicas** basadas en:
  - 🎭 **Sentimientos**: Feliz, Triste, Enérgico, Calmado, Misterioso, Romántico, Melancólico, Nostálgico
  - 📍 **Lugares**: Playa, Bosque, Ciudad, Montaña, Desierto, Espacio, Cafetería, Lluvia

- **Características musicales dinámicas**:
  - Tempo adaptativo según el sentimiento
  - Frecuencias y tonalidades específicas
  - Ruido ambiente según el lugar
  - Envolventes ADSR para notas naturales

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior

### Pasos de instalación

1. **Clonar el repositorio** (si aplica)
```bash
git clone <tu-repo>
cd popironi
```

2. **Crear entorno virtual** (recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o en Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 🎮 Uso

1. **Iniciar el servidor**
```bash
python app.py
```

2. **Abrir en el navegador**
```
http://localhost:5000
```

3. **Generar melodías**:
   - Selecciona un sentimiento
   - Selecciona un lugar
   - Haz clic en "Generar Melodía"
   - Escucha y descarga tu melodía única

## 📁 Estructura del Proyecto

```
popironi/
├── app.py                 # Servidor Flask y lógica de generación
├── requirements.txt       # Dependencias Python
├── templates/
│   └── index.html        # Interfaz web
└── generated_audio/      # Carpeta de melodías generadas (auto-creada)
```

## 🎼 Cómo Funciona

### Sistema de Generación

1. **Mapeo de Sentimientos**: Cada sentimiento se mapea a características musicales:
   - Tempo (muy lento a muy rápido)
   - Tonalidad (mayor/menor)
   - Conjunto de frecuencias (notas musicales)

2. **Mapeo de Lugares**: Cada lugar añade ambiente:
   - Tipo de reverberación
   - Ruido ambiental característico
   - Textura sonora

3. **Síntesis de Audio**:
   - Generación de ondas senoidales para notas
   - Aplicación de envolventes ADSR
   - Adición de armónicos
   - Mezcla con ruido ambiente

4. **Resultado**: Archivo WAV de ~15 segundos con melodía única

## 🎨 Sentimientos Disponibles

- **Feliz**: Tempo rápido, tonalidad mayor, notas brillantes
- **Triste**: Tempo lento, tonalidad menor, notas graves
- **Enérgico**: Tempo muy rápido, notas agudas
- **Calmado**: Tempo muy lento, notas suaves
- **Misterioso**: Tempo lento, notas cromáticas
- **Romántico**: Tempo medio, progresiones suaves
- **Melancólico**: Tempo lento, tonalidad menor
- **Nostálgico**: Tempo medio, armonías complejas

## 🌍 Lugares Disponibles

- **Playa**: Ondas, reverb alto
- **Bosque**: Pájaros, ambiente natural
- **Ciudad**: Reverb bajo, urbano
- **Montaña**: Viento, espacioso
- **Desierto**: Silencio, árido
- **Espacio**: Etéreo, reverb muy alto
- **Cafetería**: Murmullos, acogedor
- **Lluvia**: Gotas, ambiente húmedo

## 🛠️ Tecnologías

- **Backend**: Python, Flask
- **Procesamiento de Audio**: NumPy, SciPy
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Audio**: Formato WAV, 44.1kHz

## 💡 Características Técnicas

- **100% Gratis**: Sin APIs de pago, todo local
- **Síntesis en tiempo real**: Generación en segundos
- **Formato estándar**: Archivos WAV compatibles
- **Sin límites**: Genera tantas melodías como quieras
- **Ligero**: Sin modelos ML pesados

## 🔧 Personalización

Puedes personalizar las características editando `app.py`:

```python
# Agregar nuevo sentimiento
SENTIMIENTOS['tuno'] = {
    'tempo': 'rápido',
    'tonalidad': 'mayor',
    'frecuencias': [440, 554, 659, 784]
}

# Agregar nuevo lugar
LUGARES['cueva'] = {
    'ambiente': 'resonante',
    'reverb': 'muy_alto',
    'ruido': 'eco'
}
```

## 📝 Notas

- Los archivos de audio se guardan en `generated_audio/`
- Cada archivo incluye timestamp para evitar sobrescrituras
- Puedes limpiar archivos antiguos con el endpoint `/limpiar`

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Siéntete libre de:
- Agregar nuevos sentimientos
- Agregar nuevos lugares
- Mejorar la síntesis de audio
- Mejorar la interfaz

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## 🎯 Demo

Este es un proyecto de demostración que muestra cómo combinar:
- Síntesis de audio procedural
- Mapeo emocional a características musicales
- Generación paramétrica de melodías
- Interfaz web interactiva

---

**¡Disfruta creando melodías únicas! 🎶**
