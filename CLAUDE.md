# Estudio de edición de video

Este repo es un estudio de edición de video. Responde siempre en español.

## Al empezar una sesión

Si `whisper`, `yt-dlp` o `earshot` no están instalados (`which whisper yt-dlp earshot`),
corre `./setup-video-tools.sh` antes de editar.

## Cuando el usuario sube un video o pega un enlace

Hazlo en automático, sin esperar a que nombre las herramientas:

1. **Entrada**
   - Archivo subido: cópialo a `videos/originales/`.
   - Enlace (Reel, TikTok, YouTube): descárgalo con `yt-dlp` a `videos/referencias/`.
2. **Analiza** con `ffprobe` (duración, resolución, fps) y saca cuadros clave con `ffmpeg`
   para ver el contenido.
3. **Escucha**
   - Transcribe con `whisper` (`--language Spanish --output_format srt`) y guarda el `.srt`
     junto al video.
   - Detecta silencios (`ffmpeg -af silencedetect`) para proponer cortes.
   - Revisa el audio con las herramientas MCP de earshot (`measure`, `timeline`).
4. **Pregunta antes de editar.** Muestra un resumen (de qué trata, duración, silencios,
   calidad del audio) y propone qué hacer.
5. **Edita** según lo que pida el usuario:
   - Textos, gráficas, transiciones, subtítulos animados: skills de **HyperFrames**.
   - Copiar el estilo de un video de referencia: skill **reverse-any-video**, o
     **style-sampling**.
   - Efectos de sonido, música y mezcla: skills **earshot** y **real-sound**.
     La voz siempre debe oírse por encima de la música.
   - Escenas o personajes 3D: conector **blender**, que solo funciona si Blender está
     abierto en la computadora del usuario.
6. **Entrega** el resultado en `videos/finales/` y envíalo al usuario.

## Reglas

- Nunca sobrescribas el video original.
- Por defecto, exporta en vertical 1080x1920 para Reels/TikTok, salvo que el usuario pida
  otro formato.
- No subas videos pesados a git. `videos/` está en `.gitignore`.
