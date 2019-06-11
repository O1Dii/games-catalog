import os


def _get_env_variable(variable_name):
    try:
        return os.environ[variable_name]
    except KeyError:
        error_msg = f'Set the {variable_name} environment variable'
        raise EnvironmentError(error_msg)
