using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

public class RadioGroup : MonoBehaviour
{
    [SerializeField]
    private bool getCompsAlways = true;
    [SerializeField]
    private RadioBase[] radios;

    public void OnEnable()
    {
        if (getCompsAlways)
        {
            radios = GetComponentsInParent<RadioBase>();
        }
    }

    /// <summary>
    /// Flase - 0, True - 1
    /// </summary>
    /// <param name="isOn">Flase - 0, True - 1</param>
    public void Radio(bool isOn)
    {
        Radio(isOn ? 1 : 0);
    }

    public void Radio(int index)
    {
        foreach (var radio in radios)
        {
            radio.Radio(index);
        }
    }
}
