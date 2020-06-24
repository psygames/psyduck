using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System;

public static class UnityExtension
{
    public static T GetOrAddComponent<T>(this GameObject gameObject) where T : Component
    {
        var component = gameObject.GetComponent<T>();
        if (component == null)
            component = gameObject.AddComponent<T>();
        return component;
    }

    public static Coroutine DelayDo(this MonoBehaviour mono, float delay, Action callback)
    {
        return mono.StartCoroutine(DelayDoCoro(delay, callback));
    }

    private static IEnumerator DelayDoCoro(float delay, Action callback)
    {
        yield return new WaitForSeconds(delay);
        callback?.Invoke();
    }

    public static void LoadFromUrl(this RawImage rawImage, string url)
    {
        if (rawImage.texture != null && rawImage.texture.name == url)
            return;
        var rect = rawImage.rectTransform.rect;
        Texture2D texture = new Texture2D((int)rect.width, (int)rect.height);
        rawImage.texture = texture;
        rawImage.texture.name = url;
        UIManager.Instance.StartCoroutine(_LoadQr(rawImage, url));
    }


    static IEnumerator _LoadQr(RawImage rawImage, string url)
    {
        using (var req = UnityEngine.Networking.UnityWebRequest.Get(url))
        {
            yield return req.SendWebRequest();
            if (req.isHttpError || req.isNetworkError)
            {
                Debug.LogError(req.error);
            }
            else
            {
                byte[] results = req.downloadHandler.data;
                Texture2D texture = (Texture2D)rawImage.texture;
                texture.LoadImage(results);
            }
        }
    }
}
