# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intents', 'intents.dialogflow_service', 'intents.model']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-dialogflow>=2.0.0,<3.0.0', 'pyyaml>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'intents',
    'version': '0.0.1',
    'description': 'Define and operate Dialogflow Agents with a simple, code-first, approach',
    'long_description': '# Intents ⛺\n\n**Intents** is a Python library to define and operate Dialogflow Agents with a simple,\ncode-first approach.\n\n> **disclaimer**: this project is not affiliated, associated, authorized,\n> endorsed by, or in any way officially connected with Dialogflow. The names\n> Dialogflow, Google, as well as related names, marks, emblems and images are\n> registered trademarks of their respective owners.\n\n## Project status\n\nThis project is still in early development stage, its API could change without\nnotice. This is a broad overview of the features that are planned and their\ncompletion status.\n\n| Feature           | State  | Note                                                                                |\n|-------------------|--------|-------------------------------------------------------------------------------------|\n| [Agent Definition](STATUS.md#agent-definition)  | 🟡     | Can define basic Intents, with examples, parameters and responses                   |\n| [Cloud Sync](STATUS.md#cloud-sync)        | 🟡     | Can export Agent to a valid Dialogflow ZIP. Cannot yet manage Google Cloud Projects |\n| [Prediction client](STATUS.md#prediction-client) | 🟡     | Can act as a client for predictions and triggers. Cannot receive webhook requests         |\n\nA more detailed view of the single features is reported in [STATUS.md](STATUS.md)\n\n## Install\n\n*Intents* can be installed with PIP as a standard Python package\n\n```sh\npip install intents\n```\n\n## Usage\n\nCheck out the included `example_agent/` to explore *Intents* approach to\nAgent definition. In short, that is a full Agent defined as a set of Python\nclasses (Intents and Entities) and YAML files (language resources).\n\n### Export Agent\n\nA Dialogflow-compatible Agent ZIP can be built as follows:\n\n```py\nfrom example_agent import ExampleAgent\nfrom intents.dialogflow_service.export import export\n\nagent = ExampleAgent(\'/path/to/service_account.json\')\nexport(agent, \'/any/path/ExampleAgent.zip\')\n```\n\n`ExampleAgent.zip` can be loaded into an existing Dialogflow project by using the\nstandard *"Settings > Export and Import > Restore from ZIP"* feature. Also via\nAPI, if you are familiar with it.\n\n### Predict Intent\n\nUploaded Agents can be accessed with a human-friendly API:\n\n```py\nfrom example_agent import ExampleAgent\n\nagent = ExampleAgent(\'/path/to/service_account.json\')\nresult = agent.predict("My name is Guido")\n\nresult                  # user_name_give(user_name="Guido")\nresult.user_name        # "Guido"\nresult.fulfillment_text # "Hi Guido, I\'m Bot"\nresult.confidence       # 0.84\n```\n\n### Trigger Intent\n\nSame goes for triggering intents:\n\n```py\nfrom example_agent import smalltalk\n\nagent = ExampleAgent(\'/path/to/service_account.json\')\nresult = agent.trigger(smalltalk.agent_name_give(agent_name=\'Ugo\'))\n\nresult.fulfillment_text # "Howdy Human, I\'m Ugo"\n```\n\n## Develop\n\n## Setup\n\nDependencies are managed with Poetry\n(https://python-poetry.org/docs/#installation). This is how you setup your\nenvironment:\n\n    poetry install\n\n## Build Documentation\n\nThis project is documented using Sphinx. This is how you build the documentation site:\n\n```sh\ncd docs/\npoetry run make html\n```\n\nDocumentation will be created in the `docs/_build/` folder.\n\n## Test\n\ntbd\n',
    'author': 'Dario',
    'author_email': 'dario.chi@inventati.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dariowho/intents',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
