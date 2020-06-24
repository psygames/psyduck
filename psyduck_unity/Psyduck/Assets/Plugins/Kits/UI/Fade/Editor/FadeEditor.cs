using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(Fade), true)]
public class FadeEditor : Editor
{
    public override void OnInspectorGUI()
    {
        GUILayout.Space(10);
        Fade fade = target as Fade;
        #region  Fade In
        var style = new GUIStyle();
        style.richText = true;
        EditorGUILayout.BeginHorizontal();
        EditorGUILayout.LabelField($"<b><color=#{(fade.enableFadeIn ? "4DFFFF" : "7B7B7B")}><size=14>Fade In</size></color></b>", style, GUILayout.Width(60));
        fade.enableFadeIn = EditorGUILayout.Toggle(fade.enableFadeIn);
        EditorGUILayout.EndHorizontal();
        if (fade.enableFadeIn)
        {
            EditorGUILayout.BeginVertical("box");
            if (EditorApplication.isPlaying && GUILayout.Button("Trigger"))
            {
                fade.FadeIn();
            }
            PropertyField("onEnableFadeIn");
            PropertyField("fadeInReset");
            PropertyField("fadeInMethod");
            PropertyField("fadeInDelay");
            PropertyField("fadeInDuration");
            PropertyField("autoFadeOut");
            EditorGUILayout.EndVertical();
        }
        GUILayout.Space(10);
        #endregion

        #region  Fade Out
        EditorGUILayout.BeginHorizontal();
        EditorGUILayout.LabelField($"<b><color=#{(fade.enableFadeOut ? "4DFFFF" : "7B7B7B")}><size=14>Fade Out</size></color></b>", style, GUILayout.Width(72));
        fade.enableFadeOut = EditorGUILayout.Toggle(fade.enableFadeOut);
        EditorGUILayout.EndHorizontal();
        if (fade.enableFadeOut)
        {
            EditorGUILayout.BeginVertical("box");
            if (EditorApplication.isPlaying && GUILayout.Button("Trigger"))
            {
                fade.FadeOut();
            }
            PropertyField("fadeOutReset");
            PropertyField("fadeOutMethod");
            PropertyField("fadeOutDelay");
            PropertyField("fadeOutDuration");
            PropertyField("outSetInactive");
            EditorGUILayout.EndVertical();
        }
        GUILayout.Space(10);
        #endregion

        #region  From To
        EditorGUILayout.LabelField("<b><color=#4DFFFF><size=14>From To</size></color></b>", style);
        EditorGUILayout.BeginVertical("box");
        if (GUILayout.Button("set [from] as current"))
        {
            SetPropertyValueAsCurrent("from");
        }
        PropertyField("from");
        if (GUILayout.Button("set [to] as current"))
        {
            SetPropertyValueAsCurrent("to");
        }
        PropertyField("to");
        EditorGUILayout.EndVertical();
        GUILayout.Space(10);
        #endregion
        serializedObject.ApplyModifiedProperties();
    }

    void SetPropertyValueAsCurrent(string propertyName)
    {
        Fade fade = target as Fade;
        if (fade is FadeAlpha && fade.GetComponent<CanvasGroup>() != null)
        {
            serializedObject.FindProperty(propertyName).floatValue = fade.GetComponent<CanvasGroup>().alpha;
        }
        else if (fade is FadePosition)
        {
            Vector2 value = fade.GetComponent<RectTransform>().anchoredPosition;
            serializedObject.FindProperty(propertyName).vector2Value = value;
        }
        else if (fade is FadeSize)
        {
            Vector2 value = fade.GetComponent<RectTransform>().sizeDelta;
            serializedObject.FindProperty(propertyName).vector2Value = value;
        }
        else if (fade is FadeScale)
        {
            Vector2 value = fade.transform.localScale;
            serializedObject.FindProperty(propertyName).vector2Value = value;
        }
        else if (fade is FadeColor && fade.GetComponent<UnityEngine.UI.Graphic>() != null)
        {
            serializedObject.FindProperty(propertyName).colorValue = fade.GetComponent<UnityEngine.UI.Graphic>().color;
        }
        // Add Others Here
    }

    public void PropertyField(string propertyName, params GUILayoutOption[] options)
    {
        var field = serializedObject.FindProperty(propertyName);
        if (field != null)
            EditorGUILayout.PropertyField(field, options);
    }
}
