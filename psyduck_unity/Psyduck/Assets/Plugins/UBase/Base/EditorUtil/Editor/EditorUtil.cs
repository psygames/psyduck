using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using System;

namespace UnityEditor
{
    public static class EditorUtil
    {
        public static string Popup(string selected, string[] array, string[] aliasArray = null)
        {
            var index = array.ToList().IndexOf(selected);
            index = index < 0 ? 0 : index;
            index = EditorGUILayout.Popup(index, aliasArray ?? array);
            return index >= 0 && index < array.Length ? array[index] : selected;
        }

        public static void DisableGroup(Action callback)
        {
            EditorGUI.BeginDisabledGroup(true);
            callback?.Invoke();
            EditorGUI.EndDisabledGroup();
        }

        public static void Horizontal(Action callback)
        {
            EditorGUILayout.BeginHorizontal();
            callback?.Invoke();
            EditorGUILayout.EndHorizontal();
        }

        public static void Vertical(Action callback)
        {
            EditorGUILayout.BeginVertical();
            callback?.Invoke();
            EditorGUILayout.EndVertical();
        }

        public static void Box(Action callback)
        {
            EditorGUILayout.BeginVertical("box");
            callback?.Invoke();
            EditorGUILayout.EndVertical();
        }

        public static void Box(string title, Action callback)
        {
            Label(title);
            EditorGUILayout.BeginVertical("box");
            callback?.Invoke();
            EditorGUILayout.EndVertical();
        }

        private static Dictionary<long, Vector2> sScrollPos = new Dictionary<long, Vector2>();
        public static void ScrollView(Action callback)
        {
            var hash = callback.GetHashCode();
            if (!sScrollPos.ContainsKey(hash))
                sScrollPos.Add(hash, Vector2.zero);
            sScrollPos[hash] = EditorGUILayout.BeginScrollView(sScrollPos[hash]);
            callback?.Invoke();
            EditorGUILayout.EndScrollView();
        }

        private static GUIStyle GeneralStyle(Color color = default)
        {
            GUIStyle style = new GUIStyle();
            if (color == default)
            {
                color = Color.white;
            }

            style.active.textColor = color;
            style.focused.textColor = color;
            style.normal.textColor = color;
            style.richText = true;
            return style;
        }

        public static string Text(string title, string content)
        {
            return EditorGUILayout.TextField(title, content);
        }

        public static string Text(string content)
        {
            return EditorGUILayout.TextField(content);
        }

        public static void Label(string label1, string label2, Color color = default)
        {
            if (color == default)
                EditorGUILayout.LabelField(label1, label2);
            else
                EditorGUILayout.LabelField(label1, label2, GeneralStyle(color));
        }

        public static void Label(string label, Color color = default)
        {
            if (color == default)
                EditorGUILayout.LabelField(label);
            else
                EditorGUILayout.LabelField(label, GeneralStyle(color));
        }

        public static Enum Enum(string title, Enum selected)
        {
            return EditorGUILayout.EnumPopup(title, selected);
        }

        public static string PrefsStringField(string prefName, string title, string defaultValue = "")
        {
            var prefStr = EditorPrefs.GetString(prefName, defaultValue);
            var str = (EditorGUILayout.TextField(title, prefStr));
            if (str != prefStr)
            {
                EditorPrefs.SetString(prefName, str);
            }
            return str;
        }
    }
}