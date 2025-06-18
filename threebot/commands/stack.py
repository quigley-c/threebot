# stack command

desc = 'Provides a stack for manipulating commands'
usage = 'stack [push|pop|peek] [command|sound]'

global_stack = []

def execute(data, argv):
    if len(argv) < 1:
        data.reply(f'Invalid usage: {usage}')
        return
    
    if argv[0] == 'push':
        # add command or sound to the stack
        if len(argv) < 2:
            data.reply(f'Invalid usage: stack push [sound|alias]')
            return
        global_stack.push(argv[1])
        return

    if len(global_stack) < 1:
        data.reply(f'The stack is empty. Add something with \'stack push [sound|alias]\'')
        return
    top = global_stack[0]
    parts = top[0].split(' ')
    mods = []
    if len(parts) > 1:
        mods = parts[1:]
    if argv[0] == 'pop':
        # execute command or sound and remove from the stack
        data.util.play_sound_or_alias(parts[0], mods)
        global_stack.pop()
        return
    
    if argv[0] == 'peek':
        # returns the top of the stack to the user
        data.reply(f'{top}')
        return

#execute
