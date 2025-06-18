# Sound play command.

import random
import threading
import time

desc = "Delays a command for a random time."
usage = "delay COMMAND [ARGS...]"

def execute(data, argv):
    def thread_init(delay, cmd):
        time.sleep(delay)
        data.commands.execute(data, cmd)

    MIN_MINUTES = 10
    MAX_MINUTES = 30

    delay = 60 * random.randint(MIN_MINUTES, MAX_MINUTES)
    random.seed(time.time() + time.time())

    thr = threading.Thread(target=thread_init, args=(delay, argv))
    thr.start()

    data.reply('Delayed "{}".'.format(' '.join(argv)))
    print('DBG: delayed {} by {}'.format(' '.join(argv), delay))
