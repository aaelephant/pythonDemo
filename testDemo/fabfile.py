from fabric.api import cd, env, prefix, run, task

env.hosts = ['172.29.90.7', '172.29.90.7']

@task
def memory_usage():
    run('free -m')

@task
def deploy():
    with cd('/var/www/project-env/project'):
        with prefix('. ../bin/activate'):
            run('git pull')
            run('touch app.wsgi')