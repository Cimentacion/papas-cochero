#!/usr/bin/env python3
"""Genera la edición para Google Play (carpeta play/) a partir de src-papas-cochero.html.

Quita todo lo que tiene dueño: clubes reales, jugadores reales, leyendas reales,
estadios, árbitros, marcas, competiciones y confederaciones con marca registrada.
Uso:  python3 tools/build_play.py
"""
import json, os, re, sys, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src-papas-cochero.html')
OUT = os.path.join(ROOT, 'play')
MAIN_URL = 'https://cimentacion.github.io/papas-cochero/'
PLAY_URL = MAIN_URL + 'play/'

s = open(SRC, encoding='utf-8').read()

def h(x):
    return int(hashlib.md5(x.encode('utf-8')).hexdigest(), 16)

def block(start):
    """Devuelve el texto de una constante JS desde `start` hasta el ; de cierre de nivel 0."""
    i = s.index(start)
    depth = 0; j = i + len(start); instr = None
    while j < len(s):
        c = s[j]
        if instr:
            if c == '\\': j += 2; continue
            if c == instr: instr = None
        elif c in '"\'`': instr = c
        elif c in '[{(': depth += 1
        elif c in ']})':
            depth -= 1
        elif c == ';' and depth == 0:
            return i, j + 1
        j += 1
    raise ValueError(start)

def get_block(start):
    a, b = block(start); return s[a:b]

# ---------- 1) clubes reales -> inventados ----------
clubs = {}  # real -> town
for name in ['const BIG=', 'const TIER_REAL=', 'const TOP_TEAMS=']:
    for m in re.finditer(r'\["([^"]+)","([^"]+)"\]', get_block(name)):
        clubs.setdefault(m.group(1), m.group(2))
eu = []
for m in re.finditer(r'\["([^"]+)","([A-Z]{3})",\d', get_block('const EUCLUBS=')):
    eu.append((m.group(1), m.group(2)))

ES_SUF = ['Balompié Vecinal', 'Club Popular', 'Peña Futbolera', 'Deportivo Municipal', 'Atlético Comarcal',
          'Sporting Vecinal', 'Racing Popular', 'Olímpico Local', 'Juventud Deportiva', 'Unión Barriada',
          'Club de la Plaza', 'Deportivo del Mercado', 'Balompié de la Feria', 'Agrupación Futbolera']
EU_SUF = ['Football Club Vecinal', 'Rovers Popular', 'Athletic Local', 'Sporting Barriada', 'Olympique Vecinal',
          'Union Popular', 'Wanderers Local', 'Calcio Popolare', 'Sportverein Vecinal', 'Racing Popular']
STOP = set('FC CF AC SC SS AS RC CD UD SD CA AD CE RCD Real Club United City Athletic Athletico Atlético Atletico Bayern Borussia Inter Internazionale Juventus Olympique Sporting Racing Deportivo de del la los las Balompié Calcio Football Hotspur Rovers Wanderers Albion Villa Town County 1. 04 05 1899 1909 1846 Sport Lisboa e Benfica Ajax PSV Feyenoord Celtic Rangers Shakhtar Dinamo Dynamo Red Bull Galatasaray Fenerbahçe Beşiktaş Olympiacos Panathinaikos Napoli Milan Roma Lazio Atalanta Fiorentina Porto Braga Brugge Anderlecht Saint-Germain Marseille Lyonnais Monaco Lille Eintracht Bayer VfB VfL Hertha Werder Schalke Union Salzburg Sturm Slavia Sparta Zagreb Basel Young Boys Copenhagen Malmö Bodø/Glimt Glimt Bodø Lazio Sociedad Betis Valencia Villarreal Osasuna Celta Getafe Mallorca Girona Alavés Espanyol Leganés'.split())
COUNTRY_CITY = {'ENG': 'Londinium', 'ESP': 'Villarriba', 'ITA': 'Borgo', 'GER': 'Kleinstadt', 'FRA': 'Petitville', 'POR': 'Vilarinho',
                'NED': 'Dorpstad', 'BEL': 'Bourgval', 'TUR': 'Köyşehir', 'SCO': 'Wee Burgh', 'AUT': 'Dorfburg', 'SUI': 'Bergdorf',
                'CZE': 'Malé Město', 'GRE': 'Mikropoli', 'CRO': 'Selo', 'UKR': 'Selyshche', 'DEN': 'Lilleby', 'NOR': 'Smaby', 'SRB': 'Selo'}

used = set(clubs) | {n for n, _ in eu}
mapping = {}

def pick_name(base, sufs, key):
    k = h(key)
    for i in range(len(sufs)):
        cand = f'{base} {sufs[(k + i) % len(sufs)]}'
        if cand not in used:
            used.add(cand); return cand
    cand = f'{base} {sufs[k % len(sufs)]} {k % 97}'; used.add(cand); return cand

for real, town in clubs.items():
    mapping[real] = pick_name(town, ES_SUF, real)
for real, cc in eu:
    if real in mapping: continue
    words = [w for w in re.split(r'\s+', real) if w and w not in STOP and not re.match(r'^\d', w)]
    base = max(words, key=len) if words else COUNTRY_CITY.get(cc, 'Villa')
    if base in ('Madrid', 'Barcelona', 'München', 'Manchester', 'London', 'Milano', 'Lisboa', 'Liverpool', 'Paris'):
        pass
    mapping[real] = pick_name(base, EU_SUF, real)

# equipos locales con marca
mapping['Cerveza Cruzcampo'] = 'Cerveza La Campiña'

# ---------- 2) jugadores, leyendas, caras y estadios reales fuera ----------
def replace_block(start, new):
    global s
    a, b = block(start); s = s[:a] + new + s[b:]

replace_block('const REAL_SQ=', 'const REAL_SQ={};')
replace_block('const REAL_LOOK=', 'const REAL_LOOK={};')
replace_block('const STAD_REAL=', 'const STAD_REAL={};')
# sedes del Mundial/Eurocopa: solo la ciudad
def _nven(txt):
    seen = {}
    def r(m):
        city = m.group(2); n = seen.get(city, 0); seen[city] = n + 1
        return '"' + ['Estadio de ', 'Estadio Olímpico de ', 'Campo Municipal de ', 'Estadio Nuevo de '][min(n, 3)] + city + ', ' + city + '"'
    return re.sub(r'"([^",]+), ([^"]+)"', r, txt)
_a, _b = block('const NVEN=')
s = s[:_a] + _nven(s[_a:_b]) + s[_b:]
replace_block('const CANON_REAL=', 'const CANON_REAL=["Shun «Shinkansen» Aoki","Long «Dragón» Ma","Ha-joon «K-Pop» Lee"];')
LEG = [["Iván «El Muro» Petrovski", "POR"], ["Carlinhos «Pulmão» Torreira", "DEF"], ["Franz «El Káiser» Brauner", "DEF"], ["Bobby «Roca» Moorland", "DEF"],
       ["Giacomo «Il Treno» Fabbri", "DEF"], ["Jan «El Flaco» Krujff", "MED"], ["Doutor Sabino", "MED"], ["Alfredo «La Saeta» Distéfani", "MED"],
       ["Dieguito «El Pelusa» Marrero", "DEL"], ["O Reizinho", "DEL"], ["Eusebinho «La Pantera»", "DEL"], ["Ferenc «Cañoncito» Puskar", "DEL"],
       ["Gerd «El Torpedo» Müllner", "DEL"], ["Mané «Piernas Torcidas»", "DEL"], ["Bobby «Bigote» Charlwood", "MED"], ["Luisito «El Arquitecto» Suaz", "MED"]]
replace_block('const LEGENDS=', 'const LEGENDS=' + json.dumps(LEG, ensure_ascii=False) + ';')

# ---------- 3) sustituciones de texto (largo primero) ----------
TXT = {
    # personas reales mencionadas en frases
    'Yashin, Beckenbauer, Cruyff, Di Stéfano, Maradona, Pelé, Eusébio': 'Petrovski, Brauner, Krujff, Distéfani, Marrero, O Reizinho, Eusebinho',
    'Yashin, Beckenbauer, Cruyff, Di Stéfano, Maradona, Pelé': 'Petrovski, Brauner, Krujff, Distéfani, Marrero, O Reizinho',
    '["Mamadou","Diallo","Pelé","Eusébio","Garrincha","Sócrates"].forEach(n=>m[n]=n==="Sócrates"?"trop":n==="Garrincha"?"trop":"afri");': '["Mamadou","Diallo"].forEach(n=>m[n]="afri");',
    'el Messi del barrio': 'el crack del barrio', 'Maradona, Pelé': 'las leyendas del fútbol', 'Maradona': 'Marrero', 'Pelé': 'O Reizinho',
    'Pepe Gil Manzano': 'Pepe Gil Manzanares', 'Mateu Lahuerta': 'Mateo Lahuerta',
    # marcas
    'Mercadona': 'supermercado', 'Lidl': 'súper de la rotonda', 'Ducados': 'Celtas sin filtro', 'Phoskitos': 'pastelitos', 'Mahou': 'cerveza',
    'Cruzcampo': 'La Campiña', 'Spotify ': '', 'Riyadh Air ': '', 'Reale Arena': 'Arena', 'Abanca-': '',
    'Coca-Cola': 'refresco de cola',
    # competiciones y organismos con marca
    'UEFA Champions League': 'Liga de Campeones Continental', 'Champions League': 'Liga de Campeones Continental', 'Champions': 'Liga de Campeones',
    'UEFA Europa League': 'Copa Continental', 'Europa League': 'Copa Continental', 'UEFA Conference League': 'Trofeo Continental', 'Conference League': 'Trofeo Continental',
    'título UEFA B': 'título de entrenador nivel B', 'Copa del Rey': 'Copa Nacional', 'Bota de Oro': 'Bota de Hojalata',
}
CONF = {'"UEFA"': '"EUR"', '"CONMEBOL"': '"SUD"', '"CONCACAF"': '"NCA"', '"CAF"': '"AFR"', '"AFC"': '"ASI"', '"OFC"': '"OCE"'}

def subst(text):
    # clubes (cadenas entre comillas y texto suelto), primero los nombres largos
    for real in sorted(mapping, key=len, reverse=True):
        text = text.replace(real, mapping[real])
    for k in sorted(TXT, key=len, reverse=True):
        text = text.replace(k, TXT[k])
    for k, v in CONF.items():
        text = text.replace(k, v)
    text = re.sub(r'\{UEFA:(\d+),CAF:(\d+),AFC:(\d+),CONMEBOL:(\d+),CONCACAF:(\d+),OFC:',r'{EUR:\1,AFR:\2,ASI:\3,SUD:\4,NCA:\5,OCE:',text)
    text = text.replace('la FIFA', 'la Federación').replace('la UEFA', 'la Confederación').replace('FIFA, dólares', 'Federación, dólares').replace('UEFA, euros', 'Confederación, euros')
    text = re.sub(r'\bUEFA\b', 'Confederación', text)
    text = re.sub(r'\bFIFA\b', 'Federación', text)
    return text

s = subst(s)

# ---------- 4) que se actualice desde play/ y use los audios de la web principal ----------
s = s.replace(f'window.PC_REMOTE="{MAIN_URL}"', f'window.PC_REMOTE="{PLAY_URL}";window.PC_PLAY=1', 1)
assert 'window.PC_PLAY=1' in s
s = s.replace('VOX.base=(location.href.indexOf(window.PC_REMOTE)===0?"":window.PC_REMOTE)+"audio/"', f'VOX.base="{MAIN_URL}audio/"')
assert f'VOX.base="{MAIN_URL}audio/"' in s
s = s.replace('localStorage.getItem("pc_code")', 'localStorage.getItem("pcp_code")').replace('localStorage.getItem("pc_codev")', 'localStorage.getItem("pcp_codev")')
s = s.replace('localStorage.setItem("pc_code"', 'localStorage.setItem("pcp_code"').replace('localStorage.setItem("pc_codev"', 'localStorage.setItem("pcp_codev"')

# ---------- 5) comprobación: no queda nada real ----------
src0 = open(SRC, encoding='utf-8').read()
reals = set(clubs) | {n for n, _ in eu}
for m in re.finditer(r'\["([^"]+)","(?:POR|DEF|MED|DEL)",\d', src0[src0.index('const REAL_SQ='):src0.index('const REAL_SQ=') + 200000]):
    nm = m.group(1)
    if len(nm) >= 6: reals.add(nm)
for m in re.finditer(r'\["([^"]+)","(?:POR|DEF|MED|DEL)"\]', get_block('const LEGENDS=') if False else src0[src0.index('const LEGENDS='):src0.index('const LEGENDS=') + 3000]):
    reals.add(m.group(1))
for k in ['Real Madrid', 'FC Barcelona', 'Messi', 'Maradona', 'Pelé', 'Cruyff', 'Beckenbauer', 'Mbappé', 'Spotify', 'Riyadh', 'Mercadona', 'Cruzcampo', 'Ducados', 'Champions', 'UEFA', 'FIFA', 'Copa del Rey', 'Bernabéu', 'Camp Nou']:
    reals.add(k)
left = sorted({r for r in reals if (' ' in r or len(r)>8 or r in ('Pelé','Messi','UEFA','FIFA')) and r in s and r not in ('Guilherme',) and r not in mapping.values() and not any(r in v for v in mapping.values())})
if left:
    open('/tmp/claude-0/t/play_fail.html','w',encoding='utf-8').write(s); print('QUEDAN NOMBRES REALES:', left[:80]); sys.exit(1)

# ---------- 6) escribir ----------
os.makedirs(os.path.join(OUT, 'i18n'), exist_ok=True)
head = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read().split('<body>')[0] + '<body>'
head = head.replace('icon-180.png', '../icon-180.png').replace('manifest.webmanifest', '../manifest.webmanifest')
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(head + s + '</body></html>')
v = re.search(r'window\.PC_VERSION="([^"]+)"', s).group(1)
notes = json.load(open(os.path.join(ROOT, 'version.json'), encoding='utf-8'))['notes']
json.dump({'v': v, 'notes': [subst(n) for n in notes]}, open(os.path.join(OUT, 'version.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for f in os.listdir(os.path.join(ROOT, 'i18n')):
    arr = json.load(open(os.path.join(ROOT, 'i18n', f), encoding='utf-8'))
    json.dump([subst(x) for x in arr], open(os.path.join(OUT, 'i18n', f), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(mapping, open(os.path.join(ROOT, 'tools', 'clubs-map.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('ok', v, len(mapping), 'clubes renombrados')
