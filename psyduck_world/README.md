## API

****

###  发起账号登录请求

##### URL

` /psyduck/login `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
token | 令牌 | 仅发起请求后，会取得令牌 |
result | 结果 | 结果数据 或 错误信息 |

****

###  获取登录操作状态

##### URL

` /psyduck/login_get_state `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
state | 登录状态 | 当前操作下的状态 |
result | 结果 | 结果数据 或 错误信息 |

****

##### 状态说明

状态 | 说明  
-|-
request | 刚收到请求，即刚收到 login |
process |  开始处理请求 |
scan | 等待扫码 |
verify_get | 等待输入手机号，获取验证码 |
verify_get_hint | 手机号错误，继续等待，result中包含错误提示 |
verify_set | 等待输入验证码，开始验证 |
verify_set_hint | 验证码错误，继续等待，result中包含错误提示 |
wait_for_done | 等待完成登陆 |
done | 登陆完成 |
fail | 登陆失败，result中包含错误提示 |

****

###  获取短信验证码

##### URL

` /psyduck/login_verify_get `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |
phone | 手机号 | 11 位手机号码 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
result | 结果 | 结果数据 或 错误信息 |

****

###  填写手机验证码

##### URL

` /psyduck/login_verify_set `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |
code | 验证码 | 6 位短信验证码 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
result | 结果 | 结果数据 或 错误信息 |

****

###  更新用户信息请求

##### URL

` /psyduck/update `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
csdn | CSDN 账户 | CSDN 账户 ID |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
token | 令牌 | 仅发起请求后，会取得令牌 |
result | 结果 | 结果数据 或 错误信息 |

****

### 获取更新用户信息操作状态

##### URL

` /psyduck/update_get_state `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
state | 验证状态 | 当前操作下的状态 |
result | 结果 | 结果数据 或 错误信息 |

****

###  下载请求

##### URL

` /psyduck/download `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
csdn | CSDN 账户 | CSDN 账户 ID |
url | CSDN 资源链接 | CSDN 资源链接 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
token | 令牌 | 仅发起请求后，会取得令牌 |
result | 结果 | 结果数据 或 错误信息 |

****

###  获取下载操作状态

##### URL

` /psyduck/download_get_state `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
state | 验证状态 | 当前操作下的状态 |
result | 结果 | 结果数据 或 错误信息 |

****

###  获取已登录的账号列表

##### URL

` /psyduck/user_list `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
result | 结果 | 结果数据 或 错误信息 |

****

###  获取账号下载过的资源列表

##### URL

` /psyduck/user_list `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
csdn | CSDN 账户 | * 空代表所有CSDN账号 |
index | 起始位置 | * 每页最多10条数据 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
result | 结果 | 结果数据 或 错误信息 |

****

###  查询资源资源信息

##### URL

` /psyduck/download_get `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
id | 资源 ID | 可见于下载链接中 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
result | 结果 | 结果数据 或 错误信息 |

****

###  关键字搜索资源信息

##### URL

` /psyduck/download_find `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
keyword | 关键字 | 关键字自动分词处理 |
index | 起始位置 | * 每页最多10条数据 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
result | 结果 | 结果数据 或 错误信息 |
