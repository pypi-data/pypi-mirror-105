import threading

import pyhectiqlab
import pyhectiqlab.ops as ops
from pyhectiqlab.auth import AuthProvider

from packaging import version

class EventsManager():
    def __init__(self, mock=False):
        self.auth_provider = AuthProvider()
        self.mock = mock
        events = []

    def is_logged(self):
        return self.auth_provider.is_logged()

    def refresh_token(self):
        self.auth_provider._refresh_token()
        return

    def compare_python_version(self, on_failed):
        """Compare the current python version and the
        required python version.
        """
        def threading_method():
            res = ops.fetch_minimum_python_version()
            required_version = res['version']
            if version.parse(pyhectiqlab.__version__) < version.parse(required_version):
                print(f'Your pyhectiqlab version ({pyhectiqlab.__version__}) is obsolete (required: {required_version}).')
                print('Update with:')
                print('`pip install --upgrade pyhectiqlab`')
                print('>>>>>>> Switching to dry mode. <<<<<<<<')
                on_failed()
            return res

        x = threading.Thread(target=threading_method)
        x.start()
        return 

    def add_event(self, task_name, args, auth=True, async_method=True, repeat_if_401=True):
        if self.mock :
            return
        method = getattr(ops, task_name)

        def threading_method(*args, **kwargs):
            res = method(*args, **kwargs)
            if res["status_code"]==401:
                if repeat_if_401:
                    self.auth_provider._refresh_token()
                    self.add_event(task_name, args, auth=auth, async_method=False, repeat_if_401=False)
            return res

        kwargs = {}
        if auth:
            kwargs = {"token": self.auth_provider.token}

        if async_method:
            x = threading.Thread(target=threading_method, args=args, kwargs=kwargs)
            x.start()
            return
        else:
            return method(*args, **kwargs)

