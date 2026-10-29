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

.method public voices()Ljava/lang/String;
    .registers 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_start
    new-instance v0, Ljava/lang/StringBuilder;
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V
    iget-object v1, p0, Lcom/papascochero/game/Tts;->tts:Landroid/speech/tts/TextToSpeech;
    invoke-virtual {v1}, Landroid/speech/tts/TextToSpeech;->getVoices()Ljava/util/Set;
    move-result-object v1
    if-eqz v1, :done
    invoke-interface {v1}, Ljava/util/Set;->iterator()Ljava/util/Iterator;
    move-result-object v1
    :loop
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z
    move-result v2
    if-eqz v2, :done
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;
    move-result-object v2
    check-cast v2, Landroid/speech/tts/Voice;
    invoke-virtual {v2}, Landroid/speech/tts/Voice;->getLocale()Ljava/util/Locale;
    move-result-object v3
    invoke-virtual {v3}, Ljava/util/Locale;->getLanguage()Ljava/lang/String;
    move-result-object v3
    const-string v4, "es"
    invoke-virtual {v4, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v3
    if-eqz v3, :loop
    invoke-virtual {v2}, Landroid/speech/tts/Voice;->getName()Ljava/lang/String;
    move-result-object v3
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v3, "|"
    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    goto :loop
    :done
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v0
    return-object v0
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch
    :catch
    const-string v0, ""
    return-object v0
.end method

.method public voice(Ljava/lang/String;)V
    .registers 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_start
    iget-object v0, p0, Lcom/papascochero/game/Tts;->tts:Landroid/speech/tts/TextToSpeech;
    invoke-virtual {v0}, Landroid/speech/tts/TextToSpeech;->getVoices()Ljava/util/Set;
    move-result-object v1
    if-eqz v1, :end
    invoke-interface {v1}, Ljava/util/Set;->iterator()Ljava/util/Iterator;
    move-result-object v1
    :loop
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z
    move-result v2
    if-eqz v2, :end
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;
    move-result-object v2
    check-cast v2, Landroid/speech/tts/Voice;
    invoke-virtual {v2}, Landroid/speech/tts/Voice;->getName()Ljava/lang/String;
    move-result-object v3
    invoke-virtual {v3, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v3
    if-eqz v3, :loop
    invoke-virtual {v0, v2}, Landroid/speech/tts/TextToSpeech;->setVoice(Landroid/speech/tts/Voice;)I
    :end
    return-void
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch
    :catch
    return-void
.end method
