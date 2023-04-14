# TriggerAction

my implement of Trigger Action service  

## 本科毕设代码库，持续更新中  

## 目前完成的功能  

- 成功学会github啦
- 米家设备信息和令牌的局域网获取与控制
- 博联设备的抓包控制和api控制的方法确定
- xml文件的创建与读写管理
- 米家设备的信息规格化处理
- 正在编写米家设备信息的自动化存取  

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
> - xml文件的树型组织方式(demo)
> - xml文件的事件语言(demo)
> - xml文件的读取与写入，内存中存在的形式(已)
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

## 多线程处理的一种方案

1.通信手段：队列变量

        import threading
        import queue# 线程 A：从队列中获取数据，并输出
        def thread_a(q):
            while True:
                data = q.get()
                if data is None:
                    break
                print('Thread A:', data)

        def thread_b(q):
            for i in range(10):
                q.put(i)
            q.put(None)  # 结束标记

        q = queue.Queue()
        t1 = threading.Thread(target=thread_a, args=(q,))
        t2 = threading.Thread(target=thread_b, args=(q,))
        t1.start()
        t2.start()

        t1.join()
        t2.join()
2.组织结构
>
> 1.任务分配线程
>
> - 根据从xml文件中读取到的事件集合，解析事件类型，规划各类线程，并布置好通信通道（队列）
> - 启动IoT设备监听线程，监听设备的各种状态（可优化至事件指定状态监听，节约资源，或者分开监听，频率不同）
> - 启动事件更新线程，相应用户的修改操作。
> - 启动相应的执行线程，执行线程需要同步至事件状态，包括事件激活状态等。
>
> 2.IoT设备监听线程
>
> - 根据xml设备文件获取历史设备，调用底层API获得当前局域网在线设备
> - 更新当前在线设备的状态，供有效触发器监听线程查询
> - 更新历史设备xml文件（只新增不删除）
>
> 3.有效触发器监听线程
>
> - 执行线程组唤起的监听线程，监听受关注的IoT设备的特定状态，用于触发事件执行
> - 受制于事件的激活状态（status）、conditions条件组、trigger组件的合法性检查来生存
> - 用于节省资源，但会加大开发难度，待定
>
> 4.执行线程
>
> - 调用底层IoT控制接口来执行相关操作
> - 由有效触发器监听线程唤起，同时传入执行参数组（actions组），解析执行
> - 对事件的action组字典具有解析功能，尽量增加通用性（不同设备，不同操作的同一调用）
> - 可增加执行命令comand，等待父线程的执行信号执行，而actions参数组解析和接口调用的布置可以实现安排好，增加响应速度。
