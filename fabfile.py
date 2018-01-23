from fabric.contrib.files import exists, sed
from fabric.api import env, local, run
from fabric.operations import put

REPO_URL = 'git@github.com:Windsooon/Unicooo-django.git'
USER = 'Windson'
TOUCH = '/var/www/www_jobder'


def deploy():
    site_folder = '/home/{0}/jobder/'.format(USER)
    # git stath
    run('cd {0} && git stash'.format(site_folder))
    run('git pull origin master')
    run('git stash pop')
    run('touch {0}'.format(TOUCH))
