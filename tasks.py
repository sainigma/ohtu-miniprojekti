from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/index.py")

@task
def test(ctx):
    ctx.run("export TESTING=True; pytest src")

@task
def coverage(ctx):
    ctx.run("export TESTING=True; coverage run --branc -m pytest src")

@task
def coverage_report(ctx):
    ctx.run("coverage html")

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")

@task
def robot(ctx):
    ctx.run("export TESTING=True; robot src")

@task
def verify(ctx):
    test(ctx)
    robot(ctx)
    lint(ctx)
