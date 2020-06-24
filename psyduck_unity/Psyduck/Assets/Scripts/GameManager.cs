using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        UIManager.Instance.loadViewFunc = (name) =>
        {
            return Resources.Load<ViewBase>(name);
        };

        UIManager.Open<MainView>();
    }
}
