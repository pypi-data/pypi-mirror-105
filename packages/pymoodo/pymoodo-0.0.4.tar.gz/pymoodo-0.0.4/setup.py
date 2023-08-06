# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymoodo']

package_data = \
{'': ['*']}

install_requires = \
['asyncinit>=0.2.4,<0.3.0',
 'asyncio>=3.4.3,<4.0.0',
 'python-engineio>=3.14.2,<4.0.0',
 'python-socketio[asyncio_client]>=4.6.1,<5.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pymoodo',
    'version': '0.0.4',
    'description': 'Python client to communicate with Moodo API',
    'long_description': '# pymoodo\nPython client to communicate with Moodo API.\n\n# How to use\n```python\nimport asyncio\nimport sys\nimport logging\nfrom pymoodo import Controller\n\nasync def main(email, password):\n    controller = await Controller(email, password)\n\n    # Turn on MoodoBox\n    for id in controller.boxes:\n        controller.boxes[id].turn_on(100)\n        # controller.boxes[id].set_fan_speed(21)\n\n        controller.boxes[id].slots[0].set_fan_speed(100)\n        controller.boxes[id].slots[1].set_fan_speed(100)\n        controller.boxes[id].slots[2].set_fan_speed(100)\n        controller.boxes[id].slots[3].set_fan_speed(100)\n\n        for slot_id in controller.boxes[id].slots:\n            slot = controller.boxes[id].slots[slot_id]\n            slot.turn_on()\n            slot.set_fan_speed(100)\n\n        for slot_id in controller.boxes[id].slots:\n            slot = controller.boxes[id].slots[slot_id]\n            slot.turn_off()\n\n        controller.boxes[id].turn_off()\n\n        while True:\n            pass\n\nif __name__ == "__main__":\n    if len(sys.argv) == 3:\n        asyncio.get_event_loop().run_until_complete(main(sys.argv[1], sys.argv[2]))\n    else:\n        print(\'Run example with arguments <email> <password>\')\n```\n',
    'author': 'Alex van Assem',
    'author_email': 'avassem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/avassem85/pymoodo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
