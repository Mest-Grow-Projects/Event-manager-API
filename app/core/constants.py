messages = {
    "db_connection": "Database connection initialized...",
    "shutdown": "Application shutting down...",
    "app_title": "Events Management API",
    "app_description": "A REST API to manage events",
    "app_version": "1.0.0",
    "welcome": "Welcome to the Event Management System API"
}

error_messages = {
    "database_url": "DATABASE_URL environment variable is not set",
    "internal_error": "An internal server error occurred",
    "expired_token": "Token has expired, please login again",
}

status_messages = {
    "not_found": "User not found, please create an account",
    "conflict": "User with this email already exists, you can login",
    "credentials_error": "Authorization header must be provided with a 'Bearer' prefix",
    "code_required": "Verification code is required",
    "update_invalid": "No valid fields provided for update",
    "user_id_required": "User ID is required",
    "failed_user": "Failed to create a new user",
    "access_denied": "Unauthorized access, no token provided"
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
    "all_users": "Users retrieved successfully",
    "found_user": "User found successfully",
    "update_user": "User updated successfully",
    "delete_user": "User deleted successfully",
    "add_app_admin": "Admin added successfully",
    "change_role_status": "User role status changed successfully",
    "add_organizer": "Organizer added successfully",
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
    "invalid_payload": "Invalid token payload",
}