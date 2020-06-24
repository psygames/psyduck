using UnityEngine;

public static class Vibrator
{
    public static void Vibrate(float seconds)
    {
#if UNITY_ANDROID && !UNITY_EDITOR
        AndroidVibrator.Vibrate((long)(seconds * 1000));
#else
        // ios failed
        // Handheld.Vibrate(); 
#endif
    }

    public static void Vibrate()
    {
        // ios failed
        // Handheld.Vibrate();
    }

    public static void Cancel()
    {

#if UNITY_ANDROID && !UNITY_EDITOR
        AndroidVibrator.Cancel();
#else
        // Cancel Vibration 
#endif
    }



    /// <summary>
    /// Android Only
    /// </summary>
#if UNITY_ANDROID && !UNITY_EDITOR || UNITY_EDITOR
    private static class AndroidVibrator
    {
        public static AndroidJavaClass unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
        public static AndroidJavaObject currentActivity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity");
        public static AndroidJavaObject vibrator = currentActivity.Call<AndroidJavaObject>("getSystemService", "vibrator");
        public static AndroidJavaObject context = currentActivity.Call<AndroidJavaObject>("getApplicationContext");

        ///<summary>
        /// Only on Android
        /// https://developer.android.com/reference/android/os/Vibrator.html#vibrate(long)
        ///</summary>
        public static void Vibrate(long milliseconds)
        {
            if (!HasVibrator())
                return;
            vibrator.Call("vibrate", milliseconds);
        }

        ///<summary>
        ///Only on Android
        ///</summary>
        public static void Cancel()
        {
            if (!HasVibrator())
                return;
            vibrator.Call("cancel");
        }

        private static bool _checked;
        private static bool _hasVibrater;
        private static bool HasVibrator()
        {
            if (_checked)
            {
                return _hasVibrater;
            }

            AndroidJavaClass contextClass = new AndroidJavaClass("android.content.Context");
            string Context_VIBRATOR_SERVICE = contextClass.GetStatic<string>("VIBRATOR_SERVICE");
            AndroidJavaObject systemService = context.Call<AndroidJavaObject>("getSystemService", Context_VIBRATOR_SERVICE);
            if (systemService.Call<bool>("hasVibrator"))
            {
                _hasVibrater = true;
            }
            else
            {
                _hasVibrater = false;
            }
            _checked = true;
            return _hasVibrater;
        }
    }
#endif

}


