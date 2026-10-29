.class public Lcom/papascochero/game/Chrome;
.super Landroid/webkit/WebChromeClient;

.field private act:Lcom/papascochero/game/MainActivity;

.method public constructor <init>(Lcom/papascochero/game/MainActivity;)V
    .registers 2
    invoke-direct {p0}, Landroid/webkit/WebChromeClient;-><init>()V
    iput-object p1, p0, Lcom/papascochero/game/Chrome;->act:Lcom/papascochero/game/MainActivity;
    return-void
.end method

.method public onShowFileChooser(Landroid/webkit/WebView;Landroid/webkit/ValueCallback;Landroid/webkit/WebChromeClient$FileChooserParams;)Z
    .registers 7
    iget-object v0, p0, Lcom/papascochero/game/Chrome;->act:Lcom/papascochero/game/MainActivity;
    iget-object v1, v0, Lcom/papascochero/game/MainActivity;->cb:Landroid/webkit/ValueCallback;
    if-eqz v1, :skip
    const/4 v2, 0x0
    invoke-interface {v1, v2}, Landroid/webkit/ValueCallback;->onReceiveValue(Ljava/lang/Object;)V
    :skip
    iput-object p2, v0, Lcom/papascochero/game/MainActivity;->cb:Landroid/webkit/ValueCallback;
    invoke-virtual {p3}, Landroid/webkit/WebChromeClient$FileChooserParams;->createIntent()Landroid/content/Intent;
    move-result-object v1
    const/16 v2, 0x2a
    :try_start
    invoke-virtual {v0, v1, v2}, Lcom/papascochero/game/MainActivity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch
    const/4 v1, 0x1
    return v1
    :catch
    move-exception v1
    const/4 v2, 0x0
    iput-object v2, v0, Lcom/papascochero/game/MainActivity;->cb:Landroid/webkit/ValueCallback;
    invoke-interface {p2, v2}, Landroid/webkit/ValueCallback;->onReceiveValue(Ljava/lang/Object;)V
    const/4 v1, 0x0
    return v1
.end method
