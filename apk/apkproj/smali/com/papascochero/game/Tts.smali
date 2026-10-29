.class public Lcom/papascochero/game/Tts;
.super Ljava/lang/Object;
.implements Landroid/speech/tts/TextToSpeech$OnInitListener;

.field public tts:Landroid/speech/tts/TextToSpeech;
.field public ok:Z

.method public constructor <init>(Landroid/content/Context;)V
    .registers 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    new-instance v0, Landroid/speech/tts/TextToSpeech;
    invoke-direct {v0, p1, p0}, Landroid/speech/tts/TextToSpeech;-><init>(Landroid/content/Context;Landroid/speech/tts/TextToSpeech$OnInitListener;)V
    iput-object v0, p0, Lcom/papascochero/game/Tts;->tts:Landroid/speech/tts/TextToSpeech;
    return-void
.end method

.method public onInit(I)V
    .registers 6
    if-nez p1, :fail
    iget-object v0, p0, Lcom/papascochero/game/Tts;->tts:Landroid/speech/tts/TextToSpeech;
    new-instance v1, Ljava/util/Locale;
    const-string v2, "es"
    const-string v3, "ES"
    invoke-direct {v1, v2, v3}, Ljava/util/Locale;-><init>(Ljava/lang/String;Ljava/lang/String;)V
    invoke-virtual {v0, v1}, Landroid/speech/tts/TextToSpeech;->setLanguage(Ljava/util/Locale;)I
    const v1, 0x3f90a3d7
    invoke-virtual {v0, v1}, Landroid/speech/tts/TextToSpeech;->setSpeechRate(F)I
    const/4 v1, 0x1
    iput-boolean v1, p0, Lcom/papascochero/game/Tts;->ok:Z
    :fail
    return-void
.end method

.method public speak(Ljava/lang/String;)V
    .registers 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-boolean v0, p0, Lcom/papascochero/game/Tts;->ok:Z
    if-eqz v0, :end
    iget-object v0, p0, Lcom/papascochero/game/Tts;->tts:Landroid/speech/tts/TextToSpeech;
    const/4 v1, 0x1
    const/4 v2, 0x0
    const-string v3, "pc"
    invoke-virtual {v0, p1, v1, v2, v3}, Landroid/speech/tts/TextToSpeech;->speak(Ljava/lang/CharSequence;ILandroid/os/Bundle;Ljava/lang/String;)I
    :end
    return-void
.end method

.method public flush(Ljava/lang/String;)V
    .registers 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-boolean v0, p0, Lcom/papascochero/game/Tts;->ok:Z
    if-eqz v0, :end
    iget-object v0, p0, Lcom/papascochero/game/Tts;->tts:Landroid/speech/tts/TextToSpeech;
    const/4 v1, 0x0
    const/4 v2, 0x0
    const-string v3, "pc"
    invoke-virtual {v0, p1, v1, v2, v3}, Landroid/speech/tts/TextToSpeech;->speak(Ljava/lang/CharSequence;ILandroid/os/Bundle;Ljava/lang/String;)I
    :end
    return-void
.end method

.method public pitch(F)V
    .registers 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-object v0, p0, Lcom/papascochero/game/Tts;->tts:Landroid/speech/tts/TextToSpeech;
    invoke-virtual {v0, p1}, Landroid/speech/tts/TextToSpeech;->setPitch(F)I
    return-void
.end method
