class HAHQConfigurator(object):
    """
    This class helps converting a config dict to a string which has the format of the HAProxy config file.
    Converting works bi-directional.
    """
    class HAHQConfiguratorException(Exception):
        """
        this Exception is thrown for all kind of errors regarding the conversion
        """
        pass

    SECTION_KEYWORDS = [
        'global',
        'defaults',
        'frontend',
        'backend',
        'listen',
        'peers',
        'mailers',
        'userlist',
        'namespace_list',
        'resolvers',
    ]
    """a list of keywords indicating the begin of a section in the HAProxy config file"""

    def __init__(self, config_data=None, config_string=None):
        """
        a HAHQConfigurator can be initialized either with a dict describing the config, or a string formatted like the
        config file.

        :param config_data: dict with config data
        :param config_string: string in config file format
        :raises HAHQConfigurator.HAHQConfiguratorException: is thrown in case neither config data nor config string is
        supplied
        """
        if not config_data and not config_string:
            raise HAHQConfigurator.HAHQConfiguratorException('either config data or config string has to be supplied')
        self.config_data = config_data if config_data else None
        self.config_string = config_string if config_string else None

    def __str__(self):
        return self.get_config_string()

    def __dir__(self):
        return self.get_config_data()

    def __eq__(self, other):
        if not isinstance(other, HAHQConfigurator) or self.get_config_data() != other.get_config_data():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_config_string(self):
        """
        returns the config as string and converts it to string, in case it's only available as a dict

        :return: config string
        """
        if not self.config_string:
            self.__build_config_string()

        return self.config_string

    def get_config_data(self):
        """
        returns the config data as a dict and converts it to dict, in case it's only available as a string

        :return: config data
        """
        if not self.config_data:
            self.__build_config_data()

        return self.config_data

    def __build_config_string(self):
        """
        builds the config string from config data

        :raises HAHQConfigurator.HAHQConfiguratorException: is thrown in case config data isn't set
        """
        if not self.config_data:
            raise HAHQConfigurator.HAHQConfiguratorException('no config data set')

        self.config_string = ''

        for section in self.config_data['configHolder']:
            self.config_string += section['section']['type'] + ' ' + section['section']['name'] + '\n'

            for value in section['values']:
                self.config_string += '\t' + value + '\n'

            self.config_string += '\n'

        self.config_string = self.config_string[:(len(self.config_string) - 2)]

    def __build_config_data(self):
        """
        builds the config data from config string

        :raises HAHQConfigurator.HAHQConfiguratorException: is thrown in case config string isn't set
        """
        if not self.config_string:
            raise HAHQConfigurator.HAHQConfiguratorException('no config string set')

        self.config_data = {'configHolder': []}

        section = None

        for line in self.config_string.split('\n'):
            words = line.split()

            if len(words) > 0 and words[0][0] != '#':
                if words[0] in self.SECTION_KEYWORDS:
                    if section:
                        self.config_data['configHolder'].append(section)

                    section = {
                        'section': {
                            'type': words[0],
                            'name': ' '.join(words[1:]),
                        },
                        'values': [],
                    }
                else:
                    if section:
                        section['values'].append(' '.join(words))

        if section:
            self.config_data['configHolder'].append(section)
