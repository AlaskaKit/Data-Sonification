from pyo import *
import os
import itertools
from random import randint

hardcode_sample = [220.0, 350.0, 440.0, 546.0, 880.0, 523.0]
hardcode_duration = 60
name_sample = "record1"
frequencies = iter(hardcode_sample)

s = Server(audio='offline').boot()

# Path of the recorded sound file.
path = os.path.join("./wav_files", f"{name_sample}.wav")

# Setting the record options
s.recordOptions(dur=hardcode_duration, filename=path, fileformat=0, sampletype=1)

fqs2 = SigTo(value=220, time=8, init=200)
synth = SineLoop(freq=fqs2, mul=.2).out()


def pick_new_freq():
	try:
		fqs2.value = next(frequencies)
	except StopIteration:
		fqs2.value = hardcode_sample[-1]
		print("The array is over.")


pat = Pattern(function=pick_new_freq, time=10).play()



s.recstart()
s.start()


s.shutdown()





