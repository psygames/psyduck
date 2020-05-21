package com.cjy.csdn.system.security;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.springframework.security.web.session.SessionInformationExpiredEvent;
import org.springframework.security.web.session.SessionInformationExpiredStrategy;

import com.fasterxml.jackson.databind.ObjectMapper;

public class CustomExpiredSessionStrategy implements SessionInformationExpiredStrategy {
    private ObjectMapper objectMapper = new ObjectMapper();
    //private RedirectStrategy redirectStrategy = new DefaultRedirectStrategy();

    @Override
    public void onExpiredSessionDetected(SessionInformationExpiredEvent event) throws IOException {
        Map<String, Object> map = new HashMap<>(16);
        map.put("code", 0);
        map.put("msg", "您的账号在另一台机器登录，您被迫下线。".concat(event.getSessionInformation().getLastRequest().toString()));
        // Map -> Json
        String json = objectMapper.writeValueAsString(map);
        
        //直接在页面打印json数据
        event.getResponse().setContentType("application/json;charset=UTF-8");
        event.getResponse().getWriter().write(json);

        // 如果是跳转html页面，url代表跳转的地址，跳转到 session过期提示页面
        //redirectStrategy.sendRedirect(event.getRequest(), event.getResponse(), "/login/invalid");
    }
}

