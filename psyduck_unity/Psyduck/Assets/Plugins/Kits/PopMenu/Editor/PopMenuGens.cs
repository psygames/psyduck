
/***
 * Auto Generate Script, Don't Edit.
***/
using System.IO;
using UnityEditor;
using UnityEngine;

static public class PopMenuGens
{
    [MenuItem("GameObject/PopMenu/Create Empty", false, 11)]
    private static void CreateEmpty()
    {
        GameObject go = new GameObject();
        go.name = "GameObject";
        go.AddComponent<RectTransform>();
        PlaceUIElementRoot(go);
    }

    [MenuItem("GameObject/PopMenu/Delete", false, 12)]
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
    
    static private void AddTPrefab(string prefabName)
    {
        var templateDir = PopMenuSettings.Instance.prefabTemplateDir;
        var prefabPath = Path.Combine(templateDir, prefabName + ".prefab");
        var res = AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
        GameObject go = Object.Instantiate(res) as GameObject;
        go.name = res.name;
        PlaceUIElementRoot(go);
    }

    
    [MenuItem("GameObject/PopMenu/Button", false, 101)]
    static public void AddButton()
    {
        AddTPrefab("Button");
    }
    
    [MenuItem("GameObject/PopMenu/Image", false, 102)]
    static public void AddImage()
    {
        AddTPrefab("Image");
    }
    
    [MenuItem("GameObject/PopMenu/InputField", false, 103)]
    static public void AddInputField()
    {
        AddTPrefab("InputField");
    }
    
    [MenuItem("GameObject/PopMenu/RawImage", false, 104)]
    static public void AddRawImage()
    {
        AddTPrefab("RawImage");
    }
    
    [MenuItem("GameObject/PopMenu/ScrollView", false, 105)]
    static public void AddScrollView()
    {
        AddTPrefab("ScrollView");
    }
    
    [MenuItem("GameObject/PopMenu/Slider", false, 106)]
    static public void AddSlider()
    {
        AddTPrefab("Slider");
    }
    
    [MenuItem("GameObject/PopMenu/Text", false, 107)]
    static public void AddText()
    {
        AddTPrefab("Text");
    }
    
}
