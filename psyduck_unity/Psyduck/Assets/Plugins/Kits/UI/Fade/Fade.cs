using System;
using UnityEngine;
using DG.Tweening;

public class Fade : MonoBehaviour, IFade
{
    public bool enableFadeIn = true;
    public bool onEnableFadeIn = false;
    public bool fadeInReset = true;
    public float fadeInDelay = 0f;
    public float fadeInDuration = 0.15f;
    public Ease fadeInMethod = Ease.InSine;
    public event Action onFadeInComplete;

    public bool enableFadeOut = true;
    public bool outSetInactive = true;
    public bool fadeOutReset = false;
    public float fadeOutDelay = 0f;
    public float fadeOutDuration = 0.15f;
    public Ease fadeOutMethod = Ease.OutSine;
    public event Action onFadeOutComplete;

    public bool autoFadeOut = false;
    public bool isIn { get; protected set; }

    private RectTransform m_rectTransform;
    public RectTransform rectTransform
    {
        get
        {
            if (m_rectTransform == null)
                m_rectTransform = GetComponent<RectTransform>();
            return m_rectTransform;
        }
    }

    protected virtual void OnEnable()
    {
        if (enableFadeIn && onEnableFadeIn)
            FadeIn();
    }

    protected virtual void DoFadeInReset()
    {

    }

    protected virtual void DoFadeIn()
    {

    }

    protected virtual void DoFadeOutReset()
    {

    }

    protected virtual void DoFadeOut()
    {

    }

    public void FadeIn()
    {
        if (!enableFadeIn)
            return;
        isIn = true;
        if (!gameObject.activeSelf)
            gameObject.SetActive(true);
        if (fadeInReset)
            DoFadeInReset();
        DoFadeIn();
    }

    public void FadeOut()
    {
        if (!enableFadeOut)
            return;
        isIn = false;
        if (!gameObject.activeSelf)
            gameObject.SetActive(true);
        if (fadeOutReset)
            DoFadeOutReset();
        DoFadeOut();
    }

    public void FadeInImmediately()
    {
        if (!enableFadeIn)
            return;
        isIn = true;
        DoFadeOutReset();
        OnFadeInFinished();
    }

    public void FadeOutImmediately()
    {
        if (!enableFadeOut)
            return;
        isIn = false;
        if (outSetInactive && gameObject.activeSelf)
            gameObject.SetActive(false);
        DoFadeInReset();
        OnFadeOutFinished();
    }

    protected virtual void OnFadeInFinished()
    {
        if (autoFadeOut && isIn && gameObject.activeInHierarchy)
            FadeOut();
        if (onFadeInComplete != null)
            onFadeInComplete.Invoke();
    }

    protected virtual void OnFadeOutFinished()
    {
        if (outSetInactive && gameObject.activeSelf)
            gameObject.SetActive(false);
        if (onFadeOutComplete != null)
            onFadeOutComplete.Invoke();
    }
}
