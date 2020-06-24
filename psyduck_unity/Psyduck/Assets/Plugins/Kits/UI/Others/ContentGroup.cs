using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Reflection;

public class ContentGroup : MonoBehaviour
{
    public MonoBehaviour template;
    private object itemList;
    private void Awake()
    {
        template.gameObject.SetActive(false);
    }

    public void SetData<P, D>(ICollection<D> dataList)
    where P : MonoBehaviour
    {
        SetData<P, D>(dataList, (index, item, data) =>
        {
            BindingFlags flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
            item.GetType().GetMethod("SetData", flags)?.Invoke(item, new object[] { data });
        });
    }

    public void SetData<P, D>(ICollection<D> dataList, Action<int, P, D> setContentFunc)
    where P : MonoBehaviour
    {
        if (itemList == null)
            itemList = new List<P>();
        SetListContent((P)template, transform, itemList as List<P>, dataList, setContentFunc);
    }

    static void SetListContent<P, D>(P prefab, Transform parent, List<P> itemList, ICollection<D> dataList,
        Action<int, P, D> setContentFunc, int start = 0, int count = 0)
        where P : MonoBehaviour
    {
        if (itemList == null)
            return;
        if (dataList == null)
        {
            foreach (var item in itemList)
            {
                SetActive(item, false);
            }
        }
        else
        {
            CreateItemList(prefab, parent, itemList, dataList.Count, start, count);
            using (var emu = dataList.GetEnumerator())
            {
                for (int i = 0; i < start && emu.MoveNext(); ++i)
                {
                }
                for (int i = 0; i < itemList.Count; ++i)
                {
                    if (emu.MoveNext())
                    {
                        int index = start + i;
                        var item = itemList[i];
                        var data = emu.Current;
                        SetActive(item, true);
                        setContentFunc?.Invoke(index, item, data);
                    }
                    else
                    {
                        SetActive(itemList[i], false);
                    }
                }
            }
        }
    }

    private static void CreateItemList<P>(P prefab, Transform parent, List<P> itemList, int dataListCount, int start, int count)
        where P : MonoBehaviour
    {
        if (count == 0 || (start + count) > dataListCount)
        {
            count = dataListCount - start;
        }
        while (itemList.Count < count)
        {
            itemList.Add(AddChild(parent, prefab));
        }
    }

    public static T AddChild<T>(Transform parent, T prefab) where T : MonoBehaviour
    {
        T t = Instantiate(prefab) as T;
        t.name = prefab.name;
        t.transform.SetParent(parent, false);
        return t;
    }
    static void SetActive<P>(P p, bool active) where P : MonoBehaviour
    {
        p.gameObject.SetActive(active);
    }
}
