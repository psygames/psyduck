using System.Collections;
using System.Collections.Generic;
using UnityEngine;
/*
 * Prefab 中遵循： obj[0] 为不可用状态， obj[1] 为可用状态， 其余为扩展状态。
 * 只有可用和不可用状态时，尽量使用 Radio(bool isOn) 方法
 */
public class RadioObjects : RadioBase
{
    [SerializeField]
    private GameObject[] gameObjects = new GameObject[2];

    private void Awake()
    {
        SetRadios();
    }

    public override void Radio(int index)
    {
        base.Radio(index);
        if (gameObjects == null)
            return;

        for (int i = 0; i < gameObjects.Length; i++)
        {
            if (!gameObjects[i])
                continue;
            if (i != index && gameObjects[i].activeSelf && (gameObjects?[index] != gameObjects[i]))
                gameObjects[i].SetActive(false);
            else if (i == index && !gameObjects[i].activeSelf)
                gameObjects[i].SetActive(true);
        }
    }

    private void SetRadios()
    {
        Radio(radioIndex);
    }
}
