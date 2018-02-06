import os
from fabric.api import env, run
from fabric.network import ssh

USER = 'Windson'
TOUCH = '/var/www/www_jobder_net_wsgi.py'

env.user = 'Windson'
env.hosts = ['ssh.pythonanywhere.com']
site_folder = '/home/{0}/jobder/'.format(USER)


def deploy():
    # git stath
    # run_deploy()
    update_key()


def update_key():
    js_key_path = os.path.join(site_folder, 'static/js/job.js')
    run('sed -i "s/pk_test_fEJG3FbEEKCGhriUfqjWJZG5/pk_live_1vr5cqWQbuK89pF5nDwxNXCQ/g" {0}'.format(js_key_path))


def run_deploy():
    run(
        'cd {0} && git stash && git pull origin master && git stash pop && touch {1}'.format(site_folder, TOUCH))
