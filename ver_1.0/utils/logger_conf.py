from datetime import datetime


def log_auth(event, login, ip, status, reason, user_agent):

    line = (
        f"{datetime.now()} | "
        f"event={event} | "
        f"login={login} | "
        f"ip={ip} | "
        f"status={status} | "
        f"reason={reason} | "
        f"user_agent={user_agent}\n"
    )

    with open("logs/auth.log", "a") as f:
        f.write(line)

"""
РЕГИСТРАЦИЯ:
пароли не совпали
log_auth("REGISTER", email, ip, "FAILED", "password_mismatch", user_agent)

существующий пользователь
log_auth("REGISTER", email, ip, "FAILED", "user_exists", user_agent)

успешная регистрация
log_auth("REGISTER", email, ip, "SUCCESS", "ok", user_agent)

LOGIN:
успешно
log_auth("LOGIN", email, ip, "SUCCESS", "ok", user_agent)

неуспешно
log_auth("LOGIN", email, ip, "FAILED", "invalid_credentials", user_agent)
"""

def get_client_ip(request):

    ip = request.headers.get("X-Forwarded-For")

    if ip:
        ip = ip.split(",")[0]
    else:
        ip = request.remote_addr

    return ip