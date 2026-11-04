package com.cimentacion.papascochero;

import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.webkit.JavascriptInterface;

/** Puente con el juego: abrir enlaces fuera y avisos de la liga online. */
public class Bridge {
    private final Activity a;

    public Bridge(Activity a) {
        this.a = a;
    }

    @JavascriptInterface
    public void open(String url) {
        try {
            a.startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        } catch (Exception e) { }
    }

    @JavascriptInterface
    public void perm() {
        if (Build.VERSION.SDK_INT >= 33
                && a.checkSelfPermission("android.permission.POST_NOTIFICATIONS") != PackageManager.PERMISSION_GRANTED) {
            a.runOnUiThread(() -> a.requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"}, 3));
        }
    }

    @JavascriptInterface
    public void notify(String title, String text) {
        try {
            NotificationManager nm = (NotificationManager) a.getSystemService(Activity.NOTIFICATION_SERVICE);
            if (Build.VERSION.SDK_INT >= 26) {
                nm.createNotificationChannel(new NotificationChannel("liga", "Liga online", NotificationManager.IMPORTANCE_DEFAULT));
            }
            Intent i = new Intent(a, MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
            PendingIntent pi = PendingIntent.getActivity(a, 0, i, PendingIntent.FLAG_IMMUTABLE);
            Notification.Builder nb = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(a, "liga") : new Notification.Builder(a);
            nb.setSmallIcon(android.R.drawable.star_on).setContentTitle(title).setContentText(text).setAutoCancel(true).setContentIntent(pi);
            nm.notify((int) (System.currentTimeMillis() % 100000), nb.build());
        } catch (Exception e) { }
    }
}
