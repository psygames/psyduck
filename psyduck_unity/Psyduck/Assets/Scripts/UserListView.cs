using Psyduck;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UserListView : ViewBase
{
    public ContentGroup group;

    CommonAction action = new CommonAction();

    void OnEnable()
    {
        Refresh();
    }

    private void Refresh()
    {
        action.UserList(DeviceID.UUID, OnUserList);
    }

    private void OnUserList(UserListResult res)
    {
        if (res.isOK)
        {
            group.SetData<UserItem, UserInfo>(res.userInfos);
        }
        else
        {
            Debug.LogError(res.errorMsg);
        }
    }

    public void OnClickRefresh()
    {
        Refresh();
    }

    public void OnClickClose()
    {
        Close();
        UIManager.Open<MainView>();
    }
}
