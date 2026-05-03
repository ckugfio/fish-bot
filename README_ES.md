# 🎣 Bot de Pesca v2.1

> **Bot automatizado de pesca para juegos de PC usando detección de color en pantalla**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green.svg)]()
[![Plataforma](https://img.shields.io/badge/Plataforma-Windows-lightgray.svg)]()

[Versión en inglés](README_EN.md)

---

## ✨ Características

- **Teclas personalizables**: Configura las teclas para lanzar, recoger y activar el bot
- **Detección por color**: Captura automáticamente el color del indicador de pesca
- **Selección de región**: Define el área de pantalla donde aparece el icono
- **Tolerancia de color ajustable**: Controla qué tan precisa debe ser la detección
- **Multilenguaje**: Interfaz en español e inglés
- **Tecla de acceso rápido**: Activa/desactiva el bot con una tecla configurable (por defecto F9)
- **Guarda configuración**: Guarda tus ajustes entre sesiones

## 📋 Requisitos

- Windows (utiliza APIs nativas de Windows para enviar teclas)
- Python 3.8 o superior

## 🚀 Instalación Rápida

1. **Clona o descarga** este repositorio
2. **Instala dependencias**:

```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Ejecutar desde código fuente:

```bash
python fishing_bot.py
```

### Crear ejecutable (.exe):

```bash
pyinstaller BotDePesca.spec
```

El ejecutable se generará en la carpeta `dist/`.

## ⚙️ Configuración

1. **Configura las teclas**:
   - Haz clic en cada tecla para cambiarla
   - **LANZAR**: Tecla para lanzar el sedal
   - **RECOGER**: Tecla para recoger el sedal
   - **INICIAR**: Tecla para activar/desactivar el bot

2. **Selecciona la región**:
   - Haz clic en "Seleccionar región"
   - Arrastra para definir la zona donde aparece el icono de pesca

3. **Selecciona el color**:
   - Usa "Paleta" para elegir un color manualmente
   - Usa "Pantalla" para capturar el color directamente del juego

4. **Ajusta la tolerancia**:
   - Aumenta si no detecta bien el color
   - Disminuye para detección más precisa

5. **Inicia el bot**:
   - Pulsa "INICIAR BOT" o la tecla configurada (F9 por defecto)

## 🔧 Cómo Funciona

El bot trabaja en un ciclo continuo:
1. **Lanza** el sedal (tecla configurada)
2. **Monitorea** la región seleccionada buscando el color del indicador
3. **Detecta** el color (picada) y recoge el sedal automáticamente
4. **Repite** el ciclo

## 📝 Configuración de ejemplo

```json
{
  "cast_key": "1",
  "reel_key": "2",
  "toggle_key": "f9",
  "region": [100, 100, 200, 200],
  "color": [255, 200, 100],
  "tolerance": 20,
  "language": "es"
}
```

Copia `config.json.example` a `config.json` y personalízalo.

## 📁 Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `fishing_bot.py` | Código fuente principal |
| `requirements.txt` | Dependencias de Python |
| `BotDePesca.spec` | Configuración de PyInstaller |
| `crear_exe.bat` | Script para compilar (español) |
| `build_exe.bat` | Script para compilar (inglés) |
| `config.json.example` | Ejemplo de configuración |

## 💡 Notas

- Usa la API `SendInput` de Windows para mejor compatibilidad con juegos
- No requiere que el juego esté constantemente en primer plano
- Puedes minimizar el bot mientras funciona
- Si el antivirus bloquea el ejecutable, agrega una excepción

## ⚠️ Advertencia

**Usar bajo tu propia responsabilidad**. Algunos juegos pueden considerar el uso de bots como una violación de sus términos de servicio.

---

**Versión**: 2.1
