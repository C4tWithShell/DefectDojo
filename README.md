# DefectDojo

## Overview

This script is made to provide the following functionalities:
- find instances by tags
- stop and start instances
- handle specific jenkins_cron ignore flag

## Requirements

- Python3.7 or higher

- For development you will need `pip` or `pipenv`:
  ``` bash
  sudo apt install pipenv
  # or
  sudo apt install python3-pip
  ```
  
- For the container you will need `docker`:
  ```
  curl -L https://get.docker.com | sh -
  ```

## Overview

This folder contains two dockerfiles:
- Django image
- Nginx image based on django

Original images were modify to support LDAP

- LDAP:
  - `DD_LDAP_SERVER_URI`: by default set to the string with ldap servers
  - `DD_LDAP_BIND_DN`: username that are needed to connect to the LDAP servers. Empty by default
  - `DD_LDAP_BIND_PASSWORD`: password that are needed to connect to the LDAP servers. Empty by default
  - `DD_LDAP_GROUP_SEARCH_BASE`: should be set to the ou=defectdojo,...
  - `DD_LDAP_ADMIN`: group(cn) within `DD_LDAP_GROUP_SEARCH_BASE`, will set users to admin

### Docker Hub

Image was containerized:
```
docker build . -t docker.soramitsu.co.jp/build-tools/defectdojo-django:2.33.1 -t docker.soramitsu.co.jp/build-tools/defectdojo-django:latest -f Dockerfile.django
docker push docker.soramitsu.co.jp/build-tools/defectdojo-django:2.33.1

docker build . -t docker.soramitsu.co.jp/build-tools/defectdojo-nginx:2.33.1 -t docker.soramitsu.co.jp/build-tools/defectdojo-nginx:latest -f Dockerfile.nginx
docker push docker.soramitsu.co.jp/build-tools/defectdojo-nginx:2.33.1
```


Alternative commands to build:
```
docker buildx build --platform linux/amd64 . -t docker.soramitsu.co.jp/build-tools/defectdojo-django:2.35.2 -t docker.soramitsu.co.jp/build-tools/defectdojo-django:latest -f Dockerfile.django

docker buildx build --platform linux/amd64 . -t docker.soramitsu.co.jp/build-tools/defectdojo-nginx:2.35.2 -t docker.soramitsu.co.jp/build-tools/defectdojo-nginx:latest -f Dockerfile.nginx
```