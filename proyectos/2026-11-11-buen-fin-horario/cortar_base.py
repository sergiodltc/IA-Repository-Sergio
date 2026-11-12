"""Arma la base: toma solo las frases correctas, quita silencios y une todo en un clip."""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIG = ROOT.parent / "originales"
OUT = ROOT / "base.mp4"

# (clip, [(inicio, fin), ...]) en segundos: intervalos de voz de la toma correcta
SEGMENTOS = [
    ("IMG_9248", [(13.90, 16.68)]),               # No mande los correos de buen fin de tu tienda de Shopify antes de ver esto
    ("IMG_9249", [(0.57, 4.62)]),                 # La mayoría de las marcas mandan sus correos en horas cerradas...
    ("IMG_9250", [(4.21, 4.84), (5.19, 7.93)]),   # ya que es uno de los horarios más comunes...
    ("IMG_9251", [(0.99, 3.25), (3.80, 7.07)]),   # Pero lo que pasa es que básicamente todas las marcas...
    ("IMG_9252", [(0.82, 2.33)]),                 # El cliente se satura de correos
    ("IMG_9253", [(1.22, 2.60)]),                 # Y tu correo termina siendo olvidado
    ("IMG_9254", [(5.20, 7.61)]),                 # Pero si tú mandas tu correo por ejemplo a las nueve con siete
    ("IMG_9255", [(7.97, 10.41)]),                # Quedas hasta arriba de todos los correos...
    ("IMG_9256", [(0.00, 0.675), (2.54, 5.32)]),  # Así que serás de los primeros...
    ("IMG_9257", [(1.04, 3.98)]),                 # Mismo correo, mismo asunto, 7 minutos más tarde
    ("IMG_9258", [(1.20, 2.94), (4.10, 7.53)]),   # Comenta la palabra horario...
]
PRE, POST, FADE = 0.05, 0.08, 0.012

VF = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,"
      "format=yuv420p,scale=1080:1920,fps=30,setsar=1")

inputs, filtros, etiquetas, mapa = [], [], [], []
t_out = 0.0
for clip, partes in SEGMENTOS:
    for a, b in partes:
        a, b = max(0.0, a - PRE), b + POST
        i = len(inputs) // 6  # cada entrada agrega 6 argumentos
        inputs += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(ORIG / f"{clip}.MOV")]
        d = b - a
        filtros.append(f"[{i}:v]{VF},trim=duration={d:.3f},setpts=PTS-STARTPTS[v{i}]")
        filtros.append(f"[{i}:a]aresample=48000,atrim=duration={d:.3f},asetpts=PTS-STARTPTS,"
                       f"afade=t=in:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE}[a{i}]")
        etiquetas.append(f"[v{i}][a{i}]")
        mapa.append({"clip": clip, "src_in": round(a, 3), "src_out": round(b, 3),
                     "out_in": round(t_out, 3), "out_out": round(t_out + d, 3)})
        t_out += d

n = len(etiquetas)
filtros.append(f"{''.join(etiquetas)}concat=n={n}:v=1:a=1[v][araw]")
filtros.append("[araw]loudnorm=I=-14:TP=-1.5:LRA=11[a]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filtros),
       "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(OUT)]
subprocess.run(cmd, check=True)
(ROOT / "base_mapa.json").write_text(json.dumps(mapa, indent=1))
print(f"{OUT}  duración ≈ {t_out:.2f}s, {n} segmentos")
