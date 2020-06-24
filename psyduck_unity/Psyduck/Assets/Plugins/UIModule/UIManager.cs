using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using ReflectionEx;

public class UIManager : Singleton<UIManager>
{
    public RectTransform bottomLayer;
    public RectTransform commonLayer;
    public RectTransform topLayer;

    public Func<string, ViewBase> loadViewFunc { get; set; }

    private readonly List<ViewBase> mCachedViews = new List<ViewBase>();

    private ViewBase getView(Type type)
    {
        foreach (var p in mCachedViews)
        {
            if (p.GetType() == type)
            {
                return p;
            }
        }
        return null;
    }

    private void setLayer(ViewBase view, UILayer layer)
    {
        if (view == null)
            return;

        if (layer == UILayer.Common && commonLayer != null)
        {
            view.transform.SetParent(commonLayer, false);
        }
        else if (layer == UILayer.Top && topLayer != null)
        {
            view.transform.SetParent(topLayer, false);
        }
        else if (layer == UILayer.Bottom && bottomLayer != null)
        {
            view.transform.SetParent(bottomLayer, false);
        }

        var parent = view.transform.parent;
        if (parent != null)
        {
            view.rectTransform.SetSiblingIndex(parent.childCount);
        }
    }

    private ViewBase load(Type viewType)
    {
        if (!typeof(ViewBase).IsAssignableFrom(viewType))
        {
            Debug.LogError($"{viewType.Name} is not a UIView");
            return null;
        }

        var view = getView(viewType);
        if (view != null)
        {
            return view;
        }

        if (loadViewFunc == null)
        {
            Debug.LogError("UIManager Must set loadViewFunc");
            return null;
        }

        view = loadViewFunc?.Invoke(viewType.Name);
        view = Instantiate(view);
        view.gameObject.SetActive(false);
        mCachedViews.Add(view);
        return view;
    }

    private T load<T>() where T : ViewBase
    {
        return load(typeof(T)) as T;
    }

    private T open<T>(UILayer layer = UILayer.Common) where T : ViewBase
    {
        ViewBase view = getView(typeof(T));

        if (view == null)
        {
            view = Load<T>();
        }

        setLayer(view, layer);
        if (!view.gameObject.activeSelf)
        {
            view.gameObject.SetActive(true);
        }
        view.ReflectInvokeMethod("OnOpen");
        return view as T;
    }

    private void close<T>() where T : ViewBase
    {
        ViewBase view = getView(typeof(T));
        view.gameObject.SetActive(false);
        view.ReflectInvokeMethod("OnClose");
    }

    private void close(Type type)
    {
        if (!typeof(ViewBase).IsAssignableFrom(type))
        {
            Debug.LogError($"{type.Name} is not a UIView based Type");
            return;
        }
        ViewBase view = getView(type);
        view.gameObject.SetActive(false);
        view.ReflectInvokeMethod("OnClose");
    }


    #region API
    public static T Load<T>() where T : ViewBase
    {
        return Instance.load<T>();
    }

    public static T Open<T>(UILayer layer = UILayer.Common) where T : ViewBase
    {
        return Instance.open<T>(layer);
    }

    public static void Close<T>() where T : ViewBase
    {
        Instance.close<T>();
    }

    public static void Close(Type type)
    {
        Instance.close(type);
    }
    #endregion
}
