using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Psyduck
{
    public class TokenResult : Result
    {
        public string token;

        public override void Parse(JsonData jsonData)
        {
            this.status = jsonData.GetString("status") == "ok" ? Status.OK : Status.Error;
            this.token = jsonData.GetString("token");
            this.jsonResult = jsonData.Get("result");
            this.errorMsg = this.status == Status.Error ? (string)jsonResult : "";
        }
    }
}
