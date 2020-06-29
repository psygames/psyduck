using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEditor;

public class PopMenuSettings : ScriptableObject
{
    public const string ASSET_PATH = "Assets/Plugins/Kits/PopMenu/Editor/Settings.asset";

    public string rootPath = "Assets/Plugins/Kits/PopMenu/Editor/";
    public string menuRoot = "GameObject/PopMenu/";
    public string prefabTemplateDir => Path.Combine(rootPath, "Templates");
    public string generateScriptPath => Path.Combine(rootPath, "PopMenuGens.cs");
    public string generateScriptTemplatePath => Path.Combine(rootPath, "PopMenuGensTemplate.txt");

    private static PopMenuSettings _ins;
    public static PopMenuSettings Instance
    {
        get
        {
            if (_ins == null)
            {
                _ins = AssetDatabase.LoadAssetAtPath<PopMenuSettings>(ASSET_PATH);
            }
            return _ins;
        }
    }
}
