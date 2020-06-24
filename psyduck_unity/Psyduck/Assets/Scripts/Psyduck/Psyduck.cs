using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace Psyduck
{
    public class Psyduck : MonoBehaviour
    {
        public string host = "http://39.105.150.229:8748/psyduck";

        public static string _host => _instance.host;

        private static Psyduck _instance = null;

        void Awake()
        {
            _instance = this;
        }

        public static void Async(IEnumerator func)
        {
            _instance.StartCoroutine(func);
        }
    }
}
