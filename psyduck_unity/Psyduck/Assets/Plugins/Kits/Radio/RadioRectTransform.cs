using System.Collections;
using System.Collections.Generic;
using UnityEngine;
/*
 * Prefab 中遵循： obj[0] 为关闭状态， obj[1] 为打开状态， 其余为扩展状态。
 * 只有打开关闭状态时，尽量使用 Radio(bool isOn) 方法
 */
public class RadioRectTransform : RadioBase
{
    [SerializeField]
    private RectTransform rectTransform = null;

    [SerializeField]
    private bool useAnchorPos = false;
    [SerializeField]
    private bool useSizeDelta = false;
    [SerializeField]
    private bool useOffset = false;

    [SerializeField]
    private Vector2[] anchorPosition = new Vector2[2];
    [SerializeField]
    private Vector2[] sizeDelta = new Vector2[2];
    [SerializeField]
    private Vector2[] offsetMin = new Vector2[2];
    [SerializeField]
    private Vector2[] offsetMax = new Vector2[2];

    private void Awake()
    {
        SetRadios();
    }

    public override void Radio(int index)
    {
        base.Radio(index);
        if (rectTransform == null)
            return;
        if (useSizeDelta && index < sizeDelta.Length)
            rectTransform.sizeDelta = sizeDelta[index];
        if (useAnchorPos && index < anchorPosition.Length)
            rectTransform.anchoredPosition = anchorPosition[index];
        if (useOffset && index < offsetMin.Length && index < offsetMax.Length)
        {
            rectTransform.offsetMin = offsetMin[index];
            rectTransform.offsetMax = offsetMax[index];
        }
    }

    private void SetRadios()
    {
        Radio(radioIndex);
    }
}
