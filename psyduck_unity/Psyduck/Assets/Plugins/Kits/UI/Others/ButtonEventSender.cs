using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(Button))]
public class ButtonEventSender : MonoBehaviour
{
    public string prefix = "OnClick";
    public string eventName = "";

    private bool isRegister = false;
    private ButtonEventReceiver receiver = null;
    private void OnEnable()
    {
        if (isRegister)
            return;
        receiver = GetComponentInParent<ButtonEventReceiver>();
        GetComponent<Button>().onClick.AddListener(OnClick);
    }

    private void OnDisable()
    {
        if (!isRegister)
            return;
        GetComponent<Button>().onClick.RemoveListener(OnClick);
    }

    private void OnClick()
    {
        if (receiver == null)
            return;
        receiver.NotifyEvent(prefix, eventName);
    }
}
