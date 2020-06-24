using UnityEngine;
using System.Collections;
using System.Runtime.InteropServices;
using System.Net.NetworkInformation;

using System.Net.Sockets;
using System;
public class DeviceID
{
    private string _uuid = "";

    private static DeviceID s_instance;

    public static DeviceID Instance
    {
        get
        {
            if (s_instance == null)
                s_instance = new DeviceID();
            return s_instance;
        }
    }

    private DeviceID()
    {
        _uuid = SystemInfo.deviceUniqueIdentifier;
    }

    public static string UUID
    {
        get
        {
            if (s_instance == null)
            {
                s_instance = new DeviceID();
            }
            return s_instance._uuid;
        }
    }
}
