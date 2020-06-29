using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using ReflectionEx;

public class ButtonEventReceiver : MonoBehaviour
{
    public void NotifyEvent(string prefix, string eventName)
    {
        this.ReflectInvokeMethod(prefix + eventName);
    }
}
