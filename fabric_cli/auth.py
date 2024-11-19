import os


class Auth:
    _instance = None
    _token = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_token(cls, token):
        cls._token = token.strip()

    def get_access_token(self):
        # First check in-memory token
        if self._token:
            return self._token

        # Then check environment variable
        env_token = os.getenv("POWER_BI_ACCESS_TOKEN")
        if env_token:
            self._token = env_token.strip()
            return self._token

        raise ValueError("No access token found")

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json",
        }

    def __str__(self):
        return f"Auth(token={self._token})"

    def __repr__(self):
        return self.__str__()
