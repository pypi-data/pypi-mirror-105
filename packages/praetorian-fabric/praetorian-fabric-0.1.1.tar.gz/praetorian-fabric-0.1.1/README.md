# praetorian-fabric

Gladiator Titus in your service. I like heavy weights 🏋️. More strength, more praetorian, more fabric. 
What more do you want? Gimme that heavy variables 💪.

## Introduction

Praetorian Fabric library extends standard `fabric` library, to maintain communication
with praetorian services. Main purpose is to make necessary connections and provide
suitable data.

## Installation

```python
# pip
pip install praetorian-fabric

# pipenv
pipenv install praetorian-fabric

# poetry
poetry add praetorian-fabric
```

## Usage

####1. First you need to create environment variables:

- `PRAETORIAN_API_URL`
- `PRAETORIAN_API_KEY`
- `PRAETORIAN_API_SECRET`
- `PRAETORIAN_USERNAME`
- `PRAETORIAN_PASSWORD`

####2. Create `fabfile.py` folder in your project root directory
####3. Instantiate `PraetorianConfig` object:

```python
praetorian_config = PraetorianConfig(project_name='foo project')
```

####4. Create task and connect to Praetorian SSH Proxy to gain needed variables:

```python
@task
def deploy(ctx, remote_name):
    ctx = praetorian_config.connect(ctx, remote_name)
```
####5. Get variables by dot notation anywhere in your tasks:

```python
@task
def deploy(ctx, remote_name):
    ctx = praetorian_config.connect(ctx, remote_name)

    variable = praetorian_config.get_variable('variable_name')

    nested_variable = praetorian_config.get_variable('variables.nested_variable.name')
```
---
Developed with 💙 and ☕️ by [Adam Žúrek](https://zurek11.github.io/)
with the support of [BACKBONE s.r.o.](https://www.backbone.sk/), 2021 (C)
