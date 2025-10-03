#exceptions, глобально храню

class UserAlreadyExistsError(ValueError): #пользователь совпадает уже
    pass

class InvalidPasswordError(ValueError): #пароль не бьет или пароли не совпадают
    pass

class PustoyLoginParolError(ValueError): #тривиально
    pass

class UserNotFoundError(ValueError): #пользователь не найден
    pass

class ValidationError(ValueError): #ошибка валидации
    pass