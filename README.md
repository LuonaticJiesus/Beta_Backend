## 1 数据库



### UserLogin

| 属性名  | 类型      | 限制           |
| ------- | --------- | -------------- |
| user_id | AutoField | 主键           |
| token   | CharField | max_length=200 |



### UserInfo

主键：user_id

| 属性名   | 类型         | 限制                | 说明         |
| -------- | ------------ | ------------------- | ------------ |
| user_id  | AutoField    | 主键                |              |
| name     | CharField    | max_length=200      |              |
| password | CharField    | max_length=200      | 已加密的密码 |
| card_id  | CharField    | max_length=200      | 学号         |
| phone    | CharField    | max_length=20，可空 |              |
| email    | CharField    | max_length=50，可空 | 要求北航邮箱 |
| avatar   | TextField    |                     | 头像url      |
| point    | IntegerField |                     |              |



### EmailPro

| 属性名    | 类型          | 限制                                                         | 说明               |
| --------- | ------------- | ------------------------------------------------------------ | ------------------ |
| code      | CharField     | max_length=20                                                | 验证码             |
| email     | CharField     | max_length=50                                                | 验证邮箱           |
| send_type | CharField     | max_length=50, choices=(('regster', '邮箱注册'), ('forget', '忘记密码')) |                    |
| send_time | DateTimeField | auto_now_add=True                                            | 邮箱验证有生存时间 |
| name      | CharField     | max_length=200                                               |                    |
| password  | CharField     | max_length=50                                                | 已加密的密码       |
| card_id   | CharField     | max_length=200                                               | 学号               |
| phone     | CharField     | max_length=20，可空                                          |                    |
| avatar    | TextField     |                                                              | 头像url            |



### Post

主键：post_id

| 属性名   | 类型          | 限制           |
| -------- | ------------- | -------------- |
| post_id  | AutoField     | 主键           |
| title    | CharField     | max_length=200 |
| user_id  | IntegerField  | 外键           |
| txt      | TextField     |                |
| block_id | IntegerField  | 外键           |
| time     | DateTimeField |                |

帖子Post与发布人user_id和课程模块block相关联



### PostLike

点赞帖子

主键：user_id, post_id

| 属性名  | 类型         |
| ------- | ------------ |
| user_id | IntegerField |
| post_id | IntegerField |



### PostFavor

收藏帖子

主键：user_id, post_id

| 属性名  | 类型         |
| ------- | ------------ |
| user_id | IntegerField |
| post_id | IntegerField |



### PostChosen

主键：post_id, block_id

| 属性名   | 类型         |
| -------- | ------------ |
| post_id  | IntegerField |
| block_id | IntegerField |



### Block

模块

主键：block_id

| 属性名             | 类型          | 限制              | 说明                                                         |
| ------------------ | ------------- | ----------------- | ------------------------------------------------------------ |
| block_id           | AutoField     | 主键              |                                                              |
| name               | CharField     | max_length=200    |                                                              |
| time               | DateTimeField | auto_now_add=True | 模块建立的时间                                               |
| avatar             | TextField     |                   | 模块头像                                                     |
| info               | CharField     | max_length=200    |                                                              |
| approve_permission | IntegerField  |                   | 访问block的权限设置<br /><0: 无需认证，0:需要路人认证，1:成员认证，2:助理认证，3:管理认证，>=4：超管认证 |



### Comment

主键：comment_id

| 属性名          | 类型          | 限制              | 说明                         |
| --------------- | ------------- | ----------------- | ---------------------------- |
| comment_id      | AutoField     | 主键              |                              |
| user_id         | IntegerField  | 外键              | 发表评论的用户id             |
| post_id         | IntegerField  | 外键              | 评论所在帖子id               |
| parent_id       | IntegerField  | 外键、可空        | 评论所回复的父级评论         |
| reply_user_id   | IntegerField  | 外键、可空        | 评论所回复的父级评论的发布者 |
| root_comment_id | IntegerField  | 外键、可空        | 评论所回复的父级评论         |
| txt             | TextField     |                   | 评论内容                     |
| time            | DateTimeField | auto_now_add=True | 帖子发布时间                 |



### CommentLike

主键：user_id, comment_id

| 属性名     | 类型         |
| ---------- | ------------ |
| user_id    | IntegerField |
| comment_id | IntegerField |



### Notice

主键：notice_id

| 属性名    | 类型          | 限制              | 说明             |
| --------- | ------------- | ----------------- | ---------------- |
| notice_id | AutoField     | 主键              |                  |
| title     | CharField     | max_length=200    |                  |
| txt       | TextField     |                   | 通知内容         |
| user_id   | IntegerField  | 外键              | 发布通知的用户id |
| block_id  | IntegerField  | 外键              | 通知所属模块id   |
| time      | DateTimeField | auto_now_add=True | 发布通知的时间   |
| ddl       | DateTimeField |                   | 截止时间         |



### NoticeConfirm

主键：user_id, notice_id

| 属性名    | 类型         |
| --------- | ------------ |
| user_id   | IntegerField |
| notice_id | IntegerField |



### Permission

主键：user_id, block_id

| 属性名     | 类型         | 说明               |
| ---------- | ------------ | ------------------ |
| user_id    | IntegerField | 用户id             |
| block_id   | IntegerField | 用户订阅的模块id   |
| permission | IntegerField | 用户对该模块的权限 |

`permission`说明：

| 权限值permission | 意义              | 赋予的对应block下的操作权限                                  |
| ---------------- | ----------------- | ------------------------------------------------------------ |
| 0                | 订阅该block的路人 | - 查询所有信息<br />- 所有通知的接收、查看和确认<br />- 点赞帖子/评论（==maybe==） |
| 1                | 该block下的成员   | - 查询所有信息<br />- 通知的接收、查看和确认<br />- 发布帖子，发布评论<br />- 删除自己的帖子或评论 |
| 2                | 助教等            | - 查询所有信息<br />- **通知的发布、查看和修改**<br />- 发布帖子，发布评论<br />- 删除任何帖子或评论<br />- **加精帖子** |
| 3                | 管理者            |                                                              |
| 4                | 超级管理员        |                                                              |

### Contribution

主键：user_id, block_id

| 属性名       | 类型         |
| ------------ | ------------ |
| user_id      | IntegerField |
| block_id     | IntegerField |
| contribution | IntegerField |

### Message

| 属性名          | 类型          | 限制                                                         | 说明                                                         |
| --------------- | ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| message_id      | AutoField     | 主键                                                         |                                                              |
| message_type    | IntegerField  | 101,102,103<br />201,202,203,204,205,206,207,208,209<br />301,302,303,304,305<br />401 | 模块更改产生的消息<br />帖子相关产生的消息<br />评论相关产生的消息<br />登录积分增加消息 |
| time            | DateTimeField | auto_now_add=True                                            | 消息产生的时间                                               |
| state           | IntegerField  |                                                              | 消息是否被查收                                               |
| sender_id       | IntegerField  | 外键，可空                                                   | 消息产生的用户id（联表查询用户名、头像等）                   |
| receiver_id     | IntegerField  | 外键                                                         | 接收这条消息的用户id                                         |
| source_id       | IntegerField  | 外键                                                         | 根据message_type，source_id代表block_id、post_id和comment_id其一<br />意义：消息来源的id<br />用于点击**跳转** |
| source_content  | CharField     | max_length=200，可空                                         | 根据message_type，source_content代表block_name、post_title、source_comment_content其一<br />意义：消息来源的内容 |
| related_id      | IntegerField  | 外键                                                         |                                                              |
| related_content | CharField     | max_length=200，可空                                         | 根据message_type，new_content代表“模块有新帖子，请查收”等、“发布帖子，消耗积分。。。“等、被评论的内容等其一 |
| point           | IntegerField  | 可空                                                         |                                                              |



功能表说明：后端传递的数据包含上述各个字段，下表为某些字段的具体内容说明。

| 功能                     | message_type | sender_id                     | ==sender_name== | source_id（跳转）           | source_content                      | related_id                         | related_content | 消息的内容（供参考）                                         |
| ------------------------ | ------------ | ----------------------------- | --------------- | --------------------------- | ----------------------------------- | ---------------------------------- | --------------- | ------------------------------------------------------------ |
| 模块有新帖子             | 101          | block_id                      | block_name      | block_id                    |                                     | post_id                            | post_title      | ”您关注的模块” + **sender_name** + “有新帖发布啦！“ + **related_content** |
| **模块有新通知**         | 102          | block_id                      | block_name      | block_id                    |                                     | notice_id                          | notice_title    | ”您关注的模块”+**sender_name**+“有新通知！“ + **related_content** |
| 模块权限被改变           | 103          |                               | ”系统消息“      | block_id                    | block_name                          | block_id                           |                 | ”您在“+**source_content**+”下的权限已更改“                   |
| 模块被删除               | 104          |                               | ”系统消息“      | block_id                    | block_name                          | block_id                           |                 | ”您关注的模块”+**source_content**+“已被删除“                 |
|                          |              |                               |                 |                             |                                     |                                    |                 |                                                              |
| 贴子发布扣积分           | 201          |                               | ”系统消息“      | post_id                     | post_title                          | post_id                            |                 | ”您发布了一篇帖子，消耗积分“ + **point**                     |
| 帖子被加精               | 202          |                               | “系统消息”      | post_id                     | post_title                          | post_id                            |                 | ”您的帖子”+**source_content**+“被加精了“                     |
| 帖子被加精，加积分       | 203          |                               | ”系统消息“      | post_id                     | post_title                          | post_id                            |                 | ”您的帖子”+**source_content**+“被加精了，积分增加“ + **point** |
| 帖子被取消加精           | 204          |                               | “系统消息”      | post_id                     | post_title                          | post_id                            |                 | ”您的帖子“+**source_content**+被取消加精了，积分减少“ + **point** |
| 帖子被取消加精，扣除积分 | 209          |                               | “系统消息”      | post_id                     | post_title                          | post_id                            |                 | ”您的帖子“+**source_content**+被取消加精了，积分减少“ + **point** |
| 帖子被删除               | 205          |                               | “系统消息”      | post_id                     | post_title                          | post_id                            |                 | ”您的帖子“+**source_content**+”因==不合规==被删除了，详细信息请联系助教/管理员“ |
| 帖子被删除扣除积分       | 206          |                               | “系统消息”      | post_id                     | post_title                          | post_id                            |                 | ”由于您的帖子被删除了，您的积分减少“ + **point**             |
| 帖子被评论               | 207          | user_id<br />评论者           | user_name       | post_id<br />被评论的帖子id | post_title                          | comment_id                         | comment_content | ”您的帖子“ + **source_content** + ”收到一条评论“ + **related_content** |
| 帖子被评论加积分         | 208          |                               | ”系统消息“      | post_id                     | post_title                          | comment_id                         |                 | ”您的帖子“ + **source_content** + ”收到一条评论，积分增加“ + **point** |
|                          |              |                               |                 |                             |                                     |                                    |                 |                                                              |
| 评论发布扣积分           | 301          |                               | ”系统消息“      | post_id<br />评论所在的帖子 | post_title                          | comment_id<br />发布的评论id       |                 | ”您发布了一条评论，消耗积分“ + **point**                     |
| 评论被删除               | 302          |                               | “系统消息”      | post_id<br />评论所在的帖子 | post_title<br />评论所在的帖子title | comment_id<br />被删除的评论id     | comment_content | ”您发表在“ + **source_content** + ”的评论“ + **related_content**+ ”被删除了“ |
| 评论被删除，扣积分       | 303          |                               | ”系统消息“      | post_id<br />评论所在的帖子 | post_title<br />评论所在的帖子title | （comment_id<br />被删除的评论id） |                 | ”您的评论被删除，积分减少“ + **point**                       |
| 评论被评论               | 304          | user_id<br />发布评论的用户id | user_name       | post_id                     | commented_content<br />被评论的内容 | comment_id<br />评论的id           | comment_content | ”您收到了一条评论”+**related_content**                       |
| 评论被评论，加积分       | 305          | user_id<br />发布评论的id     | user_name       | post_id                     | commented_content<br />被评论的内容 | comment_id<br />评论的id           |                 | ”您收到了一条评论，积分增加” + **point**                     |
| 登录加积分               | 401          |                               | “系统消息”      | user_id                     |                                     | user_id                            |                 | ”今日登录，积分增加” + **point**                             |



### File

| 属性名   | 类型         |
| -------- | ------------ |
| obj_id   | IntegerField |
| obj_type | IntegerField |
| obj_url  | TextField    |

## 2 功能函数

### `four_s_block.py`

| 函数名                 | 传入参数                                                     | 功能                                                         | 前置条件（权限等）      | 异常处理                                                     | 接口路由                 | 请求类型 |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------------- | ------------------------------------------------------------ | ------------------------ | -------- |
| block_query_all        |                                                              | 查询所有模块信息                                             |                         |                                                              | `block/queryAll/`        | GET      |
| block_query_permission | user_id(request.META自带) permission[]                       | 根据permission[]数组中的权限限制查找Block。 数组中的权限意义：用户在不同Block中的权限 |                         |                                                              | `block/queryPermission/` | GET      |
| block_info             | block_id                                                     | 查询模块信息                                                 |                         | 模块不存在                                                   | `block/info/`            | GET      |
| block_subscribe        | user_id(request.META自带) block_id subscribe(0:取消订阅)     | subscribe=0:取消订阅 subscribe=1:订阅，`update_perm = 1 if block_perm < 0 else 0` |                         | subscribe范围非[0,1]<br />模块不存在                         | `block/subscribe/`       | POST     |
| block_random           | user_id(request.META自带) number(默认值20)                   | 随机选取['block_id', 'name', 'avatar', 'info']中的一项排序，获取前number个block |                         |                                                              | `block/random/`          | GET      |
| block_search_all       | keyword（关键词）                                            | 按关键词查询所有模块                                         |                         |                                                              | `block/searchAll/`       | GET      |
| block_search_my        | user_id(request.META自带) keyword                            | 在我的模块中按关键词查找模块                                 |                         |                                                              | `block/searchMy/`        | GET      |
| block_modify           | user_id(request.META自带) block_id name avatar info approve_permission | 修改模块的基本数据                                           | 用户在该模块下的权限为4 | 名字不合法<br />头像不合法<br />简介不合法<br />权限不合法<br />模块不存在<br />权限不足 | `block/modify/`          | POST     |
| block_delete           | user_id(request.META自带) block_id                           | 删除模块以及模块下的所有数据（包括通知、分享、贡献度等）     | 用户在该模块下的权限为4 | 模块不存在<br /> 权限不足                                    | `block/delete/`          | POST     |

### `four_s_comment.py`

| 函数名            | 传入参数                                                     | 功能（考虑贡献值）                      | 前置条件（权限等）                               | 异常处理                                                     | 接口路由             | 请求类型 |
| ----------------- | ------------------------------------------------------------ | --------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------ | -------------------- | -------- |
| comment_queryPost | user_id(request.META自带)<br />post_id                       | 查询某个post下的所有的评论              |                                                  | 帖子不存在                                                   | `comment/queryPost/` | GET      |
| comment_publish   | user_id(request.META自带)<br />post_id<br />parent_id<br />txt | 发布评论                                |                                                  | 内容格式错误<br />post不存在<br />parent_id不为空但父级comment不存在<br />父级comment的post_id与当前post_id不一致<br />用户没有在当前block下发布评论的权限<br />**积分不足** | `comment/publish/`   | POST     |
| comment_delete    | user_id(request.META自带)<br />comment_id                    | 删除评论                                | - 删除自己的评论<br />- 删除他人的评论，perm >=2 | 评论不存在<br />删除他人评论时，权限不足(pem<2)<br />~可删除自己发布的评论~ | `comment/delete/`    | POST     |
| comment_like      | user_id(request.META自带)<br />comment_id<br />like(0:取消点赞) | like=0:取消点赞<br />like!=0:点赞<br /> |                                                  | 评论不存在<br />                                             | `comment/like/`      | POST     |



### `four_s_notice.py`

| 函数名             | 传入参数                                                     | 功能（考虑贡献值）                                        | 前置条件（权限等）                      | 异常处理                                                     | 接口路由             | 请求类型 |
| ------------------ | ------------------------------------------------------------ | --------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------ | -------------------- | -------- |
| notice_query_recv  | show_confirm( 0:未"确认收到"的通知; 1:所有通知) <br />undue_op( 0:所有通知;  1:未截止通知;  -1:已截止通知) | 查询收到的(所有；未截止；已截止）(所有; 未确认)的通知信息 |                                         | show_confirm与undue_op参数范围错误                           | `notice/queryRecv/`  | GET      |
| notice_query_send  | user_id                                                      | 查询用户发送的所有通知，按时间排序                        |                                         | 用户不存在                                                   | `notice/querySend/`  | GET      |
| notice_query_by_id | notice_id                                                    | 查询notice_id的通知                                       |                                         | 通知不存在                                                   | `notice/queryById/`  | GET      |
| notice_query_block | block_id                                                     | 查询block下的所有通知，按时间排序                         |                                         | 模块不存在                                                   | `notice/queryBlock/` | GET      |
| notice_publish     | title <br />txt <br />block_id <br />ddl                     | 发布通知                                                  | 用户权限>=2                             | 标题格式错误<br /> 内容格式错误 <br />截止日期格式错误<br />权限不够<br />截止时间错误 | `notice/publish/`    | POST     |
| notice_confirm     | notice_id                                                    | 确认或取消确认收到的通知                                  | 用户权限>=1                             | 通知不存在<br />未订阅模块                                   | `notice/confirm/`    | POST     |
| notice_delete      | user_id(request.META自带) notice_id                          | 删除通知                                                  | 用户权限perm>=2且删除的是自己发布的通知 | 权限不足:不是该用户发布的通知                                | `notice/delete/`     | POST     |

### `four_s_message.py`

| 函数名              | 传入参数                                              | 功能（考虑贡献值）                     | 前置条件（权限等） | 异常处理        | 接口路由              | 请求类型 |
| ------------------- | ----------------------------------------------------- | -------------------------------------- | ------------------ | --------------- | --------------------- | -------- |
| message_query_rec   | user_id(request.META自带)                             | 查询登录用户的所有信息                 | 用户已登录         |                 | `message/queryRec/`   | GET      |
| message_confirm_all | user_id(request.META自带)                             | 所有消息设置为已读                     | 用户已登录         |                 | `message/confirmAll/` | POST     |
| message_confirm     | user_id(request.META自带)<br />message_ids<br />state | 改变一组message的message.status为state | 用户已登录         | 状态码state错误 | `message/confirm/`    | POST     |



### `four_s_permission.py`

| 函数名                | 传入参数                                                     | 功能（考虑贡献值）                               | 异常处理                                                  | 接口路由                | 请求类型 |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------ | --------------------------------------------------------- | ----------------------- | -------- |
| permission_query_user | block_id<br />permission                                     | 查询权限等于permission的block_id下的所有用户信息 | permission参数错误                                        | `permission/queryUser/` | GET      |
| permission_query      | user_id<br />block_id                                        |                                                  |                                                           | `permission/query/`     | GET      |
| permission_set        | userid(request.META自带)<br />user_id<br />block_id<br />permission | 设置user_id对应的用户的权限值                    | 权限错误permission ![0,1,2,3,4]<br />权限设置者的权限不足 | `permission/set/`       | POST     |



### `four_s_post.py`

帖子加精的问题：直接在Post里面加一个属性chosen，加精为1，非加精为0

| 函数名                | 传入参数                                                     | 功能（考虑贡献值）                             | 前置条件（权限等）                          | 异常处理                   | 接口路由               | 请求类型 |
| --------------------- | ------------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------- | -------------------------- | ---------------------- | -------- |
| post_query_title      | title                                                        | 根据title查找post                              |                                             |                            | `post/queryTitle/`     | GET      |
| post_query_by_id      | post_id                                                      | 根据post_id查找post                            |                                             | 帖子不存在                 | `post/queryByID/`      | GET      |
| post_query_block      | block_id                                                     | 查询block下发布的所有帖子                      |                                             | 模块不存在                 | `post/queryBlock/`     | GET      |
| post_query_user_block | user_id<br />block_id                                        | 查询user在block下发布的所有帖子                |                                             | 模块不存在                 | `post/queryUserBlock/` | GET      |
| post_query_user       | user_id                                                      | 查询用户发布的帖子                             |                                             | 用户不存在                 | `post/queryUser/`      | GET      |
| post_query_chosen     | block_id                                                     | 查询block下的加精帖子                          |                                             | 模块不存在                 | `post/queryChosen/`    | GET      |
| post_detail           | post_id                                                      | 查询帖子详细内容                               |                                             | 帖子不存在                 | `post/detail/`         | GET      |
| post_publish          | title <br />txt<br />block_id                                | 发布帖子                                       | 用户在当前block下的权限>=1                  | 权限不足 <br />积分不足    | `post/publish/`        | POST     |
| post_modify           | post_id<br />title<br />txt                                  | 修改帖子内容                                   | 只允许用户修改自己发布的帖子                |                            | `post/modify/`         |          |
| post_delete           | user_id(request.META自带) <br />post_id                      | 删除帖子，级联删除评论、加精、收藏、点赞的信息 | - 删除自己发布的帖子 - 删除他人帖子:perm>=2 | 权限不足                   | `post/publish/`        | POST     |
| post_like             | user_id(request.META自带) <br />post_id like(0:取消点赞,1:点赞) | 点赞或取消点赞帖子                             | 用户在帖子所在的block下的perm>=1            | 权限不足<br />帖子不存在   | `post/delete/`         | POST     |
| post_choose           | user_id(request.META自带) <br />post_id chosen(0:取消加精,非0:加精) | 加精或取消加精帖子                             | 用户在帖子所在的block下的perm>=2            | 帖子不存在<br />未订阅模块 | `post/like/`           | POST     |
| post_favor            | user_id(request.META自带) <br />post_id                      | 收藏或取消收藏帖子                             |                                             | 帖子不存在<br />未订阅模块 | `post/favor/`          | POST     |
| post_query_favor      | user_id(request.META自带) <br />                             | 查看当前收藏的所有帖子                         |                                             |                            | `post/queryFavor/`     | GET      |

### `four_s_user.py`

| 函数名          | 传入参数                                                     | 功能（考虑贡献值）               | 异常处理                                                     | 接口路由          | 请求类型 |
| --------------- | ------------------------------------------------------------ | -------------------------------- | ------------------------------------------------------------ | ----------------- | -------- |
| user_signup     | username <br />password <br />card_id<br />phone(可空)<br /> email | 用户注册，向注册邮箱发送认证链接 | 用户名为空<br />密码为空<br /> 用户名已存在 <br />学号已存在 <br />邮箱已注册 | `user/signup/`    | POST     |
| active_email    | active_code                                                  | 邮箱认证，注册成功               | 验证码错误<br />验证超时                                     | `user/active/`    | GET      |
| user_login      | username <br />password                                      |                                  | 用户名不存在<br />密码错误                                   | `user/login/`     | POST     |
| user_info       | user_id                                                      | 查询user_id 的名字和头像         | 用户不存在                                                   | `user/info/`      | POST     |
| user_my_info    |                                                              | 查询个人所有信息                 |                                                              | `user/myInfo/`    | POST     |
| user_modify     | card_id <br />phone <br />email <br />avatar                 | 根据提供的非空参数更新用户信息   | 学工卡格式错误<br />手机格式错误<br />邮箱格式错误<br />头像格式错误 | `user/modify/`    | POST     |
| user_change_pwd | old_password                                                 |                                  | 用户不存在 旧密码错误                                        | `user/changePwd/` | POST     |
| user_public_key |                                                              | 获取加密公钥                     |                                                              | `user/publicKey/` | GET      |



### `four_s_file.py`

| 函数名       | 传入参数                   | 功能                                 | 异常处理                                                     | 接口路由        | 请求类型 |
| ------------ | -------------------------- | ------------------------------------ | ------------------------------------------------------------ | --------------- | -------- |
| file_upload  | FILES.get('file')          | 上传文件                             | 文件大小不符                                                 | `file/upload/`  | POST     |
| file_connect | type<br/>id<br/>url_list[] | 将附件关联到模块、帖子或通知         | obj_type=1但是帖子不存在<br />obj_type=2但是通知不存在<br />obj_type=3但是模块不存在<br /> | `file/connect/` | POST     |
| file_list    | obj_type<br/>obj_id        | 获取模块、帖子或通知所关联的附件列表 |                                                              | `file/list/`    | GET      |



### `four_s_stat.py`

| 函数名          | 传入参数 | 功能                                                         | 接口路由                | 请求类型 |
| --------------- | -------- | ------------------------------------------------------------ | ----------------------- | -------- |
| stat_post_time  | state    | state=1查询近一年的发帖数，按月计<br />state=2查询近七天的发帖数，按天计 | `statistic/post-time`   | GET      |
| stat_post_block |          | 查询发布帖子在模块中的分布情况                               | `statistic/post-module` | GET      |
