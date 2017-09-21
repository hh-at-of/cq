import datetime
import numpy as np
import simplejson as json
import pandas as pd


class AdvEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_json()
        else:
            try:
                return super(AdvEncoder, self).default(obj)
            except:
                return("STRING:{}".format(obj))

    def dumps(self, *args, ensure_ascii=False, ignore_nan=True, **kwargs):
        return super(AdvEncoder, self).dumps(*args, default=self.default,
                                             ensure_ascii=ensure_ascii,
                                             ignore_nan=ignore_nan, **kwargs)
