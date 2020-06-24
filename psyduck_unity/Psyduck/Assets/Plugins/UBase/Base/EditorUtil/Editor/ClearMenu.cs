using System.IO;
using UnityEditor;
using UnityEngine;

namespace ClearTools
{
    public static class ClearMenu
    {
        private const string clearPersistent = "Tools/持久化数据/清除";
        private const string openPersistent = "Tools/持久化数据/打开";

        private const string clearPlayerPrefs = "Tools/持久化数据/清除(注册表)";
        private const string openPlayerPrefs = "Tools/持久化数据/打开(注册表)";


        [MenuItem(clearPersistent)]
        private static void ClearPersistent()
        {
            if (Directory.Exists(Application.persistentDataPath))
            {
                Directory.Delete(Application.persistentDataPath, true);
            }
        }

        [MenuItem(openPersistent)]
        private static void OpenPersistent()
        {
            if (Directory.Exists(Application.persistentDataPath))
            {
                System.Diagnostics.Process.Start(Application.persistentDataPath);
            }
        }

        [MenuItem(clearPlayerPrefs)]
        private static void ClearPlayerPrefs()
        {
            PlayerPrefs.DeleteAll();
        }

        [MenuItem(openPlayerPrefs)]
        private static void OpenPlayerPrefs()
        {
            
        }
    }
}