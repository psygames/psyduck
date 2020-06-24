using UnityEngine;
using DG.Tweening;

[RequireComponent(typeof(RectTransform))]
[RequireComponent(typeof(UnityEngine.UI.Graphic))]
public class FadeColor : Fade, IFade
{
    public Color from = Color.white;
    public Color to = Color.white;

    private UnityEngine.UI.Graphic m_graphic = null;

    private UnityEngine.UI.Graphic graphic
    {
        get
        {
            if (m_graphic == null)
                m_graphic = GetComponent<UnityEngine.UI.Graphic>();
            return m_graphic;
        }
    }

    protected override void DoFadeIn()
    {
        base.DoFadeIn();
        graphic.DOKill();
        graphic.DOColor(to, fadeInDuration).SetDelay(fadeInDelay)
            .SetEase(fadeInMethod).OnComplete(OnFadeInFinished);
    }

    protected override void DoFadeOut()
    {
        base.DoFadeOut();
        graphic.DOKill();
        graphic.DOColor(from, fadeOutDuration).SetDelay(fadeOutDelay)
            .SetEase(fadeOutMethod).OnComplete(OnFadeOutFinished);
    }

    protected override void DoFadeOutReset()
    {
        base.DoFadeOutReset();
        graphic.color = to;
    }

    protected override void DoFadeInReset()
    {
        base.DoFadeInReset();
        graphic.color = from;
    }
}
