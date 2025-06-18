# Sound play command.

import random

desc = "Plays a sound from the local collection."
usage = "s [CODE] [normal|fast|slow|muffle|chorus|echo|up|down|reverse|reverb]*"

def execute(data, argv):
    target = data.db.random_sound() if len(argv) < 1 else argv[0]

    mods = [] if len(argv) < 2 else argv[1:]

    if len(argv) == 0:
        for i in range(2):
            if random.random() < 0.05:
                mods.append(random.choice(('loud', 'slow', 'down', 'chorus', 'echo', 'up', 'muffle', 'reverse', 'reverb')))

    modstr = ''

    if len(mods) > 0:
        modstr = f" [{' '.join(mods)}]"
    
    data.audio.play(target, mods)
    data.reply('Playing {}{}.'.format(target, modstr))
