package com.cimentacion.papascochero;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.WindowInsets;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.widget.FrameLayout;

public class MainActivity extends Activity {
    static final int FILE_REQ = 7;
    WebView web;
    Tts tts;
    ValueCallback<Uri[]> fileCb;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(Color.parseColor("#1a1208"));
        web = new WebView(this);
        root.addView(web, new FrameLayout.LayoutParams(-1, -1));
        setContentView(root);

        // Android 15+: la app se dibuja bajo las barras del sistema; dejamos hueco para no tapar el juego
        root.setOnApplyWindowInsetsListener((v, ins) -> {
            int top, bottom, left, right;
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets i = ins.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                top = i.top; bottom = i.bottom; left = i.left; right = i.right;
            } else {
                top = ins.getSystemWindowInsetTop(); bottom = ins.getSystemWindowInsetBottom();
                left = ins.getSystemWindowInsetLeft(); right = ins.getSystemWindowInsetRight();
            }
            v.setPadding(left, top, right, bottom);
            return ins;
        });

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setAllowFileAccess(true);
        s.setAllowFileAccessFromFileURLs(true);
        s.setAllowUniversalAccessFromFileURLs(true);
        s.setTextZoom(100);

        tts = new Tts(this);
        web.addJavascriptInterface(tts, "AndroidTTS");
        web.addJavascriptInterface(new Bridge(this), "AndroidBridge");

        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
                Uri u = req.getUrl();
                String sc = u.getScheme();
                if ("file".equals(sc)) return false;
                // los enlaces externos se abren fuera del juego
                try { startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (Exception e) { }
                return true;
            }
        });
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView w, ValueCallback<Uri[]> cb, FileChooserParams p) {
                if (fileCb != null) fileCb.onReceiveValue(null);
                fileCb = cb;
                try {
                    Intent i = p.createIntent();
                    startActivityForResult(i, FILE_REQ);
                } catch (Exception e) {
                    fileCb = null;
                    return false;
                }
                return true;
            }
        });

        if (b != null) web.restoreState(b);
        else web.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onActivityResult(int req, int res, Intent data) {
        super.onActivityResult(req, res, data);
        if (req == FILE_REQ && fileCb != null) {
            fileCb.onReceiveValue(WebChromeClient.FileChooserParams.parseResult(res, data));
            fileCb = null;
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        web.saveState(out);
    }

    @Override
    public void onBackPressed() {
        // Atrás: cierra la ventana abierta del juego; si no hay ninguna, manda la app al fondo
        web.evaluateJavascript(
            "(function(){var m=document.querySelector('#modal:not([hidden]) [data-act=close]');if(m){m.click();return 1}" +
            "var f=document.querySelector('#sdfull:not([hidden]) [data-act=sdclose],#docfull:not([hidden]) [data-act=docclose]');if(f){f.click();return 1}return 0})()",
            r -> { if (!"1".equals(r)) moveTaskToBack(true); });
    }

    @Override
    protected void onPause() {
        super.onPause();
        web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
    }

    @Override
    protected void onDestroy() {
        if (tts != null) tts.shutdown();
        web.destroy();
        super.onDestroy();
    }
}
