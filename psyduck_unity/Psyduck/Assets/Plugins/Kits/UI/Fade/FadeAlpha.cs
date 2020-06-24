using UnityEngine;
using DG.Tweening;

[RequireComponent(typeof(RectTransform))]
[RequireComponent(typeof(CanvasGroup))]
public class FadeAlpha : Fade, IFade
{
    [Range(0, 1)]
    public float from = 0;
    [Range(0, 1)]
    public float to = 1;

    private CanvasGroup m_canvasGroup;
    private CanvasGroup canvasGroup
    {
        get
        {
            if (m_canvasGroup == null)
                m_canvasGroup = GetComponent<CanvasGroup>();
            if (m_canvasGroup == null)
                m_canvasGroup = gameObject.AddComponent<CanvasGroup>();
            return m_canvasGroup;
        }
    }

    protected override void DoFadeIn()
    {
        base.DoFadeIn();
        canvasGroup.DOKill();
        canvasGroup.DOFade(to, fadeInDuration)
            .SetDelay(fadeInDelay).SetEase(fadeInMethod).OnComplete(OnFadeInFinished);
    }

    protected override void DoFadeInReset()
    {
        base.DoFadeInReset();
        canvasGroup.alpha = from;
    }

    protected override void DoFadeOutReset()
    {
        base.DoFadeOutReset();
        canvasGroup.alpha = to;
    }

    protected override void DoFadeOut()
    {
        base.DoFadeOut();
        canvasGroup.DOKill();
        canvasGroup.DOFade(from, fadeOutDuration)
            .SetDelay(fadeOutDelay).SetEase(fadeOutMethod).OnComplete(OnFadeOutFinished);
    }
}
