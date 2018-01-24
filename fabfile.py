from fabric.contrib.files import exists, sed
from fabric.api import env, local, run
from fabric.operations import put

USER = 'Windson'
TOUCH = '/var/www/www_jobder_net_wsgi.py'

env.user = 'Windson'
env.hosts = ['ssh.pythonanywhere.com']



def deploy():
    site_folder = '/home/{0}/jobder/'.format(USER)
    # git stath
    run(
        'cd {0} && git stash && git pull origin master && git stash pop && touch {1}'.format(site_folder, TOUCH))
