using UnityEngine;
using DG.Tweening;

[RequireComponent(typeof(RectTransform))]
public class FadeScale : Fade, IFade
{
    public Vector3 from = Vector3.zero;
    public Vector3 to = Vector3.one;

    protected override void DoFadeIn()
    {
        base.DoFadeIn();
        rectTransform.DOKill();
        rectTransform.DOScale(to, fadeInDuration)
            .SetDelay(fadeInDelay).SetEase(fadeInMethod).OnComplete(OnFadeInFinished);
    }

    protected override void DoFadeOut()
    {
        base.DoFadeOut();
        rectTransform.DOKill();
        rectTransform.DOScale(from, fadeOutDuration)
            .SetDelay(fadeOutDelay).SetEase(fadeOutMethod).OnComplete(OnFadeOutFinished);
    }

    protected override void DoFadeInReset()
    {
        base.DoFadeInReset();
        rectTransform.localScale = from;
    }

    protected override void DoFadeOutReset()
    {
        base.DoFadeOutReset();
        rectTransform.localScale = to;
    }
}
