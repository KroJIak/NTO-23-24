# from functools import lru_cache

# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     LOCAL: bool = False
#     DEBUG: bool = False
#     IMAGEFILE: str = None


# @lru_cache()
# def settings():
#     return Settings(
#         _env_file=".env",
#         _env_file_encoding="utf-8",
#     )
