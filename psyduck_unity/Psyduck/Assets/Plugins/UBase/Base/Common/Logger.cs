using System;
using System.IO;
using System.Text;
namespace UniLogger
{

    public static class Logger
    {
        public static void LogException(object obj)
        {
            LogWithLevel(obj.ToString(), LogType.Exception);
        }


        public static void LogWarning(object obj)
        {
            LogWithLevel(obj.ToString(), LogType.Warning);
        }

        public static void Log(object obj)
        {
            LogWithLevel(obj.ToString(), LogType.Log);
        }

        public static void LogError(object obj)
        {
            LogWithLevel(obj.ToString(), LogType.Error);
        }

        public static void LogAssertion(object obj)
        {
            LogWithLevel(obj.ToString(), LogType.Assert);
        }

        private static object sync_tag = new object();
        private static void LogWithLevel(string str, LogType level)
        {
            lock (sync_tag)
            {
#if UNITY_4 || UNITY_5 || UNITY_2018 || UNITY_2019 || UNITY_2020 || UNITY_2021 || UNITY_2022 || UNITY_2023 || UNITY_2024 || UNITY_2025
                UnityEngine.Debug.LogFormat(str);
#else
            var lastColor = Console.ForegroundColor;
            Console.ForegroundColor = GetLogLevelColor(level);
            Console.WriteLine(str);
            Console.ForegroundColor = lastColor;
#endif
                if (logToFile)
                {
                    WriteToFile(str, level);
                }
            }
        }

        private static void WriteToFile(string str, LogType level)
        {
            string ext = Path.GetExtension(saveFilePath);
            string dir = Path.GetDirectoryName(saveFilePath);
            string path = Path.GetFileNameWithoutExtension(saveFilePath);
            string dateStr = DateTime.Now.ToString("_yyyy_MM_dd");
            path = Path.Combine(dir, path) + dateStr + ext;
            string spline = $"[{level}]: " + DateTime.Now.ToString("-> hh:mm:ss.fff \r\n");
            string content = spline + str + "\r\n\r\n";
            if (!File.Exists(path))
            {
                if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir))
                    Directory.CreateDirectory(dir);
                File.Create(path).Close();
            }
            StreamWriter sw = new StreamWriter(path, true, Encoding.UTF8);
            sw.Write(content);
            sw.Close();
        }

        private static ConsoleColor GetLogLevelColor(LogType level)
        {
            if (level == LogType.Log)
                return ConsoleColor.Green;
            else if (level == LogType.Error)
                return ConsoleColor.Red;
            else if (level == LogType.Warning)
                return ConsoleColor.DarkYellow;
            else
                return ConsoleColor.White;
        }

        public static bool logToFile { get; set; }
        public static string saveFilePath { get; set; }
    }

    public enum LogType
    {
        //
        // 摘要:
        //     LogType used for Errors.
        Error = 0,
        //
        // 摘要:
        //     LogType used for Asserts. (These could also indicate an error inside Unity itself.)
        Assert = 1,
        //
        // 摘要:
        //     LogType used for Warnings.
        Warning = 2,
        //
        // 摘要:
        //     LogType used for regular log messages.
        Log = 3,
        //
        // 摘要:
        //     LogType used for Exceptions.
        Exception = 4,
    }
}