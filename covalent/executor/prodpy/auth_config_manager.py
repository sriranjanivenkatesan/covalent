# Copyright 2023 Agnostiq Inc.


from functools import partial
from pathlib import Path
from typing import Dict

import toml

from ..shared.classes.settings import Settings


class AuthConfigManager:
    @staticmethod
    def get_config_file(settings: Settings = None) -> str:
        """
        Returns the path to the config file.

        Args:
            settings: The settings object to use. If None, the default settings will be used.
        
        Returns:
            The path to the config file.

        """

        if settings is None:
            settings = Settings()

        path = Path(settings.auth.config_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path.resolve())

    @staticmethod
    def get_auth_request_headers(settings: Settings = None) -> Dict[str, str]:
        """
        Returns the headers to use for an authentication request.

        Args:
            settings: The settings object to use. If None, the default settings will be used.
        
        Returns:
            Authentication request headers as a dictionary.

        """

        if settings is None:
            settings = Settings()
        return {"x-api-key": f"{AuthConfigManager.get_api_key(settings)}"}

    @staticmethod
    def save_token(token: str, settings: Settings = None) -> None:
        """
        Saves the authentication token to the config file.

        Args:
            token: The authentication token to save.
            settings: The settings object to use. If None, the default settings will be used.
        
        Returns:
            None

        """

        if settings is None:
            settings = Settings()

        auth_section_header = settings.auth.config_file_section
        token_keyname = settings.auth.cofig_file_token_keyname
        
        toml_dict = {auth_section_header: {}}
        toml_dict[auth_section_header][token_keyname] = token or ""
        
        with open(AuthConfigManager.get_config_file(settings), "w") as f:
            toml.dump(toml_dict, f)

    @staticmethod
    def get_token(settings: Settings = None) -> str:
        """
        Returns the authentication token from the config file.

        Args:
            settings: The settings object to use. If None, the default settings will be used.
        
        Returns:
            The authentication token.

        """

        if settings is None:
            settings = Settings()

        token = settings.auth.token
        if not token:
            auth_section_header = settings.auth.config_file_section
            token_keyname = settings.auth.cofig_file_token_keyname
            
            with open(AuthConfigManager.get_config_file(settings), "r") as f:
                toml_string = f.read()
                parsed_toml = toml.loads(toml_string)
                token = parsed_toml[auth_section_header][token_keyname]
        return token

    @staticmethod
    def get_api_key(settings: Settings = None) -> str:
        """
        Returns the API key from the config file.

        Args:
            settings: The settings object to use. If None, the default settings will be used.
        
        Returns:
            The API key.

        """

        if settings is None:
            settings = Settings()

        api_key = settings.auth.api_key
        if not api_key:
            auth_section_header = settings.auth.config_file_section
            api_keyname = settings.auth.config_file_api_key_keyname

            with open(AuthConfigManager.get_config_file(settings), "r") as f:
                toml_string = f.read()
                parsed_toml = toml.loads(toml_string)
                api_key = parsed_toml[auth_section_header][api_keyname]
        return api_key

    @staticmethod
    def save_api_key(api_key: str, settings: Settings = None) -> None:
        """
        Saves the API key to the config file.

        Args:
            api_key: The API key to save.
            settings: The settings object to use. If None, the default settings will be used.
        
        Returns:
            None

        """

        if settings is None:
            settings = Settings()

        auth_section_header = settings.auth.config_file_section

        api_keyname = settings.auth.config_file_api_key_keyname

        toml_dict = {auth_section_header: {}}
        toml_dict[auth_section_header][api_keyname] = api_key or ""

        with open(AuthConfigManager.get_config_file(settings), "w") as f:
            toml.dump(toml_dict, f)


get_token = partial(AuthConfigManager.get_token)
save_token = partial(AuthConfigManager.save_token)

get_api_key = partial(AuthConfigManager.get_api_key)
save_api_key = partial(AuthConfigManager.save_api_key)
