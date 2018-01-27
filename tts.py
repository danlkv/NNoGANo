# -*- coding: utf-8 -*-
from gtts import gTTS
from pydub import AudioSegment
import codecs
import numpy as np
import json
import sox
import time
import sys
from settings import *
import os.path
reload(sys)
sys.setdefaultencoding('utf-8')

words= json.load(open('words.json'))
lyr = codecs.open('lyrics.txt',encoding='utf-8')
words=lyr.read().decode('utf-8')
print words
words=words.replace(",", "").replace('\n',' ').split(' ')
#print np.array(words).astype('U')
words=[w for w in words if len(w)>0]
lyr.close()
print (words)
ww=[]
i=0
UPD = True
print len(words)
while i<len(words):
    if len(words[i])<3:
        ww.append(' '.join(words[i:i+3]))
        i = i+3
    elif len(words[i])<5:
        ww.append(' '.join(words[i:i+2]))
        i = i+2
    else:
        ww.append(' '.join(words[i:i+1]))
        i+=1
print ww
print len(ww)
words=ww
#words=' '.join(words)
f = open('lyrics.json','w+')
f.write(json.dumps(words, ensure_ascii=False).encode('utf-8'))
f.close()
words= json.load(open('lyrics.json'))

words = json.loads(json.dumps(words))
#print [w.encode('utf-8') for w in words]
words=[w for w in words if len(w)>0]
print words

def save_tts(words):    
    for w in set(words):
        if len(w)==0:
            continue
        if  os.path.isfile(TMP_DIR+w.replace(' ','%20')+'.mp3') :
            print "skipping"+w.replace(' ','%20')
            continue
        print "Processing word ",w
        tts = gTTS(text=w,lang='ru',slow=False)
        w = w.replace(' ','%20')
        tts.save(TMP_DIR+w+'.mp3')
        print "got tts result"

def effects(words):
    for w in set(words):
        w = w.replace(' ','%20')
        waud = AudioSegment.from_mp3(TMP_DIR+w+'.mp3')
        waud.export(ORIG_DIR+'orig'+w+".wav", format="wav")
        cbn = sox.Transformer()
        cbn.pitch(-5)
        cbn.treble(11.0)
        #cbn.allpass(50)
        #cbn.bass(5.)
        #cbn.flanger(delay=10)
        cbn.reverb(reverberance=20)
        cbn.gain(gain_db=1.0)
        #cbn.noiseprof('orig'+w+'.wav','noiseprof')
        #cbn.noisered('noizeprof', amount=0.5)
        cbn.tempo(1.2)
        cbn.loudness(4.0)
        #cbn.convert(samplerate=8000)
        # create the output file
        cbn.build(ORIG_DIR+'orig'+w+'.wav', WAV_DIR+w+'.wav')
if (UPD):
    save_tts(words)
effects(words)
