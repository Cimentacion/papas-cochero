# Los Papas Cochero — notas para Claude

Juego de gestión de fútbol cutre (HTML de un solo archivo) + APK Android que lo envuelve.

## Archivos
- `src-papas-cochero.html`: código fuente del juego (lo que se edita).
- `index.html`: lo publicado en GitHub Pages = `<!doctype html><html lang="es"><head><meta charset="utf-8"></head><body>` + fuente + `</body></html>`.
- `version.json`: `{"v":"X.Y","notes":[...]}`. La app compara con `window.PC_VERSION` (en la fuente) y se actualiza sola.
- `PapasCochero.apk`: APK descargable. `apk/apkproj`: proyecto apktool (smali con WebView, puente de voz `AndroidTTS` y `AndroidBridge.open(url)`).
- `tests/run.js`: partida automática con jsdom (`npm i jsdom@24`), debe acabar con `errors []`.

## Flujo para aplicar peticiones (issues con etiqueta `peticion`)
1. Leer issues abiertos. 2. Editar `src-papas-cochero.html`. 3. Subir `window.PC_VERSION` (ej. 7.5 -> 7.6).
4. Regenerar `index.html`, actualizar `version.json` (misma versión + notas cortas en español).
5. Probar (node --check del script y `tests/run.js`). 6. Commit + push a `main`. 7. Comentar y cerrar el issue.
El usuario habla español, quiere respuestas directas. No cambiar el aspecto del visor de partido si no lo pide.
