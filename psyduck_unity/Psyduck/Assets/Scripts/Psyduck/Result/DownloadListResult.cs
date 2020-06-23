using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Psyduck
{
    public class DownloadListResult : Result
    {
        public DownloadInfo[] downloadInfos;

        protected override void ParseResult()
        {
            base.ParseResult();

            downloadInfos = new DownloadInfo[jsonResult.Count];
            for (int i = 0; i < jsonResult.Count; i++)
            {
                downloadInfos[i] = new DownloadInfo();
                downloadInfos[i].Parse(jsonResult[i]);
            }
        }
    }
}
