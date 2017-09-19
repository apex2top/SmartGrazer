import configparser
import logging
import os
from operator import methodcaller


class Configuration(object):
    """This class manages the configuration-files of the application.

    This includes the main configuration for the software and the configuration of the built-in payload generators.

    All changes will be stored in a file called config.ini in the applications root directory.
    """
    default_config_file = "config/default.config.ini"
    custom_config_file = "config.ini"

    config = None

    """Loads the configuration files.

        This method tries to load the custom configuration file. If no custom config is present, a custom file will
        be stored containing the default configuration.

        Args:
            self: Object
            params: object

        Returns:
            self: Object

        Raises:
            None
    """

    def __init__(self):
        self.custom_config_file = os.getcwd() + "/" + self.custom_config_file
        self.default_config_file = os.getcwd() + "/" + self.default_config_file

        self.load()

    def handle(self, params):
        """This function handles the configuration for the software.

        A call of this function will always terminate the application.
        """
        if hasattr(params, 'reset') and params.reset is True:
            self.reset()
            exit()
        elif hasattr(params, 'config') and params.config is True:
            self.edit(params)
            exit()
        else:
            if hasattr(params, 'reset') and hasattr(params, 'config'):
                del params.reset, params.config
            # enrich config without saving the params into a file
            self.enrich(params)
            # no exit!

    def load(self):
        """Loads the configuration files.

            This method tries to load the custom configuration file. If no custom config is present, a custom file will
            be stored containing the default configuration.

            Args:
                self: Object

            Returns:
                The configparser instance of the loaded and parsed configuration.

            Raises:
                None
        """
        if self.config is None:
            self.config = self.loadCustom()

        if self.config is None:
            print("No custom config found! Loading default.")
            self.config = self.loadDefault()
            self.store()

        return self.config

    def loadDefault(self):
        """Loads the default configuration files.

            Args:
                self: Object

            Returns:
                The configparser instance of the loaded and parsed configuration.

            Raises:
                None
        """
        config = configparser.ConfigParser()
        config.read(self.default_config_file)

        return config

    def loadCustom(self):
        """Loads the custom configuration files.

            Args:
                self: Object

            Returns:
                The configparser instance of the loaded and parsed configuration or None if the file was not found.

            Raises:
                None
        """
        config = configparser.ConfigParser()

        if os.path.isfile(self.custom_config_file):
            config.read(self.custom_config_file)
            return config

        return None

    def show(self):
        """Prints the current configuration.

            Args:
                self: Object

            Returns:
                Void

            Raises:
                None
        """
        print("--- Configuration ---")
        for key in self.config["DEFAULT"]:
            print(key + ": " + self.config["DEFAULT"][key])
        print("---------------------")

    def get(self, key):
        """Returns the value for a given key.

            Args:
                self: Object\n
                key: String

            Returns:
                String

            Raises:
                None
        """
        if self.config.has_option("DEFAULT", key):
            return self.config["DEFAULT"][key]

        if self.config.has_option("GENERATOR", key):
            return self.config["GENERATOR"][key]

        if self.config.has_option("ENCODER", key):
            return self.config["ENCODER"][key]

        logging.debug(
            "Key \'" + key + "\' was not found in configuration. Returning empty string."
        )
        return ""

    def getList(self, key):
        if self.config["DEFAULT"][key].find(','):
            return self.config["DEFAULT"][key].split(',')
        else:
            return [key]

    def getDict(self, key):
        eq = '='
        themap = map(methodcaller('split', '='), self.getList(key))
        if any(eq in entry for entry in self.getList(key)):
            return dict(themap)
        else:
            return None

    def enrich(self, params):
        """Adds additional parameters to the loaded configuration.

            This allows to overwrite stored configuration values without storing them.

            Args:
                self: Object\n
                params: Dictionary

            Returns:
                store: Boolean

            Raises:
                None
        """
        store = False

        for key in params.__dict__:

            if params.__dict__[key] is not None:
                value = params.__dict__[key]

                if type(value) is list:
                    # convert lists to string
                    self.config["DEFAULT"][key] = ','.join(str(v) for v in value)
                    store = True
                else:
                    self.config["DEFAULT"][key] = str(value)
                    store = True

        return store

    def edit(self, params):
        """Adds additional parameters to the loaded configuration.

            Depending on the return value of the `enrich` method, the config will be overwritten.
            Afterwards the config will be printed to screen.

            Args:
                self: Object\n
                params: Dictionary

            Returns:
                Void

            Raises:
                None
        """

        if self.enrich(params):
            self.store()

        self.show()

    def store(self):
        """Write the configuration into file system.

            Args:
                self: Object\n

            Returns:
                Void

            Raises:
                None
        """
        with open(self.custom_config_file, 'w+') as configfile:
            self.config.write(configfile)
        print("Settings were saved to custom configuration!")

    def reset(self):
        """Delete the custom configuration file.

            Args:
                self: Object\n

            Returns:
                Void

            Raises:
                None
        """
        if os.path.isfile(self.custom_config_file):
            os.remove(self.custom_config_file)

        if not os.path.isfile(self.custom_config_file):
            print("Custom configuration wiped!")
