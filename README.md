# Sound Artificiality Detection

なりすまし音の人工性を検出するプロジェクト

## package

- ASVspoof2019protocol.py
	- ASVspoof challenge 2019のプロトコルを扱うためのモジュール
	- 現在は，PA(Phisical Attack,物理的攻撃,録音再生音)のCM(Counnter Measure)プロトコルのみ対応．後段の認証撹乱のプロトコルは対象にしていない．
	- LA(Logical Attack,論理的攻撃,人工合成音)は手を付けていない．

### ASVspoof2019protocol.PA_CM クラス

### ASVspoof2019protocol.PA_CM_Audio クラス


## install 

インストールは，

> python -m pip install git+https://github.com/helmenov/SoundArtificialityDetection.git

## 使い方

[ASV2019protocolの使い方](SAD_protocol.ipynb)

```{python}
from SoundArtificialityDetection.ASV2019protocol import PA_CM, PA_CM_Audio

# 別途，[ASVspoof2019 on Edinburgh DataShare](https://datashare.ed.ac.uk/handle/10283/3336) から，PA.zipをダウンロードし，
# 例えば，`data`に解答したとする．`./data/PA/...`という状況で，

# プロトコルのデータリストの読み込み
train = PA_CM(datadir = './data', protocol='train')

# 条件による音響信号クラス(PA_CM_Audioオブジェクト)のリストを獲得
sndlist = train.query_byIDname(key_name='spoof', attack_name='CC', environment_name='aaa')

# 獲得したリスト内のPA_CM_Audioオブジェクトの情報を表示
sndlist[1].show()

# ふつうにPA_CM_Audioオブジェクトを作る
snd1 = PA_CM_Audio(train, speaker_name='PA_0079', environment_name='aaa', attack_name='CC', key_name='spoof')

# 音響信号ファイル名でも作れる．
snd2 = PA_CM_Audio(train, sfile='PA_T_0007085')

# 情報表示
snd2.show()

# 実際に音響信号データを読み込むとき. snd.xでデータを参照できる．
snd1.read()

```
