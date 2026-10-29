.class public Lcom/papascochero/game/Bridge;
.super Ljava/lang/Object;

.field public act:Landroid/app/Activity;

.method public constructor <init>(Landroid/app/Activity;)V
    .registers 2
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lcom/papascochero/game/Bridge;->act:Landroid/app/Activity;
    return-void
.end method

.method public open(Ljava/lang/String;)V
    .registers 5
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_start
    new-instance v0, Landroid/content/Intent;
    const-string v1, "android.intent.action.VIEW"
    invoke-static {p1}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;
    move-result-object v2
    invoke-direct {v0, v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V
    const/high16 v1, 0x10000000
    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
    iget-object v1, p0, Lcom/papascochero/game/Bridge;->act:Landroid/app/Activity;
    invoke-virtual {v1, v0}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch
    return-void
    :catch
    move-exception v0
    return-void
.end method

.method public perm()V
    .registers 5
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_start
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I
    const/16 v1, 0x21
    if-lt v0, v1, :done
    const/4 v0, 0x1
    new-array v0, v0, [Ljava/lang/String;
    const/4 v1, 0x0
    const-string v2, "android.permission.POST_NOTIFICATIONS"
    aput-object v2, v0, v1
    iget-object v1, p0, Lcom/papascochero/game/Bridge;->act:Landroid/app/Activity;
    const/4 v2, 0x7
    invoke-virtual {v1, v0, v2}, Landroid/app/Activity;->requestPermissions([Ljava/lang/String;I)V
    :done
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch
    return-void
    :catch
    move-exception v0
    return-void
.end method

.method public notify(Ljava/lang/String;Ljava/lang/String;)V
    .registers 10
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_start
    iget-object v0, p0, Lcom/papascochero/game/Bridge;->act:Landroid/app/Activity;
    const-string v1, "notification"
    invoke-virtual {v0, v1}, Landroid/app/Activity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v1
    check-cast v1, Landroid/app/NotificationManager;
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I
    const/16 v3, 0x1a
    if-lt v2, v3, :old
    new-instance v2, Landroid/app/NotificationChannel;
    const-string v3, "liga"
    const-string v4, "Liga online"
    const/4 v5, 0x4
    invoke-direct {v2, v3, v4, v5}, Landroid/app/NotificationChannel;-><init>(Ljava/lang/String;Ljava/lang/CharSequence;I)V
    invoke-virtual {v1, v2}, Landroid/app/NotificationManager;->createNotificationChannel(Landroid/app/NotificationChannel;)V
    new-instance v2, Landroid/app/Notification$Builder;
    invoke-direct {v2, v0, v3}, Landroid/app/Notification$Builder;-><init>(Landroid/content/Context;Ljava/lang/String;)V
    goto :build
    :old
    new-instance v2, Landroid/app/Notification$Builder;
    invoke-direct {v2, v0}, Landroid/app/Notification$Builder;-><init>(Landroid/content/Context;)V
    const/4 v3, 0x1
    invoke-virtual {v2, v3}, Landroid/app/Notification$Builder;->setPriority(I)Landroid/app/Notification$Builder;
    const/4 v3, -0x1
    invoke-virtual {v2, v3}, Landroid/app/Notification$Builder;->setDefaults(I)Landroid/app/Notification$Builder;
    :build
    invoke-virtual {v0}, Landroid/app/Activity;->getApplicationInfo()Landroid/content/pm/ApplicationInfo;
    move-result-object v3
    iget v3, v3, Landroid/content/pm/ApplicationInfo;->icon:I
    invoke-virtual {v2, v3}, Landroid/app/Notification$Builder;->setSmallIcon(I)Landroid/app/Notification$Builder;
    invoke-virtual {v2, p1}, Landroid/app/Notification$Builder;->setContentTitle(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;
    invoke-virtual {v2, p2}, Landroid/app/Notification$Builder;->setContentText(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;
    const/4 v3, 0x1
    invoke-virtual {v2, v3}, Landroid/app/Notification$Builder;->setAutoCancel(Z)Landroid/app/Notification$Builder;
    new-instance v3, Landroid/content/Intent;
    const-class v4, Lcom/papascochero/game/MainActivity;
    invoke-direct {v3, v0, v4}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
    const/high16 v4, 0x20000000
    invoke-virtual {v3, v4}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
    const/4 v4, 0x0
    const/high16 v5, 0xc000000
    invoke-static {v0, v4, v3, v5}, Landroid/app/PendingIntent;->getActivity(Landroid/content/Context;ILandroid/content/Intent;I)Landroid/app/PendingIntent;
    move-result-object v3
    invoke-virtual {v2, v3}, Landroid/app/Notification$Builder;->setContentIntent(Landroid/app/PendingIntent;)Landroid/app/Notification$Builder;
    invoke-virtual {v2}, Landroid/app/Notification$Builder;->build()Landroid/app/Notification;
    move-result-object v2
    const/16 v3, 0x2a
    invoke-virtual {v1, v3, v2}, Landroid/app/NotificationManager;->notify(ILandroid/app/Notification;)V
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch
    return-void
    :catch
    move-exception v0
    return-void
.end method
