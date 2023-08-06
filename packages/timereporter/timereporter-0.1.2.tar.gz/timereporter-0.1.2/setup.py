# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timereporter', 'timereporter.commands', 'timereporter.views']

package_data = \
{'': ['*']}

install_requires = \
['camel>=0.1.2', 'colorama>=0.4.1', 'tabulate>=0.7.7']

setup_kwargs = {
    'name': 'timereporter',
    'version': '0.1.2',
    'description': 'Report working time from the command line.',
    'long_description': '# timereporter\nReport working time from the command line.\n\n[![Build status](https://ci.appveyor.com/api/projects/status/2qfkospugig8y9m6?svg=true)](https://ci.appveyor.com/project/Godsmith/timereporter)\n[![codecov](https://codecov.io/gh/Godsmith/timereporter/branch/master/graph/badge.svg)](https://codecov.io/gh/Godsmith/timereporter)\n\n## Requirements\n\nPython 3.6+, Windows/Linux/Mac.\n\n## Installation\n\nClone the repo and run `python setup.py install` in the root folder.\n\n### Yaml file path\n\nThe default path of the `timereporter.yaml` file that stores the calendar data\nis `%USERPROFILE%\\Dropbox\\timereporter.yaml`. To change this, set the\nTIMEREPORTER_FILE environment variable to the new path, e.g.\n\n```\nsetx TIMEREPORTER_FILE "C:\\mypath\\timereporter.yaml"\n```\n\n### Alias\n\nIt is recommended to set an alias for `python -m timereporter`, e.g. in .bashrc:\n\n```\nalias t=\'python -m timereporter\'\n```\n\nThe usage documentation below assumes that the above alias is set.\n\n\n### Customization\n\nAfter running once, the `timereporter.yaml` file will be created. In this file, the following options can be set:\n\n#### Default project name\n\nTo set another name for the default project, change the `default_project_name` variable. The default value is EPG Program.\n\n#### Target hours per day\n\nTo set the target hours per day, edit the `target_hours_per_day` variable. The\ndefault value is 27900 seconds.\n\n\n## Usage\n\n### Report time on default project\n  \n    t [<day> | [last | next] <weekday>] [came <time>] [left <time>] [lunch\n    <time>]\n\n`<time>` must be in one of the following formats: `9`, `9:00`, `0900`...\n\nAdditionally, lunch times can also be in one of the following formats: `45m`, `45 min`, ... \n\n`<day>` must be one or more of\n- `yesterday`,\n- `monday`, `Tuesday`, ..., or\n- an ISO 8601 date, e.g. `2017-04-01`.\n\nIf `<day>` is not set, today\'s date will be used.\n\n`<weekday>` must be one or more of `monday`, `Tuesday`, ...,\n\n### Create a new project\n\n    t project new [--no-work] <project-name>\n\nIf `<project-name>` is multiple words, enclose them in quotation marks, e.g.\n`"My new project"`.\n\nTime reported on projects tagged with `--no-work` reduces the required\nworking time for that day. This can be used e.g. for part-time parental leave.\n\n###   Report time on a project\n    t project (<project-name> | <project-number>) [<day>] <time>\n\nThere is no need to spell out the entire `<project-name>`, a part of it is\nenough. `imp` for `My important project`, for example.\n    \nSee also Report time on default project.\n\n###   Show reported time\n    t show [last | next] week [html] [--show-weekend]\n    t show <month> [html] [--show-weekend]\n    t\n\n`html` shows the specified week in a browser windows instead of in the console.\n\nBy default, Saturday and Sunday are not shown, but this can be changed by adding `--show-weekend`.\n\n`<month>` must be one of `january`, `february`, ...\n\n`t` is an alias for `t show week`.\n\n###   Show flex time\n    t show flex [--from=<date>] [--to=<date>]\n\n###   Undo/redo\n    t (undo | redo)\n\n###   Show help text\n    t (help | --help | -h)\n\n##   Examples\n    t last friday came 9 left 17 lunch 45m\n\nReports a working time from 09:00 to 17:00 last Friday.\n\n    t yesterday left 17:15\n\nChanges yesterday\'s leave time to 17:15.\n\n    t project new --no-work My new project\n\nCreates a new non-working project called My new project.\n\n    t project My new project 2017-09-23 04:00\n\nReports four hours worked on My new project the 23rd of September.\n\n    t show last week html\n\nShows Monday-Friday of last week in the browser.\n\n    t show october --show-weekend\n\nShows all days of October in the console.\n\n\n## Running tests\n\npytest test\n',
    'author': 'Filip Lange',
    'author_email': 'filip.lange@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Godsmith/timereporter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
