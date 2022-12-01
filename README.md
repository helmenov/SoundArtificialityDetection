---
jupyter: python3
---

```{python}
import pandas as pd
from importlib import resources
import numpy as np
import os
from SoundArtificialityDetection.ASV2019protocol import PA_CM, PA_CM_Audio
```

# Phisical Attack, Counter Measure 


## protocolごとのデータリストの読み込み

```{python}
#datadir = os.path.join("/Volumes","labo_share5","04_研究資料", "18_SoundSpoof", "ASVspoof2019","PA")
datadir = os.path.join("../datadir")

train = PA_CM(datadir=datadir,protocol='train')
eval = PA_CM(datadir=datadir,protocol='eval')
dev = PA_CM(datadir=datadir,protocol='dev')
```

## 条件によるファイルリスト獲得

```{python}
a = train.query_byIDname(key_name='spoof',attack_name='CC',environment_name='ccc') # 条件にあてはまるファイル(PA_CM_Audio形式)をNDArrayに出力
a[1].show() 
```

## 音響信号ファイルの読み込み

```{python}
# ID nameによる音響信号ファイルのPA_CM_Audio objectの作成
snd = PA_CM_Audio(train, speaker_name = 'PA_0079', environment_name = 'aaa', attack_name = 'CC', key_name = 'spoof')

# 音響信号ファイルの名前によるPA_CM_Audio objectの作成
snd2 = PA_CM_Audio(train, sfile='PA_T_0007085')

# 実際に音響信号ファイルを読み込むときは，readメソッド．self.xにデータが入る．
snd2.read()
```

## PA_CM_Audio objectの情報を表示

```{python}
snd2.show()
```

