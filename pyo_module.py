from pyo import *
import os
import itertools

hardcode_sample = [220.0, 350.0, 440.0, 546.0, 880.0, 523.0]
hardcode_duration = 60
name_sample = "record1"


s = Server(audio='offline').boot()

# Path of the recorded sound file.
path = os.path.join("./wav_files", f"{name_sample}.wav")

s.recordOptions(dur=hardcode_duration, filename=path, fileformat=0, sampletype=1)

#fqs = Linseg(hardcode_sample)
fqs2 = SigTo(220, time=5, init=200)
synth = SineLoop(freq=fqs2, mul=.2).out()
#synth = SineLoop(freq=fqs, mul=.2).out()
def pick_new_freq():
	fqs2.value = 350
pat = Pattern(function=pick_new_freq, time=20).play()


#fqs.play()


s.recstart()
s.start()


s.shutdown()





