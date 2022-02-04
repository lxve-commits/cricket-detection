import docker
client = docker.from_env()
print(client.containers)
for container in client.containers.list():
  print(container.id)

for image in client.images.list():
  print(image.id)

container = client.containers.run(image="fifth_try_docker_grillfarm", command=['bin/sh'])
print(type(container))
result = container.exec_run('main.py -h')
result = container.exec_run('echo 2')

container.stop()
