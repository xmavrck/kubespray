from __future__ import absolute_import
from ansible.plugins.callback import CallbackBase
import json

class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'json_cb'

    def __init__(self):
        self.tasks = {}
        self.stats = {}

    def dump_result(self, result, ignore_errors=True):
    	countes = 0
    	self.custom_result = dict(name=self.tasks[result._task._uuid],result=result._result, host=result._host.get_name())
        ranges = self.custom_result["result"].get("results")
        for count in ranges:
        	if count["failed"] != False:
        		countes += 1
        self.custom_result["failures"] = countes
        if self.custom_result['failures'] > 0:
    		self.custom_result["failures"] = True
    	else:
    		self.custom_result["failures"] = False
        print (json.dumps(self.custom_result))

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.tasks[task._uuid] = task.name

    v2_runner_on_ok = dump_result
    v2_runner_on_failed = dump_result
    v2_runner_on_unreachable = dump_result
    v2_runner_on_skipped = dump_result

