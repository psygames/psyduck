using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
[CustomEditor(typeof(RadioRectTransform), true)]
public class RadioRectTransformEditor : Editor
{
    SerializedProperty rectTransform;
    SerializedProperty m_radioIndex;
    SerializedProperty useAnchorPos;
    SerializedProperty useSizeDelta;
    SerializedProperty useOffset;
    SerializedProperty anchorPosition;
    SerializedProperty sizeDelta;
    SerializedProperty offsetMin;
    SerializedProperty offsetMax;

    private void OnEnable()
    {
        rectTransform = serializedObject.FindProperty("rectTransform");
        m_radioIndex = serializedObject.FindProperty("radioIndex");
        useAnchorPos = serializedObject.FindProperty("useAnchorPos");
        useSizeDelta = serializedObject.FindProperty("useSizeDelta");
        useOffset = serializedObject.FindProperty("useOffset");
        anchorPosition = serializedObject.FindProperty("anchorPosition");
        sizeDelta = serializedObject.FindProperty("sizeDelta");
        offsetMin = serializedObject.FindProperty("offsetMin");
        offsetMax = serializedObject.FindProperty("offsetMax");
    }

    private void DrawArrayField(SerializedProperty property)
    {
        if (!property.isArray)
        {
            EditorGUILayout.PropertyField(property);
            return;
        }

        EditorGUI.indentLevel = 1;
        property.arraySize = EditorGUILayout.IntField("Size", property.arraySize);
        for (int i = 0; i < property.arraySize; i++)
        {
            EditorGUILayout.PropertyField(property.GetArrayElementAtIndex(i));
        }
        EditorGUI.indentLevel = 0;
    }

    public override void OnInspectorGUI()
    {
        if (rectTransform.objectReferenceValue == null)
        {
            var trans = (target as RadioRectTransform).GetComponent<RectTransform>();
            rectTransform.objectReferenceValue = trans;
        }
        EditorGUILayout.PropertyField(rectTransform);

        var radio = (target as RadioRectTransform);

        EditorGUILayout.PropertyField(m_radioIndex);
        var isOn = EditorGUILayout.Toggle("Radio", m_radioIndex.intValue == 1);

        EditorGUILayout.PropertyField(useAnchorPos);
        if (useAnchorPos.boolValue)
        {
            DrawArrayField(anchorPosition);
        }

        EditorGUILayout.PropertyField(useSizeDelta);
        if (useSizeDelta.boolValue)
        {
            DrawArrayField(sizeDelta);
        }

        EditorGUILayout.PropertyField(useOffset);
        if (useOffset.boolValue)
        {
            DrawArrayField(offsetMin);
            DrawArrayField(offsetMax);
        }


        if (m_radioIndex.intValue < 2 || isOn)
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
            "    obj[0] 为关闭状态\n" +
            "    obj[1] 为开启状态\n" +
            "    其余为扩展状态\n" +
            "<size=12>PS: 只有关闭开启状态时，尽量使用 Radio(bool) 方法</size>", style);
        EditorGUILayout.Space();
    }
}
