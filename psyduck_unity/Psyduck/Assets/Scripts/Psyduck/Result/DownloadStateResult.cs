using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Psyduck
{
    public class DownloadStateResult : StateResult
    {
        public bool isDownloading { get { return step == "downloading"; } }
        public bool isUploading { get { return step == "uploading"; } }

        public string step
        {
            get
            {
                if (jsonResult == null || !jsonResult.Has("step"))
                    return "";
                return jsonResult.GetString("step");
            }
        }

        public long nowSize
        {
            get
            {
                if (jsonResult == null
                    || !jsonResult.Has("progress")
                    || !jsonResult.Get("progress").Has("now_size"))
                    return 0;
                return jsonResult.Get("progress").GetLong("now_size");
            }
        }

        public long totalSize
        {
            get
            {
                if (jsonResult == null
                    || !jsonResult.Has("progress")
                    || !jsonResult.Get("progress").Has("total_size"))
                    return 0;
                return jsonResult.Get("progress").GetLong("total_size");
            }
        }

        public float progress { get { return 1f * nowSize / totalSize; } }
    }
}
