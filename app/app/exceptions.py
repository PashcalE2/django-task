class AppError(RuntimeError):
    status: int
    message: str
