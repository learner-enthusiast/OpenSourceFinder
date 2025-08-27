from invoke import task

@task
def dev(c):
    c.run("uvicorn app.main:app --reload")

@task
def migrate(c,name):
       c.run(f"prisma migrate dev --name {name}")


@task
def db_generate(c):
    c.run("prisma generate")
