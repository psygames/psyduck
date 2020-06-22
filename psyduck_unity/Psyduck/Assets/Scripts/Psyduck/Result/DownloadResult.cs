using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Psyduck
{
    public class DownloadResult : Result
    {
        public DownloadInfo info;

        protected override void ParseResult()
        {
            base.ParseResult();

            info = new DownloadInfo();
            info.Parse(jsonResult);
        }
    }

    public class DownloadInfo
    {
        public string id;
        public string uid;
        public string csdn;
        public string shareUrl;
        public ResDetail resDetail;
        public DateTime createTime;

        public void Parse(JsonData jsonData)
        {
            id = jsonData.GetString("id");
            shareUrl = jsonData.GetString("share_url");
            resDetail = new ResDetail();
            resDetail.Parse(jsonData["info"]);
            createTime = jsonData.GetDateTime("create_time");
        }
    }

    public class ResDetail
    {
        public string url;
        public string title;
        public string type;
        public string size;
        public string description;
        public string filename;
        public int point;
        public int star;
        public DateTime uploadTime;
        public string uploader;

        public void Parse(JsonData jsonData)
        {
            url = jsonData.GetString("url");
            title = jsonData.GetString("title");
            type = jsonData.GetString("type");
            size = jsonData.GetString("size");
            description = jsonData.GetString("description");
            filename = jsonData.GetString("filename");
            description = jsonData.GetString("description");
            point = jsonData.GetInt("point");
            star = jsonData.GetInt("star");
            uploadTime = jsonData.GetDateTime("upload_time");
            uploader = jsonData.GetString("uploader");
        }
    }
}
