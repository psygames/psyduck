using LitJson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace psyduck.api
{
    public static class JsonDataExtention
    {
        public static bool Has(this JsonData jsonData, string key)
        {
            return jsonData.ContainsKey(key);
        }

        public static JsonData Get(this JsonData jsonData, string key)
        {
            if (jsonData.Has(key))
                return jsonData[key];
            return null;
        }

        public static bool GetBool(this JsonData jsonData, string key)
        {
            if (jsonData.Has(key))
                return bool.Parse(jsonData[key].ToString());
            return false;
        }

        public static int GetInt(this JsonData jsonData, string key)
        {
            if (jsonData.Has(key))
                return int.Parse(jsonData[key].ToString());
            return 0;
        }

        public static string GetString(this JsonData jsonData, string key)
        {
            if (jsonData.Has(key))
                return jsonData[key].ToString();
            return "";
        }

        public static DateTime GetDateTime(this JsonData jsonData, string key)
        {
            if (jsonData.Has(key))
                return DateTime.Parse(jsonData[key].ToString());
            return DateTime.MinValue;
        }
    }
}
