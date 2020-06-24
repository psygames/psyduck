using UnityEditor;
using UnityEngine;
[CustomEditor(typeof(FadeGroup), true)]
public class FadeGroupEditor : Editor
{
    public override void OnInspectorGUI()
    {
        EditorGUILayout.HelpBox("如果勾选 [Always Find Fades] ，" +
            "将在每次 FadeIn 或 FadeOut 的时候获取所有子节点中的Fade。\n" +
            "如果勾选 [On Start Find Fades]， 则在 OnStart 时获取所有自己点Fade。\n" +
            "若以上均未勾选，则使用自己管理的 Fade 列表。", MessageType.Info);
        EditorGUILayout.Space();

        bool isCustom = !PropertyField("alwaysFindFades").boolValue
            && !PropertyField("onStartFindFades").boolValue;
        if (!isCustom)
        {
            serializedObject.FindProperty("m_fades").ClearArray();
        }
        serializedObject.ApplyModifiedProperties();

        EditorGUILayout.Space();
        FadeGroup fadeGroup = target as FadeGroup;
        if (EditorApplication.isPlaying && GUILayout.Button("All Fade In"))
        {
            fadeGroup.FadeIn();
            EditorGUILayout.Space();
        }
        if (EditorApplication.isPlaying && GUILayout.Button("All Fade Out"))
        {
            fadeGroup.FadeOut();
            EditorGUILayout.Space();
        }


        GUIStyle style = new GUIStyle();
        style.richText = true;
        EditorGUILayout.LabelField("<b><color=#8CEA00><size=14>"
            + (isCustom ? "Custom Fades" : "Fades") + "</size></color></b>", style);
        EditorGUILayout.BeginVertical("box");

        var m_fades = serializedObject.FindProperty("m_fades");
        var fades = new Fade[0];
        if (!isCustom)
        {
            fades = fadeGroup.GetComponentsInChildren<Fade>(true);
        }
        else
        {
            int length = m_fades.arraySize;
            fades = new Fade[length];
            for (int i = 0; i < length; i++)
            {
                var elem = m_fades.GetArrayElementAtIndex(i);
                fades[i] = (Fade)elem.objectReferenceValue;
            }
        }

        for (int i = 0; i < fades.Length; i++)
        {
            var fade = fades[i];
            EditorGUILayout.BeginHorizontal();

            EditorGUI.BeginDisabledGroup(!fade.enableFadeIn);
            if (EditorApplication.isPlaying && GUILayout.Button("Fade In"))
            {
                fade.FadeIn();
            }
            EditorGUI.EndDisabledGroup();

            EditorGUI.BeginDisabledGroup(!fade.enableFadeOut);
            if (EditorApplication.isPlaying && GUILayout.Button("Fade Out"))
            {
                fade.FadeOut();
            }
            EditorGUI.EndDisabledGroup();

            EditorGUILayout.LabelField($" <b><color=#cccccc>{fade.name}</color></b> <color=#55AA00>[{fade.GetType().Name}]</color>", style);

            if (isCustom && GUILayout.Button("-", GUILayout.Width(20)))
            {
                m_fades.arraySize = m_fades.arraySize - 1;
                for (int j = 0; j < m_fades.arraySize; j++)
                {
                    int index = j;
                    if (j >= i) index += 1;
                    m_fades.GetArrayElementAtIndex(j).objectReferenceValue = fades[index];
                }
                serializedObject.ApplyModifiedProperties();
            }
            EditorGUILayout.EndHorizontal();
        }

        if (isCustom && GUILayout.Button("Find All Fades"))
        {
            var allFades = fadeGroup.GetComponentsInChildren<Fade>(true);
            m_fades.arraySize = allFades.Length;
            for (int i = 0; i < allFades.Length; i++)
            {
                var elem = m_fades.GetArrayElementAtIndex(i);
                elem.objectReferenceValue = allFades[i];
            }
        }

        EditorGUILayout.EndVertical();
        EditorGUILayout.Space();

        serializedObject.ApplyModifiedProperties();
    }

    public SerializedProperty PropertyField(string propertyName)
    {
        var field = serializedObject.FindProperty(propertyName);
        if (field != null)
            EditorGUILayout.PropertyField(field);
        return field;
    }
}
