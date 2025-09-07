from invoke import task


@task
def dev(c):
    c.run("uvicorn app.main:app --reload")


@task
def migrate(c, name):
    c.run(f"prisma migrate dev --name {name}", pty=True)


@task
def db_generate(c):
    c.run("prisma generate")


@task
def updatePackages(c):
    result = c.run("pip freeze", hide=True, encoding="utf-8")
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(result.stdout)
