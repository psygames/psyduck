using System;
using System.Collections.Generic;
using LitJson;

namespace Psyduck
{
    public class LoginAction : ActionBase
    {
        private string uid = "";
        private string token = "";

        public event Action<TokenResult> onBegin;
        public event Action<LoginStateResult> onProcess;
        public event Action<LoginResult> onFinish;
        public event Action<Result> onError;

        public void Login(string uid)
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
            Post("login", postData, (content) =>
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

        public void VerifyGet(string phone)
        {
            if (!isBusy)
                return;

            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            postData["token"] = token;
            postData["phone"] = phone;
            Post("login_verify_get", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var res = new Result();
                res.Parse(obj);
                if (res.isOK)
                {
                    // todo:
                }
                else
                {
                    onError?.Invoke(res);
                }
            });
        }

        public void VerifySet(string code)
        {
            if (!isBusy)
                return;

            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            postData["token"] = token;
            postData["code"] = code;
            Post("login_verify_set", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var res = new Result();
                res.Parse(obj);
                if (res.isOK)
                {
                    // todo:
                }
                else
                {
                    onError?.Invoke(res);
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
            IntervalPost("login_get_state", postData, (_content) =>
            {
                var _obj = JsonMapper.ToObject(_content);
                var state = new LoginStateResult();
                state.Parse(_obj);
                if (state.isOK)
                {
                    onProcess?.Invoke(state);
                    if (state.isDone)
                    {
                        var done = new LoginResult();
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
