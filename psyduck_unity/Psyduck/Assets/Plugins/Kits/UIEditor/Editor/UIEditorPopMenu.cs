using UnityEngine;
using UnityEditor;
using System.Collections;

public class MyHierarchyMenu
{
    [InitializeOnLoadMethod]
    static void StartInitializeOnLoadMethod()
    {
        EditorApplication.hierarchyWindowItemOnGUI += OnHierarchyGUI;
    }

    static void OnHierarchyGUI(int instanceID, Rect selectionRect)
    {
        if (Event.current != null && selectionRect.Contains(Event.current.mousePosition)
            && Event.current.button == 1 && Event.current.type <= EventType.MouseUp)
        {
            GameObject selectedGameObject = EditorUtility.InstanceIDToObject(instanceID) as GameObject;
            //这里可以判断selectedGameObject的条件
            if (selectedGameObject && selectedGameObject.GetComponent<RectTransform>() != null)
            {
                Vector2 mousePosition = Event.current.mousePosition;

                EditorUtility.DisplayPopupMenu(new Rect(mousePosition.x, mousePosition.y, 0, 0), "GameObject/CustomUI", null);
                Event.current.Use();
            }
        }
    }

}