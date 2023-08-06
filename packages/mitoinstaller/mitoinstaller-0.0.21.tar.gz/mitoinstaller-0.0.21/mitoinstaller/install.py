"""
We specify the installer as a list of steps that 
must run in order, for the installer.

Currently, we take the following steps:
1. First, try and install mitosheet3. As this works on 
   JLab 3, we first check if the user has any conflicting
   JLab 2 dependencies installed. If they do, we abort.
2. Then, if the above installation of mitosheet3 fails for 
   any reason, then we try to install mitosheet on JLab 2. 
3. If neither of them work, we give up, sadly. 
"""
from time import sleep
import io
from contextlib import redirect_stdout

from mitoinstaller.colors import NORMAL_TEXT, GREEN_TEXT
from mitoinstaller.commands import install_pip_packages, upgrade_mito_installer, exit_with_error
from mitoinstaller.log_utils import analytics, log, identify, log_step_failed
from mitoinstaller.user_install import (create_user_install, get_static_user_id_install, set_user_field)

# SHARED UTILITIES

def initial_install_step_create_user(install_or_upgrade):
    static_user_id_install = get_static_user_id_install()

    # If the user has no static install ID, create one
    if static_user_id_install is None:
        create_user_install()    
    
    identify()
    log(f'{install_or_upgrade}_started')


# MITOSHEET 3 INSTALL STEPS

def install_step_mitosheet3_check_dependencies():    
    try:
        from jupyterlab import __version__, commands
    except:
        # If JupyterLab cannot be imported, we assume
        # that we won't have any issues w/ dependencies
        return
    
    # If jupyter lab 3 can be imported, then we can install mitosheet3!
    if __version__.startswith('3'):
        return

    # If there are no extensions, we can continue
    f = io.StringIO()
    with redirect_stdout(f):
        commands.list_extensions()
    output = f.getvalue().splitlines()

    if 'No installed extensions' in output:
        return
    else:
        # Otherwise, we raise an error as they might conflict
        raise Exception("Installed extensions %s", output) 

def install_step_mitosheet3_install_mitosheet3():
    install_pip_packages('mitosheet3')

def install_step_mitosheet3_finish_install():
    # Mark that we finished install
    set_user_field('install_finished', True)
    log(f'install_finished_mitosheet3', {'package': 'mitosheet3'})
    

INSTALL_MITOSHEET3_STEPS = [
    {
        'step_name': 'check dependencies',
        'execute': install_step_mitosheet3_check_dependencies
    },
    {
        'step_name': 'install mitosheet3',
        'execute': install_step_mitosheet3_install_mitosheet3
    },
    {
        'step_name': 'finish install',
        'execute': install_step_mitosheet3_finish_install
    },
]



# MITOSHEET 2 INSTALL STEPS


def install_step_mitosheet_install_mitosheet():
    install_pip_packages('mitosheet')


def install_step_mitosheet_install_jupyter_widget_manager():
    from jupyterlab import commands
    commands.install_extension('@jupyter-widgets/jupyterlab-manager@2')


def install_step_mitosheet_rebuild_jupyterlab():
    from jupyterlab import commands
    commands.build()


def install_step_mitosheet_upgrade_mitoinstaller():
    upgrade_mito_installer()

def install_step_mitosheet_finish_install():
    # Mark that we finished install
    set_user_field('install_finished', True)
    log(f'install_finished_mitosheet', {'package': 'mitosheet'})

INSTALL_MITOSHEET_STEPS = [
    {
        'step_name': 'upgrade mitoinstaller',
        'execute': install_step_mitosheet_upgrade_mitoinstaller
    },
    {
        'step_name': 'install mitosheet',
        'execute': install_step_mitosheet_install_mitosheet
    },
    {
        'step_name': 'install @jupyter-widgets/jupyterlab-manager@2',
        'execute': install_step_mitosheet_install_jupyter_widget_manager
    },
    {
        'step_name': 'rebuild JupyterLab',
        'execute': install_step_mitosheet_rebuild_jupyterlab
    },
    {
        'step_name': 'finish install',
        'execute': install_step_mitosheet_finish_install
    },
]

def do_install_or_upgrade(install_or_upgrade):
    """
    install_or_upgrade is the workhorse of actually installing mito. It first attempts
    to install mitosheet3, and if that fails, installs mitosheet.

    install_or_upgrade should be 'install' or 'upgrade'

    Notably, the process for installing Mito initially and upgrading Mito are
    identical. As such, we reuse this function to upgrade, just with different
    error and logging messages.
    """
    if install_or_upgrade == 'install':
        success_message = f'\nMito3 has finished installing. Relaunch JupyterLab to render your first mitosheet. \n\nRun the command:\t{GREEN_TEXT}jupyter lab{NORMAL_TEXT}\n'
    else:
        success_message = f'\nMito3 has finished upgrading. Relaunch JupyterLab to see new functionality. \n\nRun the command:\t{GREEN_TEXT}jupyter lab{NORMAL_TEXT}\n'
    
    initial_install_step_create_user(install_or_upgrade)

    for idx, install_step in enumerate(INSTALL_MITOSHEET3_STEPS):
        try:
            install_step['execute']()
            
            # If we finish install, then tell the user, and exit
            if idx >= len(INSTALL_MITOSHEET3_STEPS) - 1:
                print(success_message)
                exit(0)
        except SystemExit:
            exit(0)
        except:
            # Note: if mitosheet3 installation fails, we log it, but we do
            # not exit, as we want to continue and try to install mitosheet
            error_message = "failed to " + install_step['step_name']
            log_step_failed(install_or_upgrade, 'mitosheet3', error_message)
            # We do break out of this loop!
            break

    for install_step in INSTALL_MITOSHEET_STEPS:
        try:
            install_step['execute']()
        except:
            error_message = "failed to " + install_step['step_name']
            log_step_failed(install_or_upgrade, 'mitosheet', error_message)
            exit_with_error(install_or_upgrade, error_message)

    print(success_message)