using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
[CustomEditor(typeof(RadioObjects), true)]
public class RadioObjectsEditor : Editor
{
    SerializedProperty m_gameObjects;
    SerializedProperty m_radioIndex;
    private void OnEnable()
    {
        m_gameObjects = serializedObject.FindProperty("gameObjects");
        m_radioIndex = serializedObject.FindProperty("radioIndex");
    }


    public override void OnInspectorGUI()
    {
        base.OnInspectorGUI();
        var radio = (target as RadioObjects);
        var isOn = EditorGUILayout.Toggle("Radio", m_radioIndex.intValue == 1);
        if (m_radioIndex.intValue >= 0 && m_radioIndex.intValue < 2 || isOn)
            m_radioIndex.intValue = isOn ? 1 : 0;
        serializedObject.ApplyModifiedProperties();
        radio.Radio(m_radioIndex.intValue);

        EditorGUILayout.Space();
        var style = GUIStyle.none;
        style.fontSize = 16;
        style.normal.textColor = Color.green;
        style.active.textColor = Color.green;
        style.richText = true;
        EditorGUILayout.TextArea("Prefab需遵循： \n" +
            "    obj[0] 为不可用状态\n" +
            "    obj[1] 为可用状态\n" +
            "    其余为扩展状态\n" +
            "<size=12>PS: 只有可用、不可用状态时，尽量使用 Radio(bool) 方法</size>", style);
        EditorGUILayout.Space();
    }
}
