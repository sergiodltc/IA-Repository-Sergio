#!/usr/bin/env bash
# Instala las 5 herramientas de edición de video para Claude Code.
set -e
# 1. HyperFrames (skills de animación HTML -> video). Ya incluidas en .claude/skills;
#    para actualizarlas:
npx -y skills add heygen-com/hyperframes --all --agent claude-code -y
# 2. Whisper (transcripción y subtítulos)
pip install -U openai-whisper
# 3. yt-dlp (descargar Reels/videos de referencia)
pip install -U yt-dlp
# 4. Blender MCP (requiere Blender abierto con el addon de github.com/ahujasid/blender-mcp)
uv tool install blender-mcp || true
# 5. earshot (ingeniero de sonido, MCP)
uv tool install "earshot[mcp] @ git+https://github.com/Leonxlnx/earshot" || pip install "earshot[mcp] @ git+https://github.com/Leonxlnx/earshot"
echo "Listo. Reinicia Claude Code para cargar los servidores MCP de .mcp.json"
