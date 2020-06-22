using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Psyduck
{
    public class ApiUser : ApiBase
    {
        public void List(string uid, Action<UserListResult> callback)
        {
            var postData = new Dictionary<string, string>();
            postData["uid"] = uid;
            Async(_Post("user_list", postData, (content) =>
            {
                var obj = JsonMapper.ToObject(content);
                var res = new UserListResult();
                res.Parse(obj);
                callback?.Invoke(res);
            }));
        }
    }
}
