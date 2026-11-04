package com.cimentacion.papascochero;

import android.content.Context;
import android.speech.tts.TextToSpeech;
import android.speech.tts.Voice;
import android.webkit.JavascriptInterface;
import java.util.Locale;

/** Voz de los comentaristas: el juego llama a AndroidTTS.speak/flush/pitch/voices/voice. */
public class Tts implements TextToSpeech.OnInitListener {
    private TextToSpeech tts;
    private boolean ready = false;

    public Tts(Context c) {
        tts = new TextToSpeech(c, this);
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            try { tts.setLanguage(new Locale("es", "ES")); } catch (Exception e) { }
            ready = true;
        }
    }

    @JavascriptInterface
    public void speak(String t) {
        if (ready && t != null) tts.speak(t, TextToSpeech.QUEUE_ADD, null, "pc");
    }

    @JavascriptInterface
    public void flush(String t) {
        if (ready && t != null) tts.speak(t, TextToSpeech.QUEUE_FLUSH, null, "pc");
    }

    @JavascriptInterface
    public void pitch(float p) {
        if (ready) tts.setPitch(p);
    }

    @JavascriptInterface
    public String voices() {
        if (!ready) return "";
        StringBuilder sb = new StringBuilder();
        try {
            for (Voice v : tts.getVoices()) {
                Locale l = v.getLocale();
                if (l != null && "es".equals(l.getLanguage()) && !v.isNetworkConnectionRequired()) {
                    if (sb.length() > 0) sb.append('|');
                    sb.append(v.getName());
                }
            }
        } catch (Exception e) { }
        return sb.toString();
    }

    @JavascriptInterface
    public void voice(String name) {
        if (!ready || name == null) return;
        try {
            for (Voice v : tts.getVoices()) {
                if (name.equals(v.getName())) { tts.setVoice(v); return; }
            }
        } catch (Exception e) { }
    }

    public void shutdown() {
        try { tts.stop(); tts.shutdown(); } catch (Exception e) { }
    }
}
