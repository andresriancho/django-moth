import os


def get_plugin_families():
    '''
    :return: A list of strings with the names of the plugin families.
    '''
    vuln_content = os.listdir('moth/views/vulnerabilities/')
    try:
        vuln_content.remove('__init__.py')
        vuln_content.remove('__init__.pyc')
    except ValueError:
        pass
    return sorted(vuln_content)