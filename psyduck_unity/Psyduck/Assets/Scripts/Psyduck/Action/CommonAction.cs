using System;
using System.Collections.Generic;
using LitJson;

namespace Psyduck
{
    public class CommonAction : ActionBase
    {
        public void UserList(string uid, Action<UserListResult> callback)
        {
            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            Post("user_list", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var res = new UserListResult();
                res.Parse(obj);
                callback?.Invoke(res);
            });
        }

        public void DownloadList(string uid, string csdn, int index, Action<DownloadListResult> callback)
        {
            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            postData["csdn"] = csdn;
            postData["index"] = index.ToString();
            Post("download_list", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var res = new DownloadListResult();
                res.Parse(obj);
                callback?.Invoke(res);
            });
        }

        public void DownloadList(string uid, int index, Action<DownloadListResult> callback)
        {
            DownloadList(uid, "", index, callback);
        }

        public void DownloadFind(string uid,string keyword, int index, Action<DownloadListResult> callback)
        {
            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            postData["keyword"] = keyword;
            postData["index"] = index.ToString();
            Post("download_find", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var res = new DownloadListResult();
                res.Parse(obj);
                callback?.Invoke(res);
            });
        }

        public void DownloadGet(string id, Action<DownloadResult> callback)
        {
            var postData = new Dictionary<string, string>();
            postData["id"] = id;
            Post("download_get", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var res = new DownloadResult();
                res.Parse(obj);
                callback?.Invoke(res);
            });
        }

        public void RecoverAction(string uid, Action<RecoverActionResult> callback)
        {
            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            Post("recover_action", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var res = new RecoverActionResult();
                res.Parse(obj);
                callback?.Invoke(res);
            });
        }
    }
}
