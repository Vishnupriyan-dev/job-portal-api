class AuthErr(Exception):
    """Base authentication Error"""
    pass
class InvalidEmailFormat(AuthErr):
    pass
class InvalidPasswordFormat(AuthErr):
    pass
class UserNotFoundError(AuthErr):
    pass
class PasswordMismatchError(AuthErr):
    pass
class JobExpired(AuthErr):
    pass
class JobNotFound(AuthErr):
    pass
class InvalidJobId(AuthErr):
    pass
class InvalidString(AuthErr):
    pass
class ApplicationNotFound(AuthErr):
    pass

class NomatchingJobs(AuthErr):
    pass
class InvalidCredentialsError(AuthErr):
    def __init__(self,msg):
        self.msg=msg
class NoSkillsFound(AuthErr):
    pass
class EmailAlreadyExist(AuthErr):
    pass
class SkillAlreadyExistsError(Exception):
    pass

class CompanyNotFound(AuthErr):
    def __init__(self, msg):
        self.msg=msg
class LocationNotFound(AuthErr):
    def __init__(self, msg):
        self.msg=msg

class NoneKeyError(AuthErr):
    pass
class AuthenticationError(AuthErr):
    pass
class NoneAlgorithm(AuthErr):
    pass
class DomainError(AuthErr):
    pass
class RoleAlreadyGranted(AuthErr):
    def __init__(self, msg):
        self.msg=msg

class MobileAlreadyExistsError(AuthErr):
    pass
class EmailAlreadyExistsError(AuthErr):
    pass

class AuthorizationError(AuthErr):
    def __init__(self,msg):
        self.msg=msg
    

class NoFieldError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class EmptyError(AuthErr):
    def __init__(self,msg):
        self.msg=msg
class NoAlphabetsError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class MobNoError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class PasswordLenError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class PasswordLowerCaseError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class PasswordUpperCaseError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class PasswordDigitError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class PasswordCharactersError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class InvalidJobNameError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class NoMatchedJobs(AuthErr):
    def __init__(self,msg):
        self.msg=msg
class InvalidSalaryError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class InvalidJobNameError(AuthErr):
    def __init__(self,msg):
        self.msg=msg


class JobExpiredError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class UserInactiveError(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class NoStatusFound(AuthErr):
    def __init__(self,msg):
        self.msg=msg

class JobInsertionError(AuthErr):
    def __init__(self,msg):
        self.msg=msg
class SkillInsertionError(AuthErr):
    def __init__(self,msg):
        self.msg=msg


