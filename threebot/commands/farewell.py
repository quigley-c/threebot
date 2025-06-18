# Farewell command.

desc = 'Sets or unsets your farewell sound.'
usage = 'farewell [CODE|ALIAS]'

def execute(data, argv):
    c = data.db.conn.cursor()

    c.execute('SELECT * FROM farewells WHERE username=?', [data.author])
    res = c.fetchall()

    if len(argv) > 0:
        newval = ' '.join(argv)

        # check if username is already in db
        c.execute('SELECT * FROM farewells WHERE username=?', [data.author])

        if len(res) == 0:
            param = (data.author, newval)
            c.execute('INSERT INTO farewells VALUES (?, ?)', param)
        else:
            param = (newval, data.author)
            c.execute('UPDATE farewells SET farewell=? WHERE username=?', param)

        data.reply('Set farewell to {0}.'.format(newval))
    else:
        if len(res) > 0:
            c.execute('DELETE FROM farewells WHERE username=?', [data.author])
            data.reply(f'Removed farewell (previous farewell was {res[0]})')
        else:
            data.reply('Farewell is not set! Set it with "!farewell SOUND".')

    data.db.conn.commit()
