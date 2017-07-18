from charms.reactive import when, when_not, set_state, remove_state
from charms.layer import snap
from charmhelpers.core import hookenv
from subprocess import check_output

@when_not('openldap.installed')
def install_openldap():
    channel = hookenv.config('channel')
    hookenv.status_set('maintenance', 'Installing openldap snap')
    snap.install('openldap', channel=channel, devmode=True)
    set_state('openldap.snaps.installed')
    remove_state('openldap.components.started')
    set_state('openldap.installed')

@when('openldap.installed')
@when_not('openldap.configured')
def configure_openldap():
    hookenv.status_set('maintenance', 'Configuring openldap snap')
    check_output(['openldap.slapd-config'])
    hookenv.status_set('maintenance', 'openldap configured')
    set_state('openldap.configured')

@when('openldap.configured')
def start_openldap():
    hookenv.status_set('maintenance', 'Starting openldap snap')
    check_output(['openldap.slapd'])
    hookenv.status_set('active', 'openldap running')
    set_state('openldap.running')
