using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Psyduck
{
    public class LoginResult : Result
    {
        public CsdnDetail info;

        protected override void ParseResult()
        {
            base.ParseResult();

            info = new CsdnDetail();
            info.Parse(jsonResult);
        }
    }
}
