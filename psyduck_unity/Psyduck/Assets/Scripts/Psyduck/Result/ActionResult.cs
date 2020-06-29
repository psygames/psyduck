using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Psyduck
{
    public class RecoverActionResult : Result
    {
        public ActionInfo[] actionInfos;

        protected override void ParseResult()
        {
            base.ParseResult();

            actionInfos = new ActionInfo[jsonResult.Count];
            for (int i = 0; i < jsonResult.Count; i++)
            {
                actionInfos[i] = new ActionInfo();
                actionInfos[i].Parse(jsonResult[i]);
            }
        }
    }


    public class ActionInfo
    {
        public string action;
        public string token;
        public string state;

        public void Parse(JsonData jsonData)
        {
            action = jsonData.GetString("action");
            token = jsonData.GetString("token");
            state = jsonData.GetString("state");
        }
    }
}
