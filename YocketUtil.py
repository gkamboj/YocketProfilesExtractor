from jproperties import Properties


class YocketUtil:

    @staticmethod
    def get_headers():
        headers = {
            'Authorization': YocketUtil.get_cred_config()['ACCOUNT_TOKEN'][0]
        }
        return headers

    @staticmethod
    def get_app_config():
        configs = Properties()
        with open('app_config.properties', 'rb') as config_file:
            configs.load(config_file)
        return configs

    @staticmethod
    def get_cred_config():
        credentials = Properties()
        with open('credentials_config.properties', 'rb') as config_file:
            credentials.load(config_file)
        return credentials
