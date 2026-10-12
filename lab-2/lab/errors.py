class AppError(Exception):
    """Basic application exception"""
    pass

class ValidationError(AppError):
    """Data validation exception"""
    pass

class FileError(AppError):
    """File processing exception"""
    pass

class StudentNotFoundError(AppError):
    """Student not found exception"""
    pass