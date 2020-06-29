using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NavView : ViewBase
{
    public void OnClickLogin()
    {
        UIManager.Open<LoginView>();
    }

    public void OnClickUserList()
    {
        UIManager.Open<UserListView>();
    }

    public void OnClickDownload()
    {
        UIManager.Open<DownloadView>();
    }
}
