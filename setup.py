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
    'version': '0.2.3',
    'description': '',
    'long_description': "# Sound Artificiality Detection\n\nなりすまし音の人工性を検出するプロジェクト\n\n## package\n\n- ASVspoof2019protocol.py\n\t- ASVspoof challenge 2019のプロトコルを扱うためのモジュール\n\t- 現在は，PA(Phisical Attack,物理的攻撃,録音再生音)のCM(Counnter Measure)プロトコルのみ対応．後段の認証撹乱のプロトコルは対象にしていない．\n\t- LA(Logical Attack,論理的攻撃,人工合成音)は手を付けていない．\n\n### ASVspoof2019protocol.PA_CM クラス\n\n### ASVspoof2019protocol.PA_CM_Audio クラス\n\n\n## install \n\nインストールは，\n\n> python -m pip install git+https://github.com/helmenov/SoundArtificialityDetection.git\n\n## 使い方\n\n[ASV2019protocolの使い方](SAD_protocol.ipynb)\n\n```{python}\nfrom SoundArtificialityDetection.ASV2019protocol import PA_CM, PA_CM_Audio\n\n# 別途，[ASVspoof2019 on Edinburgh DataShare](https://datashare.ed.ac.uk/handle/10283/3336) から，PA.zipをダウンロードし，\n# 例えば，`data`に解答したとする．`./data/PA/...`という状況で，\n\n# プロトコルのデータリストの読み込み\ntrain = PA_CM(datadir = './data', protocol='train')\n\n# 条件による音響信号クラス(PA_CM_Audioオブジェクト)のリストを獲得\nsndlist = train.query_byIDname(key_name='spoof', attack_name='CC', environment_name='aaa')\n\n# 獲得したリスト内のPA_CM_Audioオブジェクトの情報を表示\nsndlist[1].show()\n\n# ふつうにPA_CM_Audioオブジェクトを作る\nsnd1 = PA_CM_Audio(train, speaker_name='PA_0079', environment_name='aaa', attack_name='CC', key_name='spoof')\n\n# 音響信号ファイル名でも作れる．\nsnd2 = PA_CM_Audio(train, sfile='PA_T_0007085')\n\n# 情報表示\nsnd2.show()\n\n# 実際に音響信号データを読み込むとき. snd.xでデータを参照できる．\nsnd1.read()\n\n```\n",
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
