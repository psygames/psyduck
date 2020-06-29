using UnityEngine;
using UnityEditor;
using System.Collections;
using System.Collections.Generic;
using System;
using System.IO;

namespace PopMenu
{
    public class PopMenu
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
                    var settings = PopMenuSettings.Instance;
                    Vector2 mousePosition = Event.current.mousePosition;
                    EditorUtility.DisplayPopupMenu(new Rect(mousePosition.x, mousePosition.y, 0, 0), settings.menuRoot, null);
                    Event.current.Use();
                }
            }
        }

        [MenuItem("Tools/PopMenuGenerate")]
        static void PopMenuGenerate()
        {
            var settings = PopMenuSettings.Instance;
            var asset = AssetDatabase.LoadAssetAtPath<TextAsset>(settings.generateScriptTemplatePath);
            var regions = BuildText(asset.text);
            var main = regions["main"];
            var template = regions["template"];

            var _temps = "";
            var files = Directory.GetFiles(settings.prefabTemplateDir, "*.prefab");
            int order = 101;
            foreach (var file in files)
            {
                var name = Path.GetFileNameWithoutExtension(file);
                var _temp = template;
                _temp = _temp.Replace("{name}",name);
                _temp = _temp.Replace("{order}", order.ToString());
                _temps += _temp;
                order++;
            }

            main = main.Replace("{template}", _temps);
            main = main.Replace("{menuRoot}", settings.menuRoot);

            File.WriteAllText(settings.generateScriptPath, main);
            AssetDatabase.Refresh();
        }

        private static Dictionary<string, string> BuildText(string text)
        {
            var regions = new Dictionary<string, string>();
            var index = text.IndexOf("{region:");
            while (index != -1)
            {
                index += 8;
                var end = text.IndexOf("}", index);
                if (end == -1)
                    break;
                var name = text.Substring(index, end - index);
                index = end + 1;
                end = text.IndexOf("{endregion}", index);
                var content = text.Substring(index, end - index);
                regions.Add(name, content);

                index = end + 11;
                index = text.IndexOf("{region:", index);
            }
            return regions;
        }
    }
}