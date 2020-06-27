using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using System.IO;
using System;

public class SpriteRename
{
    [MenuItem("Assets/SpriteFomater/Format")]
    static void Format()
    {
        var path = GetSelectedPath();
        if (!path.StartsWith("Assets/Sprites", StringComparison.Ordinal))
            return;

        Rename(path, (name, ext, isFile) =>
        {
            name = name.ToLower();
            name = name.Replace("-", "_");
            name = name.Replace("+", "_");
            return name;
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

    private static string GetSelectedPath()
    {
        string[] strs = Selection.assetGUIDs;
        if (strs.Length != 1)
            return "";
        var path = AssetDatabase.GUIDToAssetPath(strs[0]);
        return path;
    }

    public class SpriteProcessor : AssetPostprocessor
    {
        private void OnPostprocessTexture(Texture2D texture)
        {
            if (!assetPath.StartsWith("Assets/Sprites/"))
                return;
            TextureImporter textureImporter = AssetImporter.GetAtPath(assetPath) as TextureImporter;
            if (textureImporter == null)
                return;

            textureImporter.textureType = TextureImporterType.Sprite;
            textureImporter.spriteImportMode = SpriteImportMode.Single;
            textureImporter.spritePixelsPerUnit = 100;
            textureImporter.spritePackingTag = "";

            TextureImporterSettings textureImportSetting = new TextureImporterSettings();
            textureImporter.ReadTextureSettings(textureImportSetting);
            textureImportSetting.spriteMeshType = SpriteMeshType.Tight;
            textureImportSetting.spriteExtrude = 1;
            textureImportSetting.spriteGenerateFallbackPhysicsShape = false;
            textureImporter.SetTextureSettings(textureImportSetting);

            textureImporter.mipmapEnabled = false;
            textureImporter.isReadable = false;
            textureImporter.wrapMode = TextureWrapMode.Clamp;
            textureImporter.filterMode = FilterMode.Bilinear;
            textureImporter.alphaIsTransparency = true;
            textureImporter.alphaSource = TextureImporterAlphaSource.FromInput;
            textureImporter.sRGBTexture = true;

            /*
            TextureImporterPlatformSettings platformSetting = textureImporter.GetPlatformTextureSettings("Standalone");
            platformSetting.maxTextureSize = 2048;
            platformSetting.textureCompression = TextureImporterCompression.Compressed;
            platformSetting.resizeAlgorithm = TextureResizeAlgorithm.Mitchell;
            platformSetting.overridden = true;
            platformSetting.textureCompression = TextureImporterCompression.Compressed;
            platformSetting.format = TextureImporterFormat.DXT5;
            textureImporter.SetPlatformTextureSettings(platformSetting);

            platformSetting = textureImporter.GetPlatformTextureSettings("iPhone");
            platformSetting.maxTextureSize = 2048;
            platformSetting.resizeAlgorithm = TextureResizeAlgorithm.Mitchell;
            platformSetting.overridden = true;
            platformSetting.compressionQuality = 100;
            platformSetting.textureCompression = TextureImporterCompression.Compressed;
            platformSetting.format = TextureImporterFormat.PVRTC_RGBA4;
            textureImporter.SetPlatformTextureSettings(platformSetting);

            platformSetting = textureImporter.GetPlatformTextureSettings("Android");
            platformSetting.maxTextureSize = 2048;
            platformSetting.resizeAlgorithm = TextureResizeAlgorithm.Mitchell;
            platformSetting.overridden = true;
            platformSetting.textureCompression = TextureImporterCompression.Compressed;
            platformSetting.format = TextureImporterFormat.ETC2_RGBA8;
            textureImporter.SetPlatformTextureSettings(platformSetting);

            platformSetting = textureImporter.GetPlatformTextureSettings("Web");
            platformSetting.maxTextureSize = 2048;
            platformSetting.resizeAlgorithm = TextureResizeAlgorithm.Mitchell;
            platformSetting.overridden = true;
            platformSetting.format = TextureImporterFormat.RGBA32;
            textureImporter.SetPlatformTextureSettings(platformSetting);
            */
        }
    }
}
