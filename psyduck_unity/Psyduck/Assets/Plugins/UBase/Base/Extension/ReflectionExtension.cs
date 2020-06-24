using System.Reflection;
using UnityEngine;

namespace ReflectionEx
{
    public static class ReflectionExtension
    {
        public static T ReflectProperty<T>(this object obj, string name)
        {
            if (obj == null)
            {
                Debug.LogError("reflection obj is null.");
                return default(T);
            }

            BindingFlags flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
            var p = obj.GetType().GetProperty(name, flags);
            if (p == null)
            {
                Debug.LogError($"{obj.GetType().Name} no Property named {name}.");
                return default(T);

            }
            return (T)p.GetValue(obj);
        }

        public static T ReflectField<T>(this object obj, string name)
        {
            if (obj == null)
            {
                Debug.LogError("reflection obj is null.");
                return default(T);
            }

            BindingFlags flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
            var f = obj.GetType().GetField(name, flags);
            if (f == null)
            {
                Debug.LogError($"{obj.GetType().Name} no Field named {name}.");
                return default(T);
            }
            return (T)f.GetValue(obj);
        }

        public static MethodInfo ReflectMethod(this object obj, string name)
        {
            if (obj == null)
            {
                Debug.LogError("reflection obj is null.");
                return null;
            }
            BindingFlags flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
            var m = obj.GetType().GetMethod(name, flags);
            if (m == null)
            {
                Debug.LogError($"{obj.GetType().Name} no Method named {name}.");
                return null;
            }
            return m;
        }

        public static void ReflectInvokeMethod(this object obj, string name, params object[] parameters)
        {
            if (obj == null)
            {
                Debug.LogError("reflection obj is null.");
                return;
            }

            BindingFlags flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
            var m = obj.GetType().GetMethod(name, flags);
            if (m == null)
            {
                Debug.LogError($"{obj.GetType().Name} no Method named {name}.");
                return;
            }
            m.Invoke(obj, parameters);
        }

        public static T ReflectInvokeMethod<T>(this object obj, string name, params object[] parameters)
        {
            if (obj == null)
            {
                Debug.LogError("reflection obj is null.");
                return default(T);
            }

            BindingFlags flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
            var m = obj.GetType().GetMethod(name, flags);
            if (m == null)
            {
                Debug.LogError($"{obj.GetType().Name} no Method named {name}.");
                return default(T);
            }
            return (T)m.Invoke(obj, parameters);
        }
    }
}