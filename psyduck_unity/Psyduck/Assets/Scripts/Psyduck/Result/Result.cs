using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace psyduck.api
{
    public class Result
    {
        public Status status;
        public string errorMsg;
        public JsonData jsonResult;

        public virtual void Parse(JsonData jsonData)
        {
            this.status = jsonData.GetString("status") == "ok" ? Status.OK : Status.Error;
            this.jsonResult = jsonData.Get("result");
            this.errorMsg = this.status == Status.Error ? (string)jsonResult : "";
            if (this.status == Status.OK)
            {
                ParseResult();
            }
        }

        protected virtual void ParseResult()
        {

        }
    }
}
