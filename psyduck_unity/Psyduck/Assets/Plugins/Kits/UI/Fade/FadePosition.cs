using UnityEngine;
using DG.Tweening;

[RequireComponent(typeof(RectTransform))]
public class FadePosition : Fade, IFade
{
    public Vector2 from = Vector2.zero;
    public Vector2 to = Vector2.zero;

    protected override void DoFadeIn()
    {
        base.DoFadeIn();
        rectTransform.DOKill();
        rectTransform.DOAnchorPos(to, fadeInDuration)
            .SetDelay(fadeInDelay).SetEase(fadeInMethod).OnComplete(OnFadeInFinished);
    }

    protected override void DoFadeOut()
    {
        base.DoFadeOut();
        rectTransform.DOKill();
        rectTransform.DOAnchorPos(from, fadeOutDuration)
            .SetDelay(fadeOutDelay).SetEase(fadeOutMethod).OnComplete(OnFadeOutFinished);
    }

    protected override void DoFadeInReset()
    {
        base.DoFadeInReset();
        rectTransform.anchoredPosition = from;
    }

    protected override void DoFadeOutReset()
    {
        base.DoFadeOutReset();
        rectTransform.anchoredPosition = to;
    }
}
