using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    void Start()
    {
        UIManager.Instance.loadViewFunc = (_view) =>
        {
            return Resources.Load<ViewBase>("Prefabs/Views/" + _view);
        };

        UIManager.Open<SignInView>();
    }
}
