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

        LoginAction loginAction = null;
        Texture2D loginQR = null;
        private void OnGUI()
        {
            var uid = "admin";
            var csdn = "y85171642";

            if (GUILayout.Button("UserList"))
            {
                var u = new CommonAction();
                u.UserList(uid, (obj) =>
                {
                    Debug.Log(obj.userInfos[0].csdnDetail.nickname);
                });
            }

            if (GUILayout.Button("DownloadGet"))
            {
                var u = new CommonAction();
                u.DownloadGet("5265765", (obj) =>
                {
                    Debug.Log(obj.info.shareUrl);
                });
            }

            if (GUILayout.Button("DownloadFind"))
            {
                var u = new CommonAction();
                u.DownloadFind(uid, "test", 0, (obj) =>
                 {
                     Debug.Log(obj.downloadInfos[0].shareUrl);
                 });
            }

            var url = "https://download.csdn.net/download/y85171642/5265765";
            if (GUILayout.Button("Download"))
            {
                var a = new DownloadAction();
                a.onBegin += (token) =>
                {
                    Debug.Log(token.token);
                };

                a.onError += (error) =>
                {
                    Debug.Log(error.errorMsg);
                };

                a.onProcess += (state) =>
                {
                    Debug.Log(state.state);
                };

                a.onFinish += (done) =>
                {
                    Debug.Log(done.info.shareUrl);
                };

                a.Download(uid, csdn, url);
            }

            if (GUILayout.Button("Login"))
            {
                loginAction = new LoginAction();
                loginAction.onBegin += (token) =>
                {
                    Debug.Log(token.token);
                };

                loginAction.onError += (error) =>
                {
                    Debug.Log(error.errorMsg);
                };

                loginAction.onProcess += (state) =>
                {
                    Debug.Log(state.state);
                };

                loginAction.onFinish += (done) =>
                {
                    Debug.Log(done.info.csdnDetail.nickname);
                };

                loginAction.Login(uid);
            }
        }
    }
}
