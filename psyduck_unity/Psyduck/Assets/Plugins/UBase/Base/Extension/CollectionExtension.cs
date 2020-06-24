using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;
using System;

public static class CollectionExtension
{
    public static T First<T>(this ICollection<T> collection, Func<T, bool> predicate = null)
    {
        foreach (var t in collection)
        {
            if (predicate == null || predicate(t))
            {
                return t;
            }
        }
        return default;
    }

    public static bool Any<T>(this ICollection<T> collection, Func<T, bool> predicate = null)
    {
        return collection.First(predicate) != null;
    }

    public static bool All<T>(this ICollection<T> collection, Func<T, bool> predicate)
    {
        foreach (var t in collection)
        {
            if (!predicate(t))
            {
                return false;
            }
        }
        return true;
    }

    public static int Count<T>(this ICollection<T> collection, Func<T, bool> predicate)
    {
        int count = 0;
        foreach (var t in collection)
        {
            if (predicate(t))
            {
                count++;
            }
        }
        return count;
    }

    public static T Max<T>(this ICollection<T> collection, Func<T, IComparable> predicate)
    {
        T first = default;
        IComparable firstCompare = default;
        foreach (var t in collection)
        {
            if (first == null || predicate(t).CompareTo(firstCompare) > 0)
            {
                firstCompare = predicate(t);
                first = t;
            }
        }
        return first;
    }

    public static T Min<T>(this ICollection<T> collection, Func<T, IComparable> predicate)
    {
        T first = default;
        IComparable firstCompare = default;
        foreach (var t in collection)
        {
            if (first == null || predicate(t).CompareTo(firstCompare) < 0)
            {
                firstCompare = predicate(t);
                first = t;
            }
        }
        return first;
    }

    public static List<T> ToList<T>(this ICollection<T> collection, Func<T, bool> predicate = null)
    {
        var list = new List<T>();
        foreach (var c in collection)
        {
            if (predicate == null || predicate(c))
            {
                list.Add(c);
            }
        }
        return list;
    }

    public static int IndexOf<T>(this ICollection<T> collection, T t)
    {
        int i = 0;
        foreach (var c in collection)
        {
            if (c.Equals(t))
            {
                return i;
            }
            i++;
        }
        return -1;
    }

    public static void ForIndex<T>(this Array array, Action<int, T> callback) where T : class
    {
        for (int i = 0; i < array.Length; i++)
        {
            callback(i, array.GetValue(i) as T);
        }
    }

    public static void ForIndex(this float[] array, Action<int, float> callback)
    {
        for (int i = 0; i < array.Length; i++)
        {
            callback(i, array[i]);
        }

    }
}
