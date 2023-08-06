from kpl_helper.base import logger, get_config, _APIBase


class Metric(_APIBase):
    def send_progress(self, progress):
        if not get_config().get_inner():
            return
        if not (0.0 <= progress <= 1.0):
            logger.warning("Progress should be in range [0.0, 1.0]. but get `{}`".format(progress))
            if progress < 0.0:
                progress = 0.0
            if progress > 1.0:
                progress = 1.0
        self.post("/task/attribute/update", json={
                                "task_id": get_config().get_task_id(),
                                "type": 'progress',
                                "name": 'progress',
                                "value": progress
                            })


def send_progress(progress):
    Metric().send_progress(progress)
