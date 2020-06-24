using Psyduck;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Experimental.UIElements;
using UnityEngine.UI;

public class UserItem : MonoBehaviour
{
    public RawImage head;
    public Text nickname;
    public Text detail;

    public void SetData(UserInfo info)
    {
        head.LoadFromUrl(info.csdnDetail.head);
        nickname.text = info.csdnDetail.nickname;
        detail.text = $"point: {info.csdnDetail.point}, coin: {info.csdnDetail.coin}, vip: {info.csdnDetail.vip.isVip}";
    }
}
