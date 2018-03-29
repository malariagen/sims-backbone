from backbone_server.errors.backbone_exception import BackboneException

class PermissionException(BackboneException):

    def __init__(self, message):
        self.message = message
