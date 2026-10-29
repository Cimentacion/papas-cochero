#!/usr/bin/env python3
"""Genera los audios de los comentaristas con Kokoro (voces de hombre em_alex / em_santa).
Uso: python3 tools/gen_voices.py kokoro-v1.0.onnx voices-v1.0.bin
Modelos: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0  (pip install kokoro-onnx soundfile)
Lee las frases de tools/vol.json y los nombres del código del juego. Escribe audio/*.mp3 y audio/manifest.json"""
import json,re,sys,os,wave,subprocess,unicodedata,tempfile
import soundfile as sf
from kokoro_onnx import Kokoro
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"audio");os.makedirs(OUT,exist_ok=True)
vol=json.load(open(os.path.join(ROOT,"tools","vol.json"),encoding="utf-8"))
src=open(os.path.join(ROOT,"src-papas-cochero.html"),encoding="utf-8").read()
names=set()
for arr in ("MALE","FEM","MOTE","FIRSTC"):
    m=re.search(r"const %s=(\[[^\]]*\])"%arr,src);names.update(json.loads(m.group(1)))
names.add("el entrenador")
def slug(t):
    t=unicodedata.normalize("NFD",t);t="".join(c for c in t if unicodedata.category(c)!="Mn").lower()
    return re.sub(r"[^a-z0-9]+","_",t).strip("_")
# (voz kokoro, velocidad, tono)
VOICES={("normal",0):("em_alex",1.05,1.0),("normal",1):("em_santa",0.95,0.94),("paleto",0):("em_alex",1.0,1.1),("paleto",1):("em_santa",0.88,0.86)}
EQ={("normal",0):"",("normal",1):",equalizer=f=170:t=q:w=1:g=4",("paleto",0):",equalizer=f=1400:t=q:w=1:g=6,highpass=f=250",("paleto",1):",equalizer=f=150:t=q:w=1:g=5,lowpass=f=4500"}
HOT={"goalUs","post","penUs","red","shot","save","goalThem","penThem","offside"}
kok=Kokoro(sys.argv[1],sys.argv[2])
keys=[]
def synth(text,key,style,spk,ev=""):
    vk=("paleto" if style=="paleto" else "normal",spk);v,sp,pitch=VOICES[vk]
    hot=ev in HOT and style!="paleto"
    if hot:sp*=1.15;pitch*=1.05
    a,sr=kok.create(text,voice=v,speed=sp,lang="es")
    with tempfile.NamedTemporaryFile(suffix=".wav",delete=False) as f:tmp=f.name
    sf.write(tmp,a,sr)
    color="highpass=f=90,acompressor=threshold=-18dB:ratio=3:attack=5:release=80"
    af=(f"asetrate={sr}*{pitch},aresample={sr},atempo={1/pitch:.4f}," if pitch!=1 else "")+color+EQ[vk]+(",volume=1.9" if hot else ",volume=1.5")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",tmp,"-af",af,"-ac","1","-ar","24000","-c:a","libmp3lame","-b:a","48k",os.path.join(OUT,key+".mp3")],check=True)
    os.remove(tmp);keys.append(key)
for style,evs in vol.items():
    for ev,lines in evs.items():
        for i,t in enumerate(lines):
            spk=(i%2) if (style=="paleto" and ev=="b_any") else (1 if ev.startswith("b_") else 0)
            synth(t,f"{style}_{ev}_{i}",style,spk,ev)
for n in sorted(names):synth(n+"!" if True else n,"n_"+slug(n),"normal",0)
json.dump({"keys":keys},open(os.path.join(OUT,"manifest.json"),"w"))
print(len(keys),"audios")
