using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Psyduck;
using UnityEngine.UI;
using UnityEngine.Networking;

public class LoginView : ViewBase
{
    enum State
    {
        Login = 0,
        Begin = 1,
        Scan = 2,
        VerifyGet = 3,
        VerifySet = 4,
        WaitForDown = 5,
        Done = 6,
        Fail = 7,
    }

    public RadioObjects radio;
    public RawImage qr;
    public InputField phone;
    public InputField code;
    public Text getHint;
    public Text setHint;
    public Text failText;
    public GameObject busy;

    private State state;
    private LoginAction action = new LoginAction();
    private string uid => DeviceID.UUID;

    private void Awake()
    {
        action.onBegin += Action_onBegin;
        action.onError += Action_onError;
        action.onFinish += Action_onFinish;
        action.onProcess += Action_onProcess;
    }

    private State lastState = State.Login;
    private void Action_onProcess(LoginStateResult obj)
    {
        if (obj.isRequest || obj.isProcess)
        {
            state = State.Begin;
        }
        else if (obj.isScan)
        {
            state = State.Scan;
            qr.LoadFromUrl(obj.qrUrl);
        }
        else if (obj.isVerifyGet || obj.isVerifyGetHint)
        {
            state = State.VerifyGet;
            if (obj.isVerifyGetHint)
                getHint.text = obj.message;
        }
        else if (obj.isVerifySet || obj.isVerifySetHint)
        {
            state = State.VerifySet;
            if (obj.isVerifySetHint)
                setHint.text = obj.message;
        }
        else if (obj.isWaitForDone)
        {
            state = State.WaitForDown;
        }
        else if (obj.isFail)
        {
            state = State.Fail;
            failText.text = obj.message;
        }
        else if (obj.isDone)
        {
            state = State.Done;
        }

        if (lastState != state)
            HideBusy();

        lastState = state;
    }

    private void Action_onFinish(LoginResult obj)
    {
        Debug.Log("登陆完成");
    }

    private void Action_onError(Result obj)
    {
        Debug.LogError("发生错误: " + obj.errorMsg);
    }

    private void Action_onBegin(TokenResult obj)
    {
        Debug.Log("开始登陆");
    }

    private void OnEnable()
    {
        if (action.isBusy)
        {
            ShowBusy();
        }
        else
        {
            HideBusy();
            state = State.Login;
        }
        Update();
    }

    public void OnClickStart()
    {
        action.Login(uid);
        ShowBusy();
    }

    public void OnClickVerifyGet()
    {
        action.VerifyGet(phone.text);
        ShowBusy();
    }

    public void OnClickVerifySet()
    {
        action.VerifySet(code.text);
        ShowBusy();
    }

    public void OnClickClose()
    {
        Close();
        UIManager.Open<MainView>();
    }

    private void Update()
    {
        radio.Radio((int)state);

        busyTime -= Time.deltaTime;
        busy.SetActive(busyTime > 0);
    }

    float busyTime = 0;
    private void ShowBusy()
    {
        busyTime = 2;
    }

    private void HideBusy()
    {
        busyTime = 0;
    }
}
