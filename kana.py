import pydomino
import numpy as np
import librosa
import os
import subprocess
import re
from glob import glob

openjtalk_bin_file_path = '/usr/bin/open_jtalk'
openjtalk_dict_dir_path = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
openjtalk_hts_file_path = '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'
openjtalk_tmp_file_path = 'tmp.lab'

def gen_label(
  text: str,
  bin_file_path: str,
  dict_dir_path: str,
  hts_file_path: str,
  lab_file_path: str
) -> None:
  subprocess.run(
    F'echo "{text}" | {bin_file_path} -x "{dict_dir_path}" -m "{hts_file_path}" -ot "{lab_file_path}"',
    capture_output=True,
    text=True,
    shell=True
  )

def parse_label(label_file_path: str) -> list:
  with open(label_file_path, mode='r', encoding='utf-8') as file:
    label = file.read()

  lab_pattern = re.compile('^(?P<begin>[0-9]+) (?P<end>[0-9]+) [a-z]+\\^[a-z]+-(?P<phoneme>[a-z]+)\\+[a-z]+=[a-z]+\\/A:(?P<accent_pos>-*[0-9|a-z]+)\\+(?P<accent_num_1>[0-9|a-z]+)\\+(?P<accent_num_2>[0-9|a-z]+)', re.M | re.I)
  parsed = [x.groupdict() for x in re.finditer(lab_pattern, label)]

  return parsed

def kana2phoneme(kana: str) -> list[str]:
  gen_label(
    kana,
    openjtalk_bin_file_path,
    openjtalk_dict_dir_path,
    openjtalk_hts_file_path,
    openjtalk_tmp_file_path
  )

  parsed = parse_label(openjtalk_tmp_file_path)
  opnjtalk_phonemes = [x['phoneme'] for x in parsed]
  pydomino_phonemes = []

  for phoneme in opnjtalk_phonemes:
    if phoneme in ['ty', 'gw', 'kw']:
      for char in phoneme:
        pydomino_phonemes.append(char)
    elif phoneme == 'sil':
      pydomino_phonemes.append('pau')
    else:
      pydomino_phonemes.append(phoneme)

  return pydomino_phonemes

def main():
  wav_file_paths = sorted(glob('wav/*.wav'))
  kana_list = []

  with open('kana.txt') as file:
    for line in file:
      stripped = line.rstrip()

      if stripped != '':
        kana_list.append(stripped)

  assert len(wav_file_paths) == len(kana_list)

  alignmer = pydomino.Aligner('/pydomino/onnx_model/model.onnx')

  for i, wav_file_path in enumerate(wav_file_paths):
    print(F'aligning: {i + 1} / {len(wav_file_paths)}')

    wave, _ = librosa.load(wav_file_path, sr=16_000, mono=True, dtype=np.float32)
    kana = kana_list[i]
    phonemes = ' '.join(kana2phoneme(kana))
    result = alignmer.align(wave, phonemes, 3)

    basename_without_ext = os.path.splitext(os.path.basename(wav_file_path))[0]
    lab_file_path = os.path.join('lab', F'{basename_without_ext}.lab')

    with open(lab_file_path, mode='w', encoding='utf-8') as file:
      for x in result:
        file.write(F'{x[0]}\t{x[1]}\t{x[2]}\n')

if __name__ == '__main__':
  main()
