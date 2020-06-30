using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ToastView : ViewBase
{
    public static string text = "";
    public FadeGroup fade;
    public Text toastText;

    float timeout = 2;
    protected override void OnOpen()
    {
        base.OnOpen();
        timeout = 2;
        toastText.text = text;
        fade.FadeIn();
    }

    private void Update()
    {
        timeout = Mathf.Max(0, timeout - Time.deltaTime);
        if (timeout <= 0)
        {
            Close();
        }
    }
}

public static class Toast
{
    public static void Show(string text)
    {
        ToastView.text = text;
        UIManager.Open<ToastView>(UILayer.Top);
    }

    public static void Error(string text)
    {
        Show($"<color=#aa2222>{text}</color>");
    }

    public static void Hide()
    {
        UIManager.Close<ToastView>();
    }
}