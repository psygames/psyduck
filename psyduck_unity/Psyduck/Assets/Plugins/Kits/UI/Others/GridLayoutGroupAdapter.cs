using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
[RequireComponent(typeof(UnityEngine.UI.GridLayoutGroup))]
public class GridLayoutGroupAdapter : MonoBehaviour
{
    public enum AdapterType
    {
        Constraint = 1,
        ItemSize = 2,
        Scale = 3,
    }

    public AdapterType adapterType = AdapterType.Constraint;
    public Vector2 sizeOffset = Vector2.zero;
    public Vector2 cellSizeOffset = Vector2.zero;
    public bool fitWidth;
    public bool fitHeight;
    public int fitSizeDivCount = 1;


    public Vector2 cellSize
    {
        get
        {
            return m_gridLayoutGroup.cellSize;
        }
        set
        {
            m_gridLayoutGroup.cellSize = value;
        }
    }

    public Vector2 spacing
    {
        get
        {
            return m_gridLayoutGroup.spacing;
        }
    }

    public RectOffset padding
    {
        get
        {
            return m_gridLayoutGroup.padding;
        }
    }

    public bool isVertical
    {
        get
        {
            return m_gridLayoutGroup.constraint == UnityEngine.UI.GridLayoutGroup.Constraint.FixedColumnCount;
        }
    }

    public int constraintCount
    {
        get
        {
            return m_gridLayoutGroup.constraintCount;
        }
        set
        {
            m_gridLayoutGroup.constraintCount = value;
        }
    }

    float lastWidth;
    float lastHeight;
    RectTransform m_cachedRectTransform;
    UnityEngine.UI.GridLayoutGroup m_gridLayoutGroup;

    private void Awake()
    {
        m_gridLayoutGroup = GetComponent<UnityEngine.UI.GridLayoutGroup>();
        m_cachedRectTransform = transform.parent.GetComponent<RectTransform>();
    }

    private void OnEnable()
    {
        if (m_cachedRectTransform == null)
            m_cachedRectTransform = transform.parent.GetComponent<RectTransform>();
    }

    void LateUpdate()
    {
        if (m_cachedRectTransform == null || m_gridLayoutGroup == null)
            return;

        if (Mathf.Approximately(lastWidth, m_cachedRectTransform.rect.width)
            && Mathf.Approximately(lastHeight, m_cachedRectTransform.rect.height))
            return;

        lastWidth = m_cachedRectTransform.rect.width;
        lastHeight = m_cachedRectTransform.rect.height;

        if (adapterType == AdapterType.Constraint)
        {
            ResetConstraint();
        }
        else if (adapterType == AdapterType.ItemSize)
        {
            Resize();
        }
    }

    void ResetConstraint()
    {
        float val;
        float space;
        if (isVertical)
        {
            val = m_cachedRectTransform.rect.width + spacing.x - padding.horizontal;
            space = cellSize.x + spacing.x;
        }
        else
        {
            val = m_cachedRectTransform.rect.height + spacing.y - padding.vertical;
            space = cellSize.y + spacing.y;
        }

        constraintCount = (int)(val / space);
    }

    void Resize()
    {
        if (!fitWidth && !fitHeight)
            return;

        Vector2 newSize = cellSize;
        if (fitWidth)
        {
            newSize.x = cellSizeOffset.x + (sizeOffset.x + m_cachedRectTransform.rect.width) / fitSizeDivCount;
        }

        if (fitHeight)
        {
            newSize.y = cellSizeOffset.y + (sizeOffset.y + m_cachedRectTransform.rect.height) / fitSizeDivCount;
        }

        cellSize = newSize;
    }
}
