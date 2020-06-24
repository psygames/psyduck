using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using ReflectionEx;

[CustomEditor(typeof(GridLayoutGroupAdapter))]
public class GridLayoutGroupAdapterEditor : Editor
{
    public override void OnInspectorGUI()
    {
        var adapter = target as GridLayoutGroupAdapter;
        EditorGUILayout.PropertyField(serializedObject.FindProperty("adapterType"));
        if (adapter.adapterType == GridLayoutGroupAdapter.AdapterType.Constraint)
        {
        }
    }
}
