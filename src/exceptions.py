class BaseException(Exception):
    msg = None

    def __init__(self, msg: str = None):
        msg = msg or self.msg
        super().__init__(msg)


class ErrorCodes:
    UNAUTHORIZED = 401
    FORBIDDEN = 401
    NOT_FOUND = 404
    FAILED = 500


class ServerError(BaseException):
    msg = 'server error'
    error_code = None


class UserNotFound(ServerError):
    msg = 'user not found'
    error_code = ErrorCodes.NOT_FOUND


class AuthRequired(ServerError):
    msg = 'auth required'
    error_code = ErrorCodes.UNAUTHORIZED


class AuthFailed(ServerError):
    msg = 'auth failed'
    error_code = ErrorCodes.FORBIDDEN


class FileAlreadyExists(ServerError):
    msg = 'such file already exists'
    error_code = ErrorCodes.FAILED


class FileNotFound(ServerError):
    msg = 'no such file'
    error_code = ErrorCodes.NOT_FOUND


class UserFileNotFound(ServerError):
    msg = 'user does not have such file'
    error_code = ErrorCodes.NOT_FOUND
