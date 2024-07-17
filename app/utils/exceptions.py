class ResourceNotFoundError(Exception):
    """Excepción lanzada cuando un recurso no se encuentra en la base de datos."""
    def __init__(self, message="Recurso no encontrado"):
        self.message = message
        super().__init__(self.message)

class ValidationError(Exception):
    """Excepción lanzada cuando falla la validación de datos de entrada."""
    def __init__(self, message="Error de validación"):
        self.message = message
        super().__init__(self.message)