using UnityEngine;
using System;

public enum UILayer
{
    Common = 0,
    Top = 1,
    Bottom = 2,
}

public abstract class ViewBase : ButtonEventReceiver
{
    protected RectTransform mRectTransform;
    public RectTransform rectTransform
    {
        get
        {
            if (mRectTransform == null)
                mRectTransform = GetComponent<RectTransform>();
            return mRectTransform;
        }
    }
    protected virtual void OnOpen() { }
    protected virtual void OnClose() { }
    protected void Close()
    {
        UIManager.Close(GetType());
    }
}
