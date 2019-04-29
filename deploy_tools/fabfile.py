import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/gwalliman/tdd_with_python'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    run('sudo apt-get install -y nginx python3-venv git')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _setup_nginx_and_gunicorn()

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=$H", capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput') #noinput removes y/n confirmations

def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput') #noinput removes y/n confirmations

def _setup_nginx_and_gunicorn():
    run(f'cat /home/{env.user}/sites/{env.host}/deploy_tools/nginx.template.conf | sed "s/DOMAIN/{env.host}/g" | sudo tee /etc/nginx/sites-available/{env.host}')
    run(f'sudo ln -sf /etc/nginx/sites-available/{env.host} /etc/nginx/sites-enabled/{env.host}')
    run('sudo rm -f /etc/nginx/sites-enabled/default')
    run(f'cat /home/{env.user}/sites/{env.host}/deploy_tools/gunicorn-systemd.template.service | sed "s/DOMAIN/{env.host}/g" | sudo tee /etc/systemd/system/gunicorn-{env.host}.service')
    run(f'cat /home/{env.user}/sites/{env.host}/deploy_tools/gunicorn_start.template.sh | sed "s/DOMAIN/{env.host}/g" | sudo tee /home/{env.user}/sites/{env.host}/gunicorn_start.sh')
    run(f'sudo chmod +x /home/{env.user}/sites/{env.host}/gunicorn_start.sh')
    run('sudo systemctl daemon-reload')
    run('sudo systemctl reload nginx')
    run(f'sudo systemctl enable gunicorn-{env.host}.service')
    run(f'sudo systemctl start gunicorn-{env.host}.service')
