using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BackgroundMask : MonoBehaviour
{
    public Color color = new Color(0f, 0f, 0f, 0.8f);
    public bool closePanel = true;

    private RectTransform m_tranform;
    private Transform m_parentTransform;

    private GameObject mMaskGo;
    private void OnEnable()
    {
        StartCoroutine(DelayShow());
    }

    private IEnumerator DelayShow()
    {
        yield return null;

        m_tranform = GetComponent<RectTransform>();
        m_parentTransform = transform.parent;

        DestroyGo();

        yield return null;

        if (mMaskGo == null && m_parentTransform != null)
        {
            mMaskGo = new GameObject();
            mMaskGo.name = this.name + "(MASK)";
            var trans = mMaskGo.AddComponent<RectTransform>();
            float zPos = m_tranform.anchoredPosition3D.z;
            trans.SetParent(m_parentTransform, false);
            trans.anchoredPosition3D = new Vector3(0, 0, zPos);
            trans.localScale = Vector3.one;
            trans.sizeDelta = new Vector2(10000, 10000);
            trans.SetSiblingIndex(m_tranform.GetSiblingIndex());

            mMaskGo.AddComponent<Image>().color = color;
            mMaskGo.AddComponent<UIEventListener>().onClick.AddListener(OnClick);
        }
    }

    private void OnClick(Vector2 pos)
    {
        if (closePanel)
        {
            var p = transform;
            do
            {
                var panel = p.GetComponent<ViewBase>();
                if (panel != null)
                {
                    UIManager.Close(panel.GetType());
                    break;
                }
                p = p.parent;
            }
            while (p != null);
        }
    }

    private void DestroyGo()
    {
        if (mMaskGo != null)
        {
            Destroy(mMaskGo);
            mMaskGo = null;
        }
    }

    private void OnDisable()
    {
        DestroyGo();
    }
}
