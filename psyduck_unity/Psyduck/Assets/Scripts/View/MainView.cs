using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainView : ViewBase
{
    public void OnClickLogin()
    {
        Close();
        UIManager.Open<LoginView>();
    }

    public void OnClickUserList()
    {
        Close();
        UIManager.Open<UserListView>();
    }

    public void OnClickDownload()
    { 
    
    }
}
