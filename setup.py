# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soundartificialitydetection']

package_data = \
{'': ['*']}

install_requires = \
['SoundFile>=0.10.3,<0.11.0',
 'japanize-matplotlib>=1.1.3,<2.0.0',
 'librosa>=0.9.2,<0.10.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'soundartificialitydetection',
    'version': '0.2.2',
    'description': '',
    'long_description': '---\njupyter: python3\n---\n\n```{python}\nimport pandas as pd\nfrom importlib import resources\nimport numpy as np\nimport os\nfrom SoundArtificialityDetection.ASV2019protocol import PA_CM, PA_CM_Audio\n```\n\n# Phisical Attack, Counter Measure \n\n\n## protocolごとのデータリストの読み込み\n\n```{python}\n#datadir = os.path.join("/Volumes","labo_share5","04_研究資料", "18_SoundSpoof", "ASVspoof2019","PA")\ndatadir = os.path.join("../datadir")\n\ntrain = PA_CM(datadir=datadir,protocol=\'train\')\neval = PA_CM(datadir=datadir,protocol=\'eval\')\ndev = PA_CM(datadir=datadir,protocol=\'dev\')\n```\n\n## 条件によるファイルリスト獲得\n\n```{python}\na = train.query_byIDname(key_name=\'spoof\',attack_name=\'CC\',environment_name=\'ccc\') # 条件にあてはまるファイル(PA_CM_Audio形式)をNDArrayに出力\na[1].show() \n```\n\n## 音響信号ファイルの読み込み\n\n```{python}\n# ID nameによる音響信号ファイルのPA_CM_Audio objectの作成\nsnd = PA_CM_Audio(train, speaker_name = \'PA_0079\', environment_name = \'aaa\', attack_name = \'CC\', key_name = \'spoof\')\n\n# 音響信号ファイルの名前によるPA_CM_Audio objectの作成\nsnd2 = PA_CM_Audio(train, sfile=\'PA_T_0007085\')\n\n# 実際に音響信号ファイルを読み込むときは，readメソッド．self.xにデータが入る．\nsnd2.read()\n```\n\n## PA_CM_Audio objectの情報を表示\n\n```{python}\nsnd2.show()\n```\n\n',
    'author': 'Kotaro SONODA',
    'author_email': 'kotaro1976@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
