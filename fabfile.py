import os
from fabric.api import env, run

USER = 'Windson'
TOUCH = '/var/www/www_jobder_net_wsgi.py'

env.user = 'Windson'
env.hosts = ['ssh.pythonanywhere.com']
site_folder = '/home/{0}/jobder/'.format(USER)


def deploy():
    # git stath
    run_deploy()
    update_val()
    reset()


def update_val():
    js_key_path = os.path.join(site_folder, 'static/js/job.js')
    js_base_url = os.path.join(site_folder, 'static/js/base.js')
    py_key_path = os.path.join(site_folder, 'common/const.py')
    run('sed -i "s/pk_test_fEJG3FbEEKCGhriUfqjWJZG5/pk_live_1vr5cqWQbuK89pF5nDwxNXCQ/g" {0}'.format(js_key_path))
    run('sed -i "s/sk_test_Mrp9fWK53zgna3gSbGGUy60W/sk_live_hdOhJFb3UdlQhvFlW9LfWAaE/g" {0}'.format(py_key_path))
    run('sed -i "s=http://127.0.0.1:8000/=https://www.jobder.net/=g" {0}'.format(js_base_url))
    run('sed -i "s/DEBUG\s=\sTrue/DEBUG\s=\sFalse/g" {0}'.format(js_base_url))


def run_deploy():
    run('cd {0} && git stash && git pull origin master && git stash pop && source ~/.virtualenvs/jobder/bin/activate && python manage.py migrate'.format(site_folder))


def reset():
    run('touch /var/www/www_jobder_net_wsgi.py')
