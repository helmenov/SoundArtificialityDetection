import os
import pandas as pd
import numpy as np
import librosa
from audioread.ffdec import FFmpegAudioFile as ar
from soundfile import SoundFile as sf

def set_data(path_to_zipfile):
    """set PA files in _data

    You can download PA.zip from [ASVspoof2019 on Edinburgh DataShare](https://datashare.ed.ac.uk/handle/10283/3336)

    Args:
        path_to_zipfile (str): path to the downloaded zip-file 'PA.zip'.

    """
    data_dir = os.path('_data')

    if os.path.exists(data_dir) == False:
        os.mkdir(data_dir)

        # extract
        with zipfile.ZipFile(path_to_zipfile) as existing_zip:
            existing_zip.extractall(data_dir)
        #os.remove('path_to_zipfile')

#######################################
# Physical Attack, Counter Measure
#######################################
class PA_CM:
    _columns = ['SPEAKER_ID','AUDIO_FILE_NAME','ENVIRONMENT_ID','ATTACK_ID','KEY']
    def __init__(self, datadir:str='_data', protocol:str='train')->None:
        """class PA_CM constructor

        Args:
            datadir (str, optional): path where the PA.zip extracted. Defaults to '_data'.
            protocol (str, optional): protocol {'train', 'dev','eval'}. Defaults to 'train'.
        """
        self.protocol = protocol
        self.datadir = datadir
        if protocol == 'train':
            tsv = os.path.join(self.datadir, "ASVspoof2019_PA_cm_protocols", "ASVspoof2019.PA.cm.train.trn.txt")
        elif protocol == 'eval':
            tsv = os.path.join(self.datadir, "ASVspoof2019_PA_cm_protocols", "ASVspoof2019.PA.cm.eval.trl.txt")
        elif protocol == 'dev' :
            tsv = os.path.join(self.datadir ,"ASVspoof2019_PA_cm_protocols", "ASVspoof2019.PA.cm.dev.trl.txt")

        self.BASE_dir = os.path.join(f"{self.datadir}", f"ASVspoof2019_PA_{protocol}","flac/")

        _df = pd.read_csv(tsv, header=None, sep=" ", names=PA_CM._columns)
        self.SPEAKER_names = np.array([f"PA_{i:04d}" for i in range(1000)])
        self.ENVIRONMENT_names = np.sort(pd.unique(_df['ENVIRONMENT_ID']))
        self.ATTACK_names = np.sort(pd.unique(_df['ATTACK_ID']))
        self.KEY_names = np.array(["bonafide","spoof"])

        self.SPEAKER = np.array([j for i in _df['SPEAKER_ID'].values for j, n in enumerate(self.SPEAKER_names) if i==n])
        self.ENVIRONMENT = np.array([j for i in _df['ENVIRONMENT_ID'].values for j, n in enumerate(self.ENVIRONMENT_names) if i==n])
        self.ATTACK = np.array([j for i in _df['ATTACK_ID'].values for j, n in enumerate(self.ATTACK_names) if i==n])
        self.KEY = np.array([j for i in _df['KEY'].values for j, n in enumerate(self.KEY_names) if i==n])
        self.BASE_names = _df['AUDIO_FILE_NAME'].values

    def query_byIDname(self, speaker_name:str=None, environment_name:str=None, attack_name:str=None, key_name:str=None):
        """query info by parameter ID names.

        Args:
            speaker_name (str, optional): speaker_IDname such as 'PA_0001'. Defaults to None.
            environment_name (str, optional): environmen_IDname such as 'aaa' from {'aaa',...,'ccc'}. Defaults to None.
            attack_name (str, optional): attack_IDname such as 'AA' from {'-', 'AA',...,'CC'}. Defaults to None.
            key_name (str, optional): key IDname such as 'bonafide' from {'bonafide', 'spoof'}. Defaults to None.

        Returns:
            NDArray of PA_CM_Audio objects queried.
        """
        queries = np.array([speaker_name, environment_name, attack_name, key_name])
        names = np.array([self.SPEAKER_names, self.ENVIRONMENT_names, self.ATTACK_names, self.KEY_names],dtype=object)
        table = np.array(["speaker", "environment", "attack", "key"])
        qid = dict()
        for i, q in enumerate(queries):
            if q is not None:
                qq = np.where(names[i]==q)[0]
                qid.update({table[i] : qq})

        print(f'{queries=},{qid=}')
        return self.query_byIDnumber(**qid)

    def query_byIDnumber(self, speaker:int=None, environment:int=None, attack:int=None, key:int=None):
        """query info by parameter ID numbers

        Args:
            speaker (int, optional): speaker ID number such as '12'. Defaults to None.
            environment (int, optional): environment ID number such as '3' from 0 to 8. Defaults to None.
            attack (int, optional): attack ID number such as '2' from 0 to 5. Defaults to None.
            key (int, optional): key ID number such as '1' from 0 to 1. Defaults to None.

        Returns:
            NDArray of PA_CM_Audio objects queried
        """
        queries = np.array([speaker, environment, attack, key],dtype=object)
        table = np.array([self.SPEAKER, self.ENVIRONMENT, self.ATTACK, self.KEY])
        cond = True
        for i, q in enumerate(queries):
            if q is not None:
                cond &= (table[i] == q)
        ans = list()
        for sfile in self.BASE_names[cond]:
            ans.append(PA_CM_Audio(protocol=self,sfile=sfile))
        return np.array(ans)


class PA_CM_Audio:
    def __init__(self, protocol, sfile=None, speaker_name=None, environment_name=None, attack_name=None, key_name=None):
        """_summary_

        Args:
            protocol (class PA_CM): class PA_CM object name
            sfile (str, optional): basename of flac file. if None, you must specify all the names of speaker, environment, attack and key instead. Defaults to None.
            speaker_name (str, optional): speaker's ID name {PA_nnnn}. if None, you must specify sfile instead. Defaults to None.
            environment_name (str, optional): environment's ID name {from 'aaa' to 'ccc'}. if None, you must specify sfile instead. Defaults to None.
            attack_name (str, optional): attack's ID name {from '-' ,'AA' to 'CC'}. if None, you must specify sfile instead. Defaults to None.
            key_name (str, optional): key ID name {'bonafide' or 'spoof'}. if None, you must specify sfile instead. Defaults to None.

        Raises:
            ValueError: _description_
        """
        if sfile != None:
            speaker = protocol.SPEAKER[protocol.BASE_names == sfile]
            environment = protocol.ENVIRONMENT[protocol.BASE_names == sfile]
            attack = protocol.ATTACK[protocol.BASE_names == sfile]
            key = protocol.KEY[protocol.BASE_names == sfile]
        elif np.all(np.array([speaker_name, environment_name, attack_name, key_name]) != None):
            speaker = np.where(protocol.SPEAKER_names == speaker_name)[0]
            environment = np.where(protocol.ENVIRONMENT_names == environment_name)[0]
            attack = np.where(protocol.ATTACK_names == attack_name)[0]
            key = np.where(protocol.KEY_names == key_name)[0]
            sfiles = protocol.BASE_names[(protocol.SPEAKER == speaker) & (protocol.ENVIRONMENT == environment) & (protocol.ATTACK == attack) & (protocol.KEY == key)]
            if len(sfiles) > 0:
                for i,f in enumerate(sfiles):
                    print(f"{i}:{f}")
                i = int(input(f'which one?[0--{i}]'))
                sfile = sfiles[i]
        else:
            raise ValueError('You must define all of speaker_name, environment_name, attack_name and key_name')

        path = os.path.join(protocol.BASE_dir ,  sfile+".flac")
        #assert os.path.exist(path)
        self.protocol, self.path, self.sfile, self.speaker, self.environment, self.attack, self.key = protocol.protocol, path, sfile, speaker, environment, attack, key
        self.info = dict(
            protocol = self.protocol,
            path = self.path, sfile = self.sfile,
            speaker_name = protocol.SPEAKER_names[self.speaker], attack_name = protocol.ATTACK_names[self.attack],
            environment_name = protocol.ENVIRONMENT_names[self.environment], key_name = protocol.KEY_names[self.key]
        )

    def read(self):
        """read audio file and update info to add length, num of channels, sampling frequency, and data-array
        """
        lenx = 0
        chx = 0
        try:
            x, fs = librosa.load(sf(self.path))
        except RuntimeError as e:
            print(f'libsndfile echoes "{e}". then use audioread')
            try:
                x, fs = librosa.load(ar(self.path))
            except Exception as e:
                print(f'Unexpected error {e}')
            else:
                lenx = len(x)
                chx = x.ndim
        except Exception as e:
            print(f'Unexpected error {e}')
        else:
            lenx = len(x)
            chx = x.ndim
        self.x, self.fs, self.lenx, self.chx = x, fs, lenx, chx
        self.info.update(fs=self.fs, lenx=self.lenx, chx=self.chx)

    def show(self):
        """show information of PA_CM_Audio object class
        """
        print(f'='*10)
        for k in self.info:
            print(f'{k}: {self.info[k]}')
        print(f'='*10)

