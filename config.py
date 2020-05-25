from configparser import ConfigParser

def config_setup(filename='config_setup.ini' , section='postgresql'):
    """
    Sets up the congfig_setup.ini file for setup.py
    :return: Returns a dictionary of the parameters from the config file
    """
    parser=ConfigParser()
    parser.read(filename)

    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]]=param[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def config_live(filename='config_live.ini' , section='postgresql'):
    """
    Sets up the congfig_setup.ini file for setup.py
    :return: Returns a dictionary of the parameters from the config file
    """
    parser=ConfigParser()
    parser.read(filename)

    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]]=param[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db