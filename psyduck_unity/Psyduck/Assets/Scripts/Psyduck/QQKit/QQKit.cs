using System;
using System.Collections;
using System.Collections.Generic;
using LitJson;
using UnityEngine;
using UnityEngine.Networking;

namespace Psyduck
{
    public class QQKit
    {
        private const string defaultGroupNum = "606737006";

        private static IEnumerator _Post(string addr, Dictionary<string, string> postData, Action<string> callback)
        {
            var url = Psyduck._qqHost + "/" + addr + "?access_token=psyduck";
            var req = UnityWebRequest.Post(url, postData);
            yield return req.SendWebRequest();
            if (req.isHttpError || req.isNetworkError)
            {
                Debug.LogError(req.error + " -> " + url);
                req.Dispose();
                callback?.Invoke("error");
                yield break;
            }
            var text = req.downloadHandler.text;
            req.Dispose();
            callback?.Invoke(text);
        }

        private static void Async(IEnumerator enumerator)
        {
            Psyduck.Async(enumerator);
        }

        public static void Post(string addr, Dictionary<string, string> postData, Action<string> callback)
        {
            Async(_Post(addr, postData, callback));
        }



        public static void GetInfo(string qqNum, Action<QQResult> callback)
        {

            var _data = new Dictionary<string, string>();
            _data.Add("group_id", defaultGroupNum);
            _data.Add("user_id", qqNum);
            Post("get_group_member_info", _data, (content) =>
            {
                if (content == "error")
                {
                    callback?.Invoke(new QQResult(false, "网络异常"));
                }
                else
                {
                    var obj = JsonMapper.ToObject(content);
                    var status = obj.GetString("status");
                    if (status == "ok")
                    {
                        callback?.Invoke(new QQResult(true, obj["data"].GetString("nickname")));
                    }
                    else
                    { 
                        callback?.Invoke(new QQResult(false, "数据错误！"));
                    }
                }
            });
        }
    }

    public class QQResult
    {
        public bool success;
        public string message;

        public QQResult(bool success, string message)
        {
            this.success = success;
            this.message = message;
        }
    }
}
