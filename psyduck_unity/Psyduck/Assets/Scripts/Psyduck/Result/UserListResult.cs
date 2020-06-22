using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace psyduck.api
{
    public class UserListResult : Result
    {
        public UserInfo[] userInfos;

        protected override void ParseResult()
        {
            base.ParseResult();

            userInfos = new UserInfo[jsonResult.Count];
            for (int i = 0; i < jsonResult.Count; i++)
            {
                userInfos[i] = new UserInfo();
                userInfos[i].Parse(jsonResult[i]);
            }
        }
    }

    public class UserInfo
    {
        public string uid;
        public string csdn;
        public string state;
        public CsdnDetail csdnDetail;
        public DateTime updateTime;

        public void Parse(JsonData jsonData)
        {
            uid = jsonData.GetString("uid");
            csdn = jsonData.GetString("csdn");
            state = jsonData.GetString("state");
            csdnDetail = new CsdnDetail();
            csdnDetail.Parse(jsonData["info"]);
            updateTime = jsonData.GetDateTime("update_time");
        }
    }

    public class CsdnDetail
    {
        public string nickname;
        public int point;
        public int coin;
        public string head;
        public CsdnVipInfo vip;

        public void Parse(JsonData jsonData)
        {
            nickname = jsonData.GetString("nickname");
            point = jsonData.GetInt("point");
            coin = jsonData.GetInt("coin");
            head = jsonData.GetString("head");
            vip = new CsdnVipInfo();
            vip.Parse(jsonData["vip"]);
        }
    }

    public class CsdnVipInfo
    {
        public bool isVip;
        public int count;
        public DateTime date;

        public void Parse(JsonData jsonData)
        {
            isVip = jsonData.GetBool("is_vip");
            count = jsonData.GetInt("count");
            date = jsonData.GetDateTime("date");
        }
    }

}
