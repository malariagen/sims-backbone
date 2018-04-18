import sys

def log_this(controller, original_function):
    def new_function(*args,**kwargs):
        user = args[-2]
        func_name = sys._getframe(1).f_code.co_name
        if kwargs is not None:
            for key, value in kwargs.items():
                print("%s == %s"%(key,value))
        import datetime
        before = datetime.datetime.now()
        x = original_function(*args,**kwargs)

        controller.log_action(user, func_name, None, args[:-2], x[0], x[1])

        return x
    return new_function

#Not actually a decorator as don't want to call original function multiple times
def authorize_this(original_function):
    def new_function(*args,**kwargs):
        user = args[-2]
        auths = args[-1]
        func_name = original_function.__name__

        if not auths:
            pass
        elif not 'cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net' in auths:
            message = 'No permission {} {} {}'.format(func_name, user, auths)
            return message, 403

        x = original_function(*args,**kwargs)
        return x
    return new_function

def apply_decorators(Cls):
    class NewCls(object):
        def __init__(self,*args,**kwargs):
            self.oInstance = Cls(*args,**kwargs)
        def __getattribute__(self,s):
            """
            this is called whenever any attribute of a NewCls object is accessed. This function first tries to
            get the attribute off NewCls. If it fails then it tries to fetch the attribute from self.oInstance (an
            instance of the decorated class). If it manages to fetch the attribute from self.oInstance, and
            the attribute is an instance method then `time_this` is applied.
            """
            try:
                x = super(NewCls,self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            x = self.oInstance.__getattribute__(s)
            if type(x) == type(self.__init__): # it is an instance method
                return log_this(self.oInstance, authorize_this(x))
            else:
                return x
    return NewCls

