import os

def get_user_service_url() -> str:
    hostname: str = os.getenv("USERSERVICE_HOSTNAME")
    port: str = os.getenv("USERSERVICE_PORT")
    return f"http://{hostname}:{port}"