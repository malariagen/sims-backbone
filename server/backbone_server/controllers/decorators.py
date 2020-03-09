import sys
import inspect
import os
import types
import re

def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects


def log_this(controller, original_function):
    def new_function(*args, **kwargs):
        log_args = args
        user = None
        if 'user' in kwargs:
            user = kwargs['user']
        elif not os.getenv('BB_NOAUTH'):
            user = args[-2]
            log_args = args[:-2]
        func_name = sys._getframe(1).f_code.co_name
        # if kwargs is not None:
        #    for key, value in kwargs.items():
        #        print("%s == %s"%(key,value))
        x = original_function(*args, **kwargs)

        controller.log_action(user, func_name, None, log_args, x[0], x[1])

        return x
    return new_function

# Not actually a decorator as don't want to call original function multiple times


def authorize_this(original_function):
    def new_function(*args, **kwargs):
        user = None
        auths = None
        if not os.getenv('BB_NOAUTH'):
            if 'user' in kwargs:
                user = kwargs['user']
            else:
                user = args[-2]
            if 'auths' in kwargs:
                auths = kwargs['auths']
            else:
                auths = args[-1]
            func_name = original_function.__name__

            #print(f'authorize_this {func_name} {auths}')

            if not auths:
                message = f"No permission {func_name} {user} {auths}"
                return message, 403
            elif 'cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net' not in auths:
                message = f"No permission {func_name} {user} {auths}"
                return message, 403
            else:
                sig = inspect.signature(original_function)
                if any(param for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD and param.name == 'studies'):
                    studies = []
                    if 'cn=all_studies,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net' in auths:
                        studies.append({
                            'bucket': 'pi',
                            'study': 'all'
                        })
                    else:
                        pattern = re.compile(r'cn=(\w+),ou=(\d+),ou=studies,ou=groups,dc=malariagen,dc=net')
                        for auth in auths:
                            match = pattern.match(auth)
                            if match:
                                studies.append({
                                    'bucket': match.group(1),
                                    'study': match.group(2)
                                })
#                    studies = [ { 'bucket': 'pi', 'study': '1208' } ]
                    kwargs['studies'] = studies

        x = original_function(*args, **kwargs)
        return x
    return new_function


def apply_decorators(Cls):
    class NewCls(object):
        def __init__(self, *args, **kwargs):
            self.oInstance = Cls(*args, **kwargs)

        def __getattribute__(self, s):
            """
            this is called whenever any attr of a NewCls object is accessed.
            This function first tries to get the attribute off NewCls.
            If it fails then it tries to fetch the attr from self.oInstance
            (an instance of the decorated class).
            If it manages to fetch the attribute from self.oInstance, and
            the attribute is an instance method then `time_this` is applied.
            """
            try:
                x = super(NewCls, self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            x = self.oInstance.__getattribute__(s)
            protected = False
            if type(x) == type(self.__init__): # it is an instance method
                protected = True
                # Don't want any methods from BaseController protected as
                # they don't have the correct args
                if get_class_that_defined_method(x).__name__ == "BaseController":
                    protected = False

            if protected:
                return log_this(self.oInstance, authorize_this(x))
            else:
                return x
    return NewCls
