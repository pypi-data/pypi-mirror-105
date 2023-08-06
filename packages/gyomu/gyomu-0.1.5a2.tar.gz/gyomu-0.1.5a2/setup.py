# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gyomu', 'gyomu.archive', 'gyomu.tasks']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2',
 'jsonpickle==2.0.0',
 'jsons==1.4.0',
 'pycryptodome==3.10.1',
 'pyzipper>=0.3.4,<0.4.0',
 'sqlalchemy==1.4.00']

setup_kwargs = {
    'name': 'gyomu',
    'version': '0.1.5a2',
    'description': 'Enterprise operational framework',
    'long_description': "*This package is originally developed in C#, and now try to migrate into Python version\n\n# Gyomu\nGyomu, which means Enterprise or Operation in Japanese, is used in enterprise.\nThe purpose of this library is \n1. Shorten development time through framework\n2. Shorten troubleshooting in testing or in production \n\nThis library won't be used by library itself. It's used with RDB ( Now Postgres & MSSQL is supported )\n\nThis library contains lots of function, but major functionality would be\n* Error handling / Logging\n* Various Parameter management\n* Task management\n* Milestone management\n* Others\n\n# Error handling / Logging\nAll status/ log to be stored in database\nBased on setting, status/log to be sent via email.\nLike log4net, etc, there are several logging type, such as Info / Warning / Business Notification / IT Error.\nFor IT error, the status/log contains stack trace so that developer could resolve issue very quickly.\nThe error is sent via email promptly so it doesn't take time to search inside log file.\n\nWhen you use this framework, at least all public method should return StatusCode object.\nStatusCode object contains error/log information and when it's instantiated, it would be recorded in DB and be sent via email if necessary.\n\nStatusCode's id is Int (32bit)\n1st 12bit is ApplicationID which must be unique per your library\n2nd 4bit is logging type, such as Info / Warning / Business Notification / IT Error.\nRemaining 16bit is Error ID which must be unique within your library.\nCombining these number lead to uniqueness among all libraries.\n\n```Python\n```\nThis is example of how to set StatusCode's id.\nRegarding CODE_GEN function's argument\n* ApplicationID\n* logging type\n* Error ID\n* Summary\n* Detail\n\nYour assigned ApplicationID must be registered in DB table, apps_info_cdtbl. apps_info_cdtbl column would be ApplicationID.\n1-4095 can be assigned and 1 is already used in Gyomu library.\nI would recommend you to set some rule by yourselves, such as common library would be <= 99, business logic library would be >=100 <500, Server side like web library would be >=500 <2000, GUI would be >=2000 or something like that.\n\nEmail recipient information need to be setup per ApplicationID on status_handler table. You can set To / CC address on this table.\n\n\n# Various Parameter management\n\nIn most programs, we tend to put external parameter on \n* Configuration file\n* Environment Variables\n\nAnd I believe this is very difficult to manage for proper environment.\nSometimes, parameter must be different per user, must be different per machine, etc.\n\nIn this framework, parameter would be saved in database.\nUsing Json serialization, mostly any kind of data to be parameterized easily.\n\nAlso this parameterization supports several kind of encoding/encryption\n* Base64 Encoding\n* AES Encryption\n* User specific encryption ( This is not supported in Python version so far)\n\nBase64 encoding can be used for easy masking.\nIt's easy to be decoded, but at a glance, we can't see raw value.\n\nAES Encryption can be used for storing DB connection string, etc\n\nUser specific encryption can be used for personal password.\nThe encrypted value can be decrypted only by encrypted user.\n\n\nThis example stores/retrieves string list parameter\n\n```Python\n```",
    'author': 'Yoshihisa Matsumoto',
    'author_email': 'yoshmatsumoto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
