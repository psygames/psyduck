using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BusyView : ViewBase
{
    public static float timeout = 0;

    private void Update()
    {
        timeout = Mathf.Max(0, timeout - Time.deltaTime);
        if (timeout <= 0)
        {
            Close();
        }
    }
}

public static class Busy
{
    public static void Show(float timeout = 10)
    {
        BusyView.timeout = timeout;
        UIManager.Open<BusyView>(UILayer.Top);
    }

    public static void Hide()
    { 
        UIManager.Close<BusyView>();
    }
}