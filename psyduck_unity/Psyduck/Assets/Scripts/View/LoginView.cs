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
        Prepare = 0,
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
    public Text verifyHint;
    public RadioObjects radioVerifyGet;
    public Text failText;

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

    private void OnEnable()
    {
        verifyHintText = "";
        verifyHint.text = "";
        RecoverAction();
        Update();
    }

    private void RecoverAction()
    {
        if (action.isBusy)
        {
            return;
        }

        state = State.Prepare;
        ShowBusy();
        CommonAction ac = new CommonAction();
        ac.RecoverAction(uid, (res) =>
        {
            HideBusy();
            if (res.isOK)
            {
                var _act = res.actionInfos.First(a => a.action == "login");
                if (_act != null)
                {
                    ShowBusy();
                    action.Recover(uid, _act);
                }
            }
        });
    }

    private string verifyHintText = "";
    private State lastState = State.Prepare;
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
            if (obj.isVerifyGetHint && verifyHintText != obj.message)
            {
                verifyHintText = obj.message;
                verifyHint.text = verifyHintText;
                HideBusy();
            }
        }
        else if (obj.isVerifySet || obj.isVerifySetHint)
        {
            state = State.VerifySet;
            if (obj.isVerifySetHint && verifyHintText != obj.message)
            {
                verifyHintText = obj.message;
                verifyHint.text = verifyHintText;
                HideBusy();
            }
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
        {
            verifyHintText = "";
            HideBusy();
        }

        lastState = state;
    }

    private void Action_onFinish(LoginResult obj)
    {
        //Debug.Log("登陆完成");
        Close();
        Toast.Show("登陆完成");
    }

    private void Action_onError(Result obj)
    {
        HideBusy();
        //Debug.LogError("发生错误: " + obj.errorMsg);
        Toast.Error("错误:" + obj.errorMsg);
    }

    private void Action_onBegin(TokenResult obj)
    {
        //Debug.Log("开始登陆");
    }

    public void OnClickStart()
    {
        action.Login(uid);
        ShowBusy();
    }

    public void OnClickVerifyGet()
    {
        if (state != State.VerifyGet)
            return;
        verifyHint.text = "";
        action.VerifyGet(phone.text);
        ShowBusy(10);
    }

    public void OnClickVerifySet()
    {
        if (state != State.VerifySet)
            return;
        verifyHint.text = "";
        action.VerifySet(code.text);
        ShowBusy(10);
    }

    public void OnClickClose()
    {
        Close();
    }

    private void Update()
    {
        radioVerifyGet.Radio(state == State.VerifySet);
        radio.Radio((int)state);
    }

    private void ShowBusy(int timeout = 10)
    {
        if (isActiveAndEnabled)
            Busy.Show(timeout);
    }

    private void HideBusy()
    {
        if (isActiveAndEnabled)
            Busy.Hide();
    }
}
