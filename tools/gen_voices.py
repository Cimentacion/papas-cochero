#!/usr/bin/env python3
"""Genera los audios de los comentaristas (voz de hombre, Piper es_ES carlfm).
Uso: python3 tools/gen_voices.py MODELO.onnx
Modelo: https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-es-carlfm-x-low.tar.gz
Lee las frases de tools/vol.json y los nombres del código del juego. Escribe audio/*.mp3 y audio/manifest.json"""
import json,re,sys,os,wave,subprocess,unicodedata,tempfile
from piper import PiperVoice
from piper.config import SynthesisConfig
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"audio");os.makedirs(OUT,exist_ok=True)
vol=json.load(open(os.path.join(ROOT,"tools","vol.json"),encoding="utf-8"))
src=open(os.path.join(ROOT,"src-papas-cochero.html"),encoding="utf-8").read()
names=set()
for arr in ("MALE","FEM","MOTE"):
    m=re.search(r"const %s=(\[[^\]]*\])"%arr,src);names.update(json.loads(m.group(1)))
names.add("el entrenador")
def slug(t):
    t=unicodedata.normalize("NFD",t);t="".join(c for c in t if unicodedata.category(c)!="Mn").lower()
    return re.sub(r"[^a-z0-9]+","_",t).strip("_")
VOICES={("normal",0):(0.92,1.04),("normal",1):(1.12,0.76),("paleto",0):(1.02,1.16),("paleto",1):(1.3,0.7)}
EQ={("normal",0):"",("normal",1):",equalizer=f=180:t=q:w=1:g=5",("paleto",0):",equalizer=f=1400:t=q:w=1:g=7,highpass=f=300",("paleto",1):",equalizer=f=150:t=q:w=1:g=6,lowpass=f=4000"}
HOT={"goalUs","post","penUs","red","shot","save","goalThem","penThem","offside"}
voice=PiperVoice.load(sys.argv[1])
keys=[]
def synth(text,key,style,spk,ev=""):
    vk=("paleto" if style=="paleto" else "normal",spk);ls,pitch=VOICES[vk]
    hot=ev in HOT and style!="paleto"
    if hot:ls*=0.84;pitch*=1.09
    with tempfile.NamedTemporaryFile(suffix=".wav",delete=False) as f:tmp=f.name
    with wave.open(tmp,"wb") as w:voice.synthesize_wav(text,w,syn_config=SynthesisConfig(length_scale=ls,noise_scale=0.9 if hot else 0.8,noise_w_scale=1.1 if hot else 0.95))
    color="highpass=f=110,lowpass=f=6800,aecho=0.8:0.6:35:0.12,acompressor=threshold=-18dB:ratio=3:attack=5:release=80"
    af=(f"asetrate=16000*{pitch},aresample=22050,atempo={1/pitch:.4f}," if pitch!=1 else "aresample=22050,")+color+EQ[vk]+(",volume=2.0" if hot else ",volume=1.6")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",tmp,"-af",af,"-ac","1","-c:a","libmp3lame","-b:a","40k",os.path.join(OUT,key+".mp3")],check=True)
    os.remove(tmp);keys.append(key)
for style,evs in vol.items():
    for ev,lines in evs.items():
        for i,t in enumerate(lines):
            spk=(i%2) if (style=="paleto" and ev=="b_any") else (1 if ev.startswith("b_") else 0)
            synth(t,f"{style}_{ev}_{i}",style,spk,ev)
for n in sorted(names):synth(n+"!" if True else n,"n_"+slug(n),"normal",0)
json.dump({"keys":keys},open(os.path.join(OUT,"manifest.json"),"w"))
print(len(keys),"audios")
