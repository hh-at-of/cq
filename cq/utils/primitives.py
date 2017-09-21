
from celery import group
import cloudpickle
import simplejson as json
import logging

from cq.utils.json_advanced_encoder import AdvEncoder
from cq.tasks.tasks import run_fct

logger = logging.getLogger(__name__)


class CQTask(object):
    def __init__(self, fct, *args, **kwargs):
        self.serialized_code = cloudpickle.dumps(fct)

        # jsonfy args and kwargs
        jsonArgs = json.dumps(args, cls=AdvEncoder, ignore_nan=True)
        jsonKwargs = json.dumps(kwargs, cls=AdvEncoder, ignore_nan=True)

        self.task = run_fct.s(self, jsonArgs, jsonKwargs)

    def apply_async(self):
        ### add position and ooptional arguments
        ##args = tuple( [ a for a in self.task.args ] + [ a for a in args ] )
        ##kwargs.update( self.task.kwargs )
        ##
        ### jsonfy args and kwargs
        ##jsonArgs = json.dumps( args, cls=AdvEncoder, ignore_nan=True )
        ##jsonKwargs = json.dumps( kwargs, cls=AdvEncoder, ignore_nan=True )
        ##
        ### remove previous args and kwargs from task
        ##self.task.args = []
        ##self.task.kwargs = {}
        
        ##return self.task.apply_async( (self, jsonArgs, jsonKwargs ), serializer='pickle'  )
        logger.info("submit task")

        return self.task.apply_async(serializer='pickle')

    def __call__(self, *args, **kwargs):
        self.apply_async(*args, **kwargs)


class CQGroup(object):
    def __init__(self, functions=[]):
        self.cq_tasks = []
        self._add_tasks(functions)
        self.group = group(f.task for f in self.cq_tasks)
        self.results = None

    def _add_tasks(self, fcts):
        for d in fcts:
            fct = d["fct"]
            args = d.get("args", ())
            kwargs = d.get("kwargs", {})

            cq_task = CQTask(fct, *args, **kwargs)
            self.cq_tasks.append(cq_task)

    def apply_async(self):
        self.results = self.group.apply_async(serializer='pickle')

    def get(self):
        return self.results.get()
