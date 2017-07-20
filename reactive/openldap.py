from charms.reactive import when, when_not, set_state, remove_state
from charms.layer import snap
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import config, status_set
from subprocess import check_output
import string
import random


@when_not('openldap.installed')
def install_openldap():
    channel = config('channel')
    status_set('maintenance', 'Installing openldap snap')
    snap.install('openldap', channel=channel, devmode=True)
    # set_state('openldap.snaps.installed')
    # remove_state('openldap.components.started')
    set_state('openldap.installed')

@when('openldap.installed')
@when_not('openldap.configured')
def configure_openldap():
    admin_password = password_generator()
    status_set('maintenance', 'Configuring openldap snap')
    check_output ("snap set openldap password="+admin_password)
    write_file("/root/openldap.password", admin_password)
    status_set('maintenance', 'openldap configured')
    set_state('openldap.configured')

@when('openldap.configured')
def start_openldap():
    # status_set('maintenance', 'Starting openldap snap')
    status_set('active', 'openldap running')
    set_state('openldap.running')

@when('openldap.running')
def config_openldap():
    channel = config('channel')
    if data_changed('admin-password', hookenv.config('admin-password')) and hookenv.config('admin-password') != "":
        check_output ("snap set openldap password="+admin_password)
        

def password_generator():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    return ''.join(random.choice(chars) for x in range(size))

def write_file(filename, output):
    with open(filename ,'w') as out:
        out.write(output + '\n')

