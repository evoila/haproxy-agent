class HAHQConfigurator(object):
    class HAHQConfiguratorException(Exception):
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

    def __init__(self, config_data=None, config_string=None):
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
        if not self.config_string:
            self.__build_config_string()

        return self.config_string

    def get_config_data(self):
        if not self.config_data:
            self.__build_config_data()

        return self.config_data

    def __build_config_string(self):
        if not self.config_data:
            raise HAHQConfigurator.HAHQConfiguratorException('no config data set')

        # TODO: build config string from data dict

    def __build_config_data(self):
        if not self.config_string:
            raise HAHQConfigurator.HAHQConfiguratorException('no config string set')

        self.config_data = []

        section_key = None
        section = None

        for line in self.config_string.split('\n'):
            words = line.split()

            if len(words) > 0 and words[0][0] != '#':
                if words[0] in self.SECTION_KEYWORDS:
                    if section and section_key:
                        self.config_data.append({section_key: section})

                    section_key = words[0]
                    section = [{'_name': ' '.join(words[1:])}]
                else:
                    if section_key:
                        section.append({ words[0]: ' '.join(words[1:])})

        if section and section_key:
            self.config_data.append({section_key: section})