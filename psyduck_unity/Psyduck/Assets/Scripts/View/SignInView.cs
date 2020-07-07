using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Psyduck;
using UnityEngine.UI;
using UnityEngine.Networking;

public class SignInView : ViewBase
{
    public InputField qqText;
    public Text errorText;

    protected override void OnOpen()
    {
        base.OnOpen();
        errorText.text = "";
        if (PlayerPrefs.HasKey("QQ"))
        {
            Sign(PlayerPrefs.GetString("QQ"));
        }
    }

    private void Sign(string qq)
    {
        if (string.IsNullOrEmpty(qq))
        {
            Toast.Show("QQ号不能为空！");
            errorText.text = "QQ号不能为空！";
            return;
        }

        Busy.Show();

        QQKit.GetInfo(qq, (res) =>
        {
            Busy.Hide();

            if (!res.success)
            {
                Toast.Show(res.message);
                errorText.text = res.message;
            }
            else
            {
                PlayerPrefs.SetString("QQ", qq);
                Toast.Show($"恭喜 {res.message} 登录成功！");
                Close();
                UIManager.Open<NavView>();
                UIManager.Open<MainView>();
            }
        });
    }

    private void OnClickSignIn()
    {
        errorText.text = "";
        Sign(qqText.text);
    }

    private void OnClickClose()
    {

    }
}
