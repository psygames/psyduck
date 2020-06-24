using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

public class RadioBase : MonoBehaviour
{
    [SerializeField]
    protected int radioIndex = 0;
    public virtual int index { get { return radioIndex; } }

    /// <summary>
    /// Flase - 0, True - 1
    /// </summary>
    /// <param name="isOn">Flase - 0, True - 1</param>
    public virtual void Radio(bool isOn)
    {
        Radio(isOn ? 1 : 0);
    }

    public virtual void Radio(int index)
    {

        this.radioIndex = index;
    }
}
