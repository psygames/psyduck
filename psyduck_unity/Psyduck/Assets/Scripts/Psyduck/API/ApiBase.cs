using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using LitJson;

namespace Psyduck
{
    public class ApiBase
    {
        protected IEnumerator _Post(string addr, Dictionary<string, string> postData, Action<string> callback)
        {
            var url = Psyduck._host + "/" + addr;
            var req = UnityWebRequest.Post(url, postData);
            yield return req.SendWebRequest();
            if (req.isHttpError || req.isNetworkError)
            {
                Debug.LogError(req.error + " -> " + url);
                yield break;
            }

            callback?.Invoke(req.downloadHandler.text);
        }

        protected void Async(IEnumerator enumerator)
        {
            Psyduck.Async(enumerator);
        }


        public IEnumerator _Download(string uid, string csdn, string url,
            Action<StateResult> stateCallback,
            Action<DownloadResult> doneCallback,
            Action<Result> errorCallback)
        {
            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            postData["csdn"] = csdn;
            postData["url"] = url;
            bool isOver = false;
            TokenResult token = null;
            yield return _Post("download", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                token = new TokenResult();
                token.Parse(obj);
                if (token.status == Status.Error)
                {
                    isOver = true;
                    errorCallback?.Invoke(token);
                }
            });

            if (isOver)
            {
                yield break;
            }

            postData.Clear();
            postData["uid"] = uid;
            postData["token"] = token.token;
            for (int i = 0; i < 3600 && !isOver; i++)
            {
                yield return _Post("download_get_state", postData, (_content) =>
                {
                    var _obj = JsonMapper.ToObject(_content);
                    var state = new StateResult();
                    state.Parse(_obj);
                    if (state.isFail)
                    {
                        errorCallback?.Invoke(token);
                        isOver = true;
                    }
                    else if (state.isDone)
                    {
                        var done = new DownloadResult();
                        done.Parse(_obj);
                        doneCallback?.Invoke(done);
                        isOver = true;
                    }
                    else
                    {
                        stateCallback.Invoke(state);
                    }
                });
            }
        }

        public void Download(string uid, string csdn, string url,
          Action<StateResult> stateCallback,
          Action<DownloadResult> doneCallback,
          Action<Result> errorCallback)
        {
            Async(_Download(uid, csdn, url, stateCallback, doneCallback, errorCallback));
        }

        public void Download(string uid, string url,
        Action<StateResult> stateCallback,
        Action<DownloadResult> doneCallback,
        Action<Result> errorCallback)
        {
            Download(uid, "", url, stateCallback, doneCallback, errorCallback);
        }


        private void OnGUI()
        {
            var uid = "admin";
            var csdn = "y85171642";

            if (GUILayout.Button("UserList"))
            {
                UserList("admin", (obj) =>
                {
                    Debug.LogError(obj.userInfos[0].updateTime);
                });
            }

            var url = "https://download.csdn.net/download/y85171642/5265765";
            if (GUILayout.Button("Download"))
            {
                Download(uid, csdn, url,
                (state) =>
                {
                    Debug.Log(state.state);
                },
                (done) =>
                {
                    Debug.Log(done.info.shareUrl);
                },
                (error) =>
                {
                    Debug.Log(error.errorMsg);
                });
            }
        }
    }

}