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
        if (!path.StartsWith("Assets/Sprites", StringComparison.Ordinal))
            return;

        Rename(path, (name, ext, isFile) =>
        {
            return name.ToLower();
        });

        AssetDatabase.Refresh();
    }

    private static void Rename(string path, Func<string, string, bool, string> handle, bool loop = true, bool withMeta = true)
    {
        if (File.Exists(path))
        {
            var name = Path.GetFileNameWithoutExtension(path);
            var dir = Path.GetDirectoryName(path);
            var ext = Path.GetExtension(path);
            var tmp = Path.Combine(dir, "__tmp__" + name + ext);
            File.Move(path, tmp);
            name = handle(name, ext, true);
            var dst = Path.Combine(dir, name + ext);
            File.Move(tmp, dst);
        }
        else if (Directory.Exists(path))
        {
            var dir = Path.GetDirectoryName(path);
            var di = new DirectoryInfo(path);
            var name = di.Name;
            di.MoveTo(Path.Combine(dir, "__tmp__" + name));
            name = handle(name, "", false);
            di.MoveTo(Path.Combine(dir, name));
            if (loop)
            {
                foreach (var fsi in di.GetFileSystemInfos())
                {
                    if (fsi.Extension == ".meta" || fsi.Extension == ".DS_Store")
                        continue;
                    Rename(fsi.FullName, handle, loop, withMeta);
                }
            }
        }

        if (withMeta)
        {
            var meta = path + ".meta";
            Rename(meta, handle, loop, false);
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
