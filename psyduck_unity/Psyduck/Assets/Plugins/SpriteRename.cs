using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using System.IO;
using System;

public class SpriteRename
{
    [MenuItem("Assets/SpriteRename/Format")]
    static void Format()
    {
        string[] strs = Selection.assetGUIDs;
        if (strs.Length != 1)
            return;
        var path = AssetDatabase.GUIDToAssetPath(strs[0]);
        Debug.Log(path);
        if (!path.StartsWith("Assets/Sprites"))
            return;

        Rename(path, (name, isFile) =>
        {
            return name.ToLower();
        });
    }

    private static void Rename(string path, Func<string, bool, string> handle)
    {
        if (File.Exists(path))
        {
            var ext = Path.GetExtension(path);
            var name = Path.GetFileNameWithoutExtension(path);
            var dir = Path.GetDirectoryName(path);
            var tmp = Path.Combine(dir, "_temp_" + name + "_temp_" + ext);
            File.Move(path, tmp);
            name = handle(name, true);
            var dst = Path.Combine(dir, "_temp_" + name + "_temp_" + ext);
            File.Move(tmp, dst);
        }
        else if (Directory.Exists(path))
        {
            var dir = Path.GetDirectoryName(path);
            var di = new DirectoryInfo(path);
            var name = handle(di.Name, false);
            di.MoveTo(Path.Combine(dir, name));
        }
    }

    [MenuItem("Assets/SpriteRename/RemoveSuffix")]
    static void RemoveSuffix()
    {
        string path = "Assets";
        string[] strs = Selection.assetGUIDs;
        if (strs != null)
        {
            path = "\"";
            for (int i = 0; i < strs.Length; i++)
            {
                if (i != 0)
                    path += "*";
                path += AssetDatabase.GUIDToAssetPath(strs[i]);
                if (AssetDatabase.GUIDToAssetPath(strs[i]) != "Assets")
                    path += "*" + AssetDatabase.GUIDToAssetPath(strs[i]) + ".meta";
            }
            path += "\"";
        }
        System.Diagnostics.Process process = new System.Diagnostics.Process();
        process.StartInfo.FileName = "TortoiseProc.exe";
        process.StartInfo.Arguments = "/command:commit /path:" + path;
        process.Start();
    }
}
