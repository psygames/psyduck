using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using LitJson;

namespace Psyduck
{
    public class DownloadAction : ActionBase
    {
        private string uid = "";
        private string token = "";

        public event Action<TokenResult> onBegin;
        public event Action<DownloadStateResult> onProcess;
        public event Action<DownloadResult> onFinish;
        public event Action<Result> onError;

        public void Download(string uid, string csdn, string url)
        {
            if (this.isBusy)
            {
                return;
            }

            this.isBusy = true;
            this.uid = uid;
            this.token = "";

            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            postData["csdn"] = csdn;
            postData["url"] = url;
            Post("download", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var token = new TokenResult();
                token.Parse(obj);
                if (token.isOK)
                {
                    this.token = token.token;
                    onBegin?.Invoke(token);
                    StateLoop();
                }
                else
                {
                    onError?.Invoke(token);
                }
            });
        }

        bool isStateOver = false;
        private void _Over()
        {
            isStateOver = true;
            isBusy = false;
        }

        private void StateLoop()
        {
            isStateOver = false;
            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            postData["token"] = token;
            IntervalPost("download_get_state", postData, (_content) =>
            {
                var _obj = JsonMapper.ToObject(_content);
                var state = new DownloadStateResult();
                state.Parse(_obj);
                if (state.isOK)
                {
                    onProcess?.Invoke(state);
                    if (state.isDone)
                    {
                        var done = new DownloadResult();
                        done.Parse(_obj);
                        onFinish?.Invoke(done);
                        _Over();
                    }
                    else if (state.isFail)
                    {
                        onError?.Invoke(state);
                        _Over();
                    }
                }
                else
                {
                    onError?.Invoke(state);
                    _Over();
                }
            }, 1, () => { return !isStateOver; }, 3600);
        }
    }
}
