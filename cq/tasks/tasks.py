
from celery.utils.log import get_task_logger

from cq.app import app
from cq.utils.json_advanced_encoder import AdvEncoder

import simplejson as json
import pickle

logger = get_task_logger(__name__)


@app.task
def run_fct(cq_task, args, kwargs, do_not_jsonfy_result=False):
    fct = pickle.loads(cq_task.serialized_code)

    # load args and kwargs which are json objects
    args = json.loads(args)
    kwargs = json.loads(kwargs)

    #print("args",args)
    #print("kwargs",kwargs)

    # call function with given arguments
    logger.info("run function ...")
    ret = fct(*args, **kwargs)
    logger.info("done.")

    # return ret as json or not
    if do_not_jsonfy_result:
        return ret
    else:
        return json.dumps(ret, cls=AdvEncoder, ignore_nan=True)


@app.task
def test_task(*args, **kwargs):
    print("test args", args)
    print("test kwargs", kwargs)

    return 42
