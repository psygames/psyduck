using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

static public class UIEditorMenuOptions
{
    private const string TemplatePath = "Assets/Plugins/Kits/UIEditor/Editor/Templates/";

    [MenuItem("GameObject/CustomUI/Create Empty", false, 11)]
    private static void CreateEmpty()
    {
        GameObject go = new GameObject();
        go.name = "GameObject";
        go.AddComponent<RectTransform>();
        PlaceUIElementRoot(go);
    }

    [MenuItem("GameObject/CustomUI/Delete", false, 12)]
    private static void DeleteTarget()
    {
        foreach (var obj in Selection.gameObjects)
        {
            if (obj != null)
            {
                Undo.DestroyObjectImmediate(obj);
            }
        }
    }

    private static void PlaceUIElementRoot(GameObject element)
    {
        GameObject parent = Selection.activeGameObject;
        string uniqueName = GameObjectUtility.GetUniqueNameForSibling(parent.transform, element.name);
        element.name = uniqueName;
        Undo.RegisterCreatedObjectUndo(element, "Create " + element.name);
        Undo.SetTransformParent(element.transform, parent.transform, "Parent " + element.name);
        GameObjectUtility.SetParentAndAlign(element, parent);
        Selection.activeGameObject = element;
    }

    #region Templates
    static private void AddTPrefab(string prefabName)
    {
        var res = AssetDatabase.LoadAssetAtPath<GameObject>(TemplatePath + prefabName + ".prefab");
        GameObject go = Object.Instantiate(res) as GameObject;
        go.name = res.name;
        PlaceUIElementRoot(go);
    }



    [MenuItem("GameObject/CustomUI/Image", false, 101)]
    static public void AddImage()
    {
        AddTPrefab("Image");
    }
    [MenuItem("GameObject/CustomUI/Text", false, 102)]
    static public void AddText()
    {
        AddTPrefab("Text");
    }
    [MenuItem("GameObject/CustomUI/Button", false, 103)]
    static public void AddButton()
    {
        AddTPrefab("Button");
    }
    [MenuItem("GameObject/CustomUI/ButtonPro", false, 104)]
    static public void AddButtonPro()
    {
        AddTPrefab("ButtonPro");
    }
    [MenuItem("GameObject/CustomUI/TextPro", false, 104)]
    static public void AddTextPro()
    {
        AddTPrefab("TextPro");
    }
    [MenuItem("GameObject/CustomUI/Slider", false, 104)]
    static public void AddSlider()
    {
        AddTPrefab("Slider");
    }
    [MenuItem("GameObject/CustomUI/RawImage", false, 104)]
    static public void AddRawImage()
    {
        AddTPrefab("RawImage");
    }
    [MenuItem("GameObject/CustomUI/ScrollView", false, 105)]
    static public void AddScrollView()
    {
        AddTPrefab("ScrollView");
    }
    [MenuItem("GameObject/CustomUI/ToggleAGroup", false, 105)]
    static public void AddToggleAGroup()
    {
        AddTPrefab("ToggleAGroup");
    }
    [MenuItem("GameObject/CustomUI/InputField", false, 102)]
    static public void AddInputField()
    {
        AddTPrefab("InputField");
    }
    #endregion
}
