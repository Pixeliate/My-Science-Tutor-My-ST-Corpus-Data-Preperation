import os
import re
import sys
from typing import Dict, List

if len(sys.argv) != 2:
    print("Usage: python data_prep.py [MyST_root] [sph2pipe]")
    sys.exit(1)
#MyST_root = '../../../../../../Desktop/Shreya/myst-v0.4.2/data'
MyST_root ='/home/speechlab/Desktop/Shreya/myst-v0.4.2/data'
task = sys.argv[1]

#checking line to be skipped
def checking(line_c):
    flag = 0
    lc = ['','<nosignal>','<sidespeech>','<noise>','<fp> ','<indiscernible>','<silence>','<laugh>','<disturbance>','<no voice>','<breath>','<discard>','<laugh>']
    for x in lc:        
            if line_c == x: flag = 1
            #new  line to remove  containing numbers
            elif any(char in line_c for char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', '(', ')', ']', '/', '<', '>']):
                    flag = 1
    if flag: return 0
    else: return 1

rep_dict = {'[INDISCERNIBLE]': '', '(())': '', '(*)': '', '.': '', '?': '', '-': '', '_': '', 
            ';': '', ':': '', '\n': '', '\\': '', '"': '', '+': '', '*': '', '&': ' and ', '<[^>]+>': ''}

def multiple_replace(string:str, rep_dict:Dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)

def process_text(text:str):
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = multiple_replace(text, rep_dict).lower()
    text = re.sub(' +', ' ', text).strip()
    return text

with open(os.path.join(MyST_root, task, task + "_Trans_wav0_25.txt"), 'r') as wav_trans_f , open(
            os.path.join("data", task, "text"), "w", encoding='utf-8') as text_f , open( 
            os.path.join("data", task, "wav.scp"), "w" , encoding='utf-8') as wav_scp_f, open(
            os.path.join("data", task, "spk2utt"), "w" , encoding='utf-8') as spk_utt_f , open(
            os.path.join("data", task, "utt2spk"), "w" , encoding='utf-8') as utt_spk_f:

    text_f.truncate()
    wav_scp_f.truncate()
    spk_utt_f.truncate()
    utt_spk_f.truncate()
    wav_trans = sorted(wav_trans_f.readlines(), key=lambda s: s.split(" ")[0])
    #wav_trans = wav_trans_f.readlines()
    for line in wav_trans:
        linei = line.split('\t',1)
        #print(linei)
        label_prep = re.split('/|\.' , linei[0])
        #print(label_prep)
        try: 
            label1 = str(str(label_prep[-3]) + str(label_prep[-2]))
            label = label1.replace("_", "").replace("-","")
            #print(label + '..........' +  task)
            #print(linei[1])
            text = process_text(linei[1])
            result = checking(text)
            if(result == 1):
                    text_f.write(label+ "\t" + text.lower() + "\n")
                    wav_scp_f.write(label + "\t" + linei[0] + "\n")
                    spk_utt_f.write(label + "\t" + label + "\n")
                    utt_spk_f.write(label + "\t" + label + "\n")
        
        except:
            pass
text_f.close()
wav_scp_f.close()
spk_utt_f.close()
utt_spk_f.close()
wav_trans_f.close()