using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using LitJson;

namespace Psyduck
{
    public class ActionBase
    {
        public bool isBusy { get; protected set; }

        private IEnumerator _Post(string addr, Dictionary<string, string> postData, Action<string> callback)
        {
            var url = Psyduck._host + "/" + addr;
            var req = UnityWebRequest.Post(url, postData);
            yield return req.SendWebRequest();
            if (req.isHttpError || req.isNetworkError)
            {
                Debug.LogError(req.error + " -> " + url);
                req.Dispose();
                yield break;
            }
            var text = req.downloadHandler.text;
            req.Dispose();
            callback?.Invoke(text);
        }

        private IEnumerator _IntervalPost(float interval, Func<bool> condition, int maxTimes,
            string addr, Dictionary<string, string> postData, Action<string> callback)
        {
            for (int i = 0; i < maxTimes && (condition == null || condition.Invoke()); i++)
            {
                yield return _Post(addr, postData, callback);
                yield return new WaitForSeconds(interval);
            }
        }

        protected void Async(IEnumerator enumerator)
        {
            Psyduck.Async(enumerator);
        }

        protected void Post(string addr, Dictionary<string, string> postData, Action<string> callback)
        {
            Async(_Post(addr, postData, callback));
        }

        protected void IntervalPost(string addr, Dictionary<string, string> postData,
            Action<string> callback, float interval, Func<bool> condition, int maxTimes)
        {
            Async(_IntervalPost(interval, condition, maxTimes, addr, postData, callback));
        }
    }
}