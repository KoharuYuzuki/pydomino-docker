import pydomino
import numpy as np
import librosa
import os
from glob import glob

def main():
  wav_file_paths = sorted(glob('wav/*.wav'))
  phonemes_list = []

  with open('phoneme.txt') as file:
    for line in file:
      stripped = line.rstrip()

      if stripped != '':
        phonemes_list.append(stripped)

  assert len(wav_file_paths) == len(phonemes_list)

  alignmer = pydomino.Aligner('/pydomino/onnx_model/model.onnx')

  for i, wav_file_path in enumerate(wav_file_paths):
    print(F'aligning: {i + 1} / {len(wav_file_paths)}')

    wave, _ = librosa.load(wav_file_path, sr=16_000, mono=True, dtype=np.float32)
    phonemes = phonemes_list[i]
    result = alignmer.align(wave, phonemes, 3)

    basename_without_ext = os.path.splitext(os.path.basename(wav_file_path))[0]
    lab_file_path = os.path.join('lab', F'{basename_without_ext}.lab')

    with open(lab_file_path, mode='w', encoding='utf-8') as file:
      for x in result:
        file.write(F'{x[0]}\t{x[1]}\t{x[2]}\n')

if __name__ == '__main__':
  main()
