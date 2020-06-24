using System;
using UnityEngine;

public class FadeGroup : MonoBehaviour
{
    public bool alwaysFindFades = true;
    public bool onStartFindFades = true;
    [SerializeField]
    private Fade[] m_fades = new Fade[0];
    public bool hasIn { get { return m_fades.Any(a => a.isIn); } }
    public bool hasOut { get { return m_fades.Any(a => !a.isIn); } }

    private bool m_isStartFadesCollected = false;
    private bool needCollect { get { return alwaysFindFades || onStartFindFades && !m_isStartFadesCollected; } }

    void Awake()
    {
        RegisterEvent();
    }

    void OnDestroy()
    {
        UnRegisterEvent();
    }

    void Start()
    {
        if (!alwaysFindFades && onStartFindFades && !m_isStartFadesCollected)
            CollectFades();
    }

    private void CollectFades()
    {
        m_isStartFadesCollected = true;
        UnRegisterEvent();
        m_fades = GetComponentsInChildren<Fade>(true);
        RegisterEvent();
    }

    private void RegisterEvent()
    {
        foreach (var fade in m_fades)
        {
            fade.onFadeInComplete += OnFadeInComplete;
            fade.onFadeOutComplete += OnFadeOutComplete;
        }
    }

    private void UnRegisterEvent()
    {
        foreach (var fade in m_fades)
        {
            fade.onFadeInComplete -= OnFadeInComplete;
            fade.onFadeOutComplete -= OnFadeOutComplete;
        }
    }

    private void OnFadeInComplete()
    {
        m_fadeInCompleteCount++;
        if (m_fadeInCompleteCallback != null
            && m_fadeInCompleteCount >= m_fades.Count(a => a.enableFadeIn))
        {
            m_fadeInCompleteCallback.Invoke();
            m_fadeInCompleteCallback = null;
        }
    }

    private void OnFadeOutComplete()
    {
        m_fadeOutCompleteCount++;
        if (m_fadeOutCompleteCallback != null
            && m_fadeOutCompleteCount >= m_fades.Count(a => a.enableFadeOut))
        {
            m_fadeOutCompleteCallback.Invoke();
            m_fadeOutCompleteCallback = null;
        }
    }

    private int m_fadeInCompleteCount = 0;
    private Action m_fadeInCompleteCallback = null;
    public virtual void FadeIn(Action onComplete = null)
    {
        m_fadeInCompleteCount = 0;
        m_fadeInCompleteCallback = onComplete;
        if (!gameObject.activeSelf)
            gameObject.SetActive(true);
        if (needCollect)
            CollectFades();
        foreach (var fade in m_fades)
        {
            fade.FadeIn();
        }
    }

    private int m_fadeOutCompleteCount = 0;
    private Action m_fadeOutCompleteCallback = null;
    public virtual void FadeOut(Action onComplete = null)
    {
        m_fadeOutCompleteCount = 0;
        m_fadeOutCompleteCallback = onComplete;
        if (!gameObject.activeSelf)
            gameObject.SetActive(true);
        if (needCollect)
            CollectFades();
        foreach (var fade in m_fades)
        {
            fade.FadeOut();
        }
    }

    public virtual void FadeInImmediately()
    {
        m_fadeInCompleteCallback = null;
        if (!gameObject.activeSelf)
            gameObject.SetActive(true);
        if (needCollect)
            CollectFades();
        foreach (var fade in m_fades)
        {
            fade.FadeInImmediately();
        }
    }

    public virtual void FadeOutImmediately()
    {
        m_fadeOutCompleteCallback = null;
        if (!gameObject.activeSelf)
            gameObject.SetActive(true);
        if (needCollect)
            CollectFades();
        foreach (var fade in m_fades)
        {
            fade.FadeOutImmediately();
        }
    }

    public void HideImmidiately()
    {
        gameObject.SetActive(false);
    }
}
