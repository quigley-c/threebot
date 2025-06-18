# Sound play command.

import random
import tempfile
import subprocess as sp
import shutil
from mimetypes import MimeTypes

ROTATION = 4

desc = "Assigns the bot comment image."
usage = "comment <IMAGE_URL>"

def execute(data, argv):
    payload = data.orig_message.removeprefix('!comment')

    # Cycle over
    for i in reversed(range(1, ROTATION)):
        print('cycling', i)
        try:
            print(f'Cycle comment {i-1} to {i}')
            shutil.copyfile(f'comment{i-1}', f'comment{i}')
        except Exception as e:
            print(f'Skip cycle: {e}')
            pass

    with open('comment0', 'w') as f:
        f.write(payload)

    comment_rotation = 0
    comment_payloads = []

    while True:
        try:
            with open(f'comment{comment_rotation}', 'r') as f:
                comment_payloads.append(f.read())
                print('Loaded comment payload')
        except Exception as e:
            print(f'Stopped loading comment at {comment_rotation}: {e}')
            break

        comment_rotation += 1

    data.threebot.comment('<br>'.join(comment_payloads))
    data.reply('Successfully updated comment')
    return
