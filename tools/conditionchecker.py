import sched
import time

# 非主要文件
# 一种实现周期性检查condition的方案
# 此处trigger与condition的名词定义模糊

class ConditionChecker:
    def __init__(self, condition_func, interval_sec):
        self.condition_func = condition_func
        self.interval_sec = interval_sec
        self.trigger_started = False
        self.s = sched.scheduler(time.time, time.sleep)

    def start(self, trigger_func):
        if not self.trigger_started:
            self.trigger_started = True
            self.check_event = self.s.enter(self.interval_sec, 1, self.check_condition, (trigger_func,))
            self.s.run()

    def stop(self):
        if self.trigger_started:
            self.s.cancel(self.check_event)
            self.trigger_started = False

    def check_condition(self, trigger_func):
        if self.condition_func():
            trigger_func()
        self.s.enter(self.interval_sec, 1, self.check_condition, (trigger_func,))