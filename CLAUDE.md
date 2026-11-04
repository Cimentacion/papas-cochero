# Los Papas Cochero — notas para Claude

Juego de gestión de fútbol cutre (HTML de un solo archivo) + APK Android que lo envuelve.

## Archivos
- `src-papas-cochero.html`: código fuente del juego (lo que se edita).
- `index.html`: lo publicado en GitHub Pages = cabecera (doctype + head con charset, viewport, metas de iPhone `apple-mobile-web-app-*`, `apple-touch-icon` icon-180.png, `manifest.webmanifest`, title) + `<body>` + fuente + `</body></html>`. Copiar la cabecera tal cual está en el index.html actual (todo hasta `<body>`).
- `icon-180.png`, `icon-192.png`, `icon-512.png`, `manifest.webmanifest`: para instalarlo en iPhone/Android desde el navegador.
- `version.json`: `{"v":"X.Y","notes":[...]}`. La app compara con `window.PC_VERSION` (en la fuente) y se actualiza sola.
- `PapasCochero.apk`: APK descargable. `apk/apkproj`: proyecto apktool (smali con WebView, puente de voz `AndroidTTS` y `AndroidBridge.open(url)`).
- **Edición Google Play** (sin nada con copyright): `python3 tools/build_play.py` genera `play/` (index.html, version.json, i18n) desde la fuente, cambiando clubes, jugadores, leyendas, estadios, árbitros, marcas y competiciones reales por inventados. Se actualiza desde `play/`. Hay que regenerarla en cada versión. `play/privacy.html` = política de privacidad.
- `android-play/`: proyecto Android (Java, WebView) para Play. `.github/workflows/play-aab.yml` lo compila al cambiar `android-play/` (o a mano con «Run workflow») y deja el AAB/APK sin firmar y el log en la rama `play-build`. Se firma fuera con la clave de subida del dueño (no está en el repo).
- `tests/run.js`: partida automática con jsdom (`npm i jsdom@24`), debe acabar con `errors []`.

## Flujo para aplicar peticiones (issues con etiqueta `peticion`)
1. Leer issues abiertos. 2. Editar `src-papas-cochero.html`. 3. Subir `window.PC_VERSION` (ej. 7.5 -> 7.6).
4. Regenerar `index.html`, actualizar `version.json` (misma versión + notas cortas en español) y ejecutar `python3 tools/build_play.py`.
5. Probar (node --check del script y `tests/run.js`). 6. Commit + push a `main`. 7. Comentar y cerrar el issue.
El usuario habla español, quiere respuestas directas. No cambiar el aspecto del visor de partido si no lo pide.
