messages = {
    "db_connection": "Database connection initialized...",
    "shutdown": "Application shutting down...",
    "app_title": "Events Management API",
    "app_description": "A REST API to manage events",
    "app_version": "1.0.0",
    "welcome": "Welcome to the Event Management System API"
}

error_messages = {
    "database_url": "DATABASE_URL environment variable is not set"
}

status_messages = {
    "not_found": "User not found",
    "conflict": "User with this email already exists",
    "credentials_error": "Could not validate credentials",
    "code_required": "Verification code is required",
}

origins = [
    "http://localhost:4200",
    "http://localhost:8080",
]

patterns_regex = {
    "name": r"^[a-zA-Z]+(?: [a-zA-Z]+)*$",
    "code": r"^\d{6}$",
}

success_messages = {
    "verify_account": "Account verified successfully",
    "login": "Login successful",
    "signup": "Signup successful",
}

validations = {
    "name": "Name must contain only letters and single spaces between words, no numbers or special characters allowed",
    "password": "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character",
    "code": "Verification OTP code must be a 6-digit number",
    "password_mismatch": "passwords don't match",
    "invalid_credentials": "Incorrect email or password",
    "not_verified": "Account not verified, Please check your email and verify your account",
    "already_verified": "Account already verified, Please login",
    "lowercase": "password must contain at least one lowercase letter",
    "uppercase": "password must contain at least one uppercase letter",
    "digit": "password must contain at least one digit",
    "special_character": "password must contain at least one special character",
    "token_required": "Token is required",
    "invalid_code": "Verification code is not valid",
    "invalid_token": "Invalid token",
}