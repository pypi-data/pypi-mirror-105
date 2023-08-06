from kpl_helper.base import get_config, _APIBase


class StopTask(_APIBase):
    def stop(self):
        if not get_config().get_inner():
            return
        self.post("/task/stop", json={"task_id": get_config().get_task_id()})


def kill():
    StopTask().stop()
