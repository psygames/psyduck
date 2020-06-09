## 独立 API

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
uid | 用户ID | 登录系统的用户ID |
message | 信息 | 发生错误时的信息 |

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
state | 登录状态 | 当前登录流程下的状态 |
result | 结果 | 结果数据，发生错误时的信息 |

****

###  获取登录二维码

##### URL

` /psyduck/login_get_qrcode `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
uid | 用户ID | 登录系统的用户ID |
message | 消息 | 二维码 URL , 发生错误时的信息 |

****

###  获取短信验证码

##### URL

` /psyduck/login_verify_get `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |
message | 手机号 | 11 位手机号码 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
uid | 用户ID | 登录系统的用户ID |
message | 信息 | 发生错误时的信息 |

****

###  填写手机验证码

##### URL

` /psyduck/login_verify_set `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |
message | 验证码 | 6 位短信验证码 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
uid | 用户ID | 登录系统的用户ID |
message | 信息 | 发生错误时的信息 |

****

###  发起验证账号在线状态请求

##### URL

` /psyduck/validate `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
message | CSDN 账户 | CSDN 账户 ID |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
token | 令牌 | 仅发起请求后，会取得令牌 |
uid | 用户ID | 登录系统的用户ID |
csdn | CSDN 账户 | CSDN 账户 ID |
message | 信息 | 发生错误时的信息 |

****

###  获取验证账号操作状态

##### URL

` /psyduck/validate_get_state `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
uid | 用户ID | 登录系统的用户ID |
token | 令牌 | 令牌 |

##### 响应数据

字段名 | 描述 |  说明  
-|-|-
status | 状态 | 响应状态 ok 或 error |
state | 验证状态 | 当前验证流程下的状态 |
result | 结果 | 结果数据，发生错误时的信息 |

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
message | 账号列表 | 已登录账号列表，发生错误时的信息 |

****

## 通用 API

****

###  通用 API

##### URL

` /psyduck `

##### 请求数据

字段名 | 描述 |  说明  
-|-|-
action | 操作 | 包含全部操作API |
token | 令牌 | 每个操作会分配唯一的Token，使用完毕后失效。 |
uid | 用户ID | 登录系统的用户ID |
message | 发送的消息 | 不同 action 有不同的消息，参考独立的 API。 |

##### 响应数据

不同 action 对应不同响应数据，参考独立的 API。

****
