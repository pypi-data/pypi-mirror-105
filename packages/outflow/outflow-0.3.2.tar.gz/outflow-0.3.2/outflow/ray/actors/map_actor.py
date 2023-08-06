# -*- coding: utf-8 -*-
import traceback
from typing import List

import ray
from outflow.core.logging import logger
from outflow.core.tasks.task_manager import TaskManager

from .base_actor import BaseActor


class BaseMapActor(BaseActor):
    def __init__(
        self,
        workflow,
        batch_inputs: List,
        index: int,
        raise_exceptions: bool,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        import logging

        logging.basicConfig(level=logging.DEBUG)
        # init_logger()

        self.workflow = workflow
        self.batch_inputs = batch_inputs
        self.index = index
        self.raise_exceptions = raise_exceptions
        self._progress = 0
        self._total = len(batch_inputs)

    def progress(self):
        return self._progress

    def total(self):
        return self._total

    def run(self):
        profile = False

        if profile:
            import cProfile

            pr = cProfile.Profile()
            pr.enable()

        ret = self._run()

        if profile:
            pr.dump_stats("one_outflow_raster_workflow.prof")
            pr.disable()

        return ret

    def _run(self):
        results = list()
        for index, input in enumerate(self.batch_inputs):
            logger.info(f"Processing input {index} of {len(self.batch_inputs)}")
            self._progress = index
            workflow_copy = self.workflow.copy()
            workflow_copy.entrypoint.bind(**input)

            terminating_tasks = list()

            if len(self.batch_inputs) == 0:
                return []

            for task in workflow_copy:
                # task.context = self.pipeline_context
                task.parallel_workflow_id = self.index

                task_manager = TaskManager()

                try:
                    task_manager.compute(workflow_copy)

                    for task in workflow_copy:
                        if task.terminating:
                            terminating_tasks.append(task_manager.results[task.id])

                    results.append(terminating_tasks)
                except Exception as e:
                    if self.raise_exceptions:
                        raise e
                    logger.warning(f"A map actor raised an exception in Map '{self}'")
                    logger.warning(traceback.format_exc())
                    results = [e]

        return results


@ray.remote
class MapActor(BaseMapActor):
    pass
