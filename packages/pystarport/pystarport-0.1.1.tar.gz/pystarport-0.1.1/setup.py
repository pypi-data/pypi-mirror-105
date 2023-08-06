# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pystarport', 'pystarport.proto_python']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'bech32>=1.1.0,<2.0.0',
 'docker>=4.3.1,<5.0.0',
 'durations>=0.3.3,<0.4.0',
 'fire>=0.4.0,<0.5.0',
 'jsonmerge>=1.7.0,<2.0.0',
 'multitail2>=1.5.2,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'supervisor>=4.2.1,<5.0.0',
 'tomlkit>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pystarport = pystarport.cli:main']}

setup_kwargs = {
    'name': 'pystarport',
    'version': '0.1.1',
    'description': 'Spawn local devnets for cosmos-sdk chains',
    'long_description': 'pystarport is like a [cosmos starport](https://github.com/tendermint/starport)\nwithout the scaffolding feature. it\'s mainly used for development and testing. It\'s developed for the Crypto.org Chain, but\nit can also be used for any cosmos-sdk based projects.\n\n## Configuration\n\na typical configuration for a devnet is like this:\n\n```\nchainmaind:\n  cmd: chain-maind  # chain binary to use, optional\n  validators:  # genesis validators\n    - coins: 10cro\n      staked: 10cro\n    - coins: 10cro\n      staked: 10cro\n  accounts:  # genesis accounts\n    - name: community\n      coins: 100cro\n    - name: ecosystem\n      coins: 200cro\n    - name: reserve\n      coins: 200cro\n      vesting: "1d"\n    - name: launch\n      coins: 100cro\n  genesis:  # patch genesis states\n   app_state:\n     staking:\n       params:\n         unbonding_time: "10s"\n```\n\nThe `validators` section defines how many nodes to run, for each node, a home directory is initialized in\n`data/node{i}`, and a validator account with specified coins is created.\n\nThe `accounts` defines other non-validator accounts, they are created in `node0`\'s keyring.\n\nIn the `genesis` section you can override any genesis configuration with the same json path.\n\n## Usage\n\n```\nNAME\n    pystarport serve - prepare and start a devnet from scatch\n\nSYNOPSIS\n    pystarport serve <flags>\n\nDESCRIPTION\n    prepare and start a devnet from scatch\n\nFLAGS\n    --data=DATA\n        Type: str\n        Default: \'./data\'\n        path to the root data directory\n    --config=CONFIG\n        Type: str\n        Default: \'./config.yaml\'\n        path to the configuration file\n    --base_port=BASE_PORT\n        Type: int\n        Default: 26650\n        the base port to use, the service ports of different nodes are calculated based on this\n    --cmd=CMD\n        Type: str\n        Default: \'chain-maind\'\n        the chain binary to use\n```\n\n## Port rules\n\nThe rules to calculate service ports based on base port is defined in the\n[`ports.py`](https://github.com/crypto-org-chain/chain-main/blob/master/pystarport/pystarport/ports.py) module.\n\nFor example, with default base port `26650`, the url of api servers of the nodes would be:\n\n- Node0: http://127.0.0.1:26654\n- Node1: http://127.0.0.1:26664\n\n> The swagger doc of node0 is http://127.0.0.1:26654/swagger/\n>\n> The default rpc port used by `chain-maind` is `26657`, that\'s the default node0\'s rpc port, so you can use\n> `chain-maind` without change to access node0\'s rpc.\n\n## Supervisor\n\n`pystarport` embeded a [supervisor](http://supervisord.org/) to manage processes of multiple nodes, you can use\n`pystarport supervisorctl` to manage the processes:\n\n```\n$ pystarport supervisorctl status\nnode0                            RUNNING   pid 35210, uptime 0:00:29\nnode1                            RUNNING   pid 35211, uptime 0:00:29\n$ pystarport supervisorctl help\n\ndefault commands (type help <topic>):\n=====================================\nadd    exit      open  reload  restart   start   tail\navail  fg        pid   remove  shutdown  status  update\nclear  maintail  quit  reread  signal    stop    version\n```\n\nOr enter an interactive shell:\n\n```\n$ pystarport supervisorctl\nnode0                            RUNNING   pid 35210, uptime 0:01:53\nnode1                            RUNNING   pid 35211, uptime 0:01:53\nsupervisor>\n```\n\n## Cli\n\nAfter started the chain, you can use `chain-maind` cli directly, there are also some wrapper commands provided by\n`pystarport cli`. It understands the directory structure and port rules, also assuming `keyring-backend=test`, and there\nare shortcuts for commonly used commands, so arguments are shorter.\n\n```\n$ pystarport cli - --help\n...\n```\n\n## Transaction Bot\n\nA simple transaction bot that works for cluster created by pystarport as well as a local node\n\nCopy and modify `bot.yaml.sample` to `bot.yaml` with your desired bot configurations.\n\n### If you are running on a pystarport created cluster:\n1. Make sure you have provide the `node` for each job in the `bot.yaml`\n2. Run the command\n```\n$ pystarport bot --chain-id=[cluster_chain_id] - start\n```\n\n### If you are running on a local node\n```\n$ pstarport bot --node_rpc=tcp://127.0.0.1:26657 --data=/path/to/your/local/node/home/ - start\n```\n\n## docker-compose\n\nWhen used with `docker-compose` or multiple machines, you need to config hostnames, and you probabely want to use a same\n`base_port` since you don\'t have port conflicts, you can config the `validators` like this:\n\n```yaml\nvalidators:\n  - coins: 10cro\n    staked: 10cro\n    base_port: 26650\n    hostname: node0\n  - coins: 10cro\n    staked: 10cro\n    base_port: 26650\n    hostname: node1\n```\n\n`pystarport init --gen_compose_file` will also generate a `docker-compose.yml` file for you.\n\n## IBC\n\nIt can setup multiple devnets at once, and connect them with ibc relayer.\n\n```\nibc-0:\n  validators:\n    - coins: 10cro\n      staked: 10cro\n      base_port: 26650\n    - coins: 10cro\n      staked: 10cro\n  accounts:\n    - name: relayer\n      coins: 100cro\n  genesis:\n    app_state:\n      transfer:\n        params:\n          receive_enabled: true\n          send_enabled: true\nibc-1:\n  validators:\n    - coins: 10cro\n      staked: 10cro\n      base_port: 26750\n    - coins: 10cro\n      staked: 10cro\n      base_port: 26760\n  accounts:\n    - name: relayer\n      coins: 100cro\n  genesis:\n    app_state:\n      transfer:\n        params:\n          receive_enabled: true\n          send_enabled: true\nrelayer:\n  global:\n    timeout: 10s\n    light-cache-size: 20\n  paths:\n    demo:\n      src:\n        chain-id: ibc-0\n        port-id: transfer\n        order: unordered\n        version: ics20-1\n      dst:\n        chain-id: ibc-1\n        port-id: transfer\n        order: unordered\n        version: ics20-1\n      strategy:\n        type: naive\n```\n\nWith following commands to setup ibc, you are ready to play with ibc functionalities:\n\n```\n# spawn the devnets\npystarport serve --config ibc.yaml\n# setup ibc channel\nhermes -c data/relayer.toml create channel ibc-0 ibc-1 --port-a transfer --port-b transfer\n# start relayer process\nsupervisorctl -c data/tasks.ini relayer-demo\n```\n\n',
    'author': 'huangyi',
    'author_email': 'huang@crypto.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/crypto-org-chain/chain-main/tree/master/pystarport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
