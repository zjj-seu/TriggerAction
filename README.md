# TriggerAction

my implement of Trigger Action service  

## 功能概览

> if (trigger)(condition)
> then (action)
>
> 在具体的应用场景中，trigger通常表示一个触发条件，比如时间触发、用户操作触发或者消息通知触发等。condition表示一个补充的条件，用于限制trigger的范围或者进一步检查trigger的有效性。action表示一个具体的操作，可以是一个函数调用、一个系统命令或者一个消息发送等。
>
> - trigger:主动检查的状态
> - condition：被动检查的状态，或者是操作触发器关闭开启节约资源
> - action：执行的操作

## 实现流程

> 读取与修改xml文件中的事件
>
> - xml文件的树型组织方式
> - xml文件的事件语言
> - xml文件的读取与写入，内存中存在的形式
> - xml文件的规则修改更新
> - 事件读取后生成对应线程
>
> 生成对应的线程
>
> - 状态线程用于存储并监控各IoT设备的状态参数
> - 执行线程用于调用IoT控制API来执行相关操作
> - 执行线程和状态线程通过线程通信手段，执行线程不直接操作数据文件。
> - Trigger存于执行线程中，周期性检查condition，周期性检查触发事件。如何通信，方式与形式
>
