# Walk through command sources in this directory and initialize them.

import importlib
import os
from os import path

MAX_DEPTH=32

dir_path = os.path.dirname(os.path.realpath(__file__))
command_dict = {}

print('Registering commands..')

for f in os.scandir(dir_path):
    if path.isfile(f.path) and path.basename(f.path) != '__init__.py':
        name = str(path.basename(f.path)).split('.')[0]
        spec = importlib.util.spec_from_file_location(name, str(f.path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, 'execute'):
            raise RuntimeError('Command {} does not have an execute() method!'.format(name))

        if not callable(module.execute):
            raise RuntimeError('Command {} "execute" is not callable!'.format(name))

        print('    > {}'.format(name))
        command_dict[name] = module

print('Registered {} command{}.'.format(
    len(command_dict),
    's' if len(command_dict) > 1 else ''
))

# Register built-in help command

def execute_help(data, argv):
    rows = []

    def esc(s: str):
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        return s

    for name in sorted(command_dict.keys()):
        if len(argv) > 0 and name not in argv:
            continue

        rows.append([
            name,
            command_dict[name].desc,
            esc(command_dict[name].usage) if hasattr(command_dict[name], 'usage') else '',
        ])

    pages = data.util.into_pages(['Command', 'Description', 'Usage'], rows, 32)

    for p in pages:
        data.reply(p)

command_dict['help'] = lambda: None
command_dict['help'].desc = 'Gets help information on one or more commands.'
command_dict['help'].execute = execute_help

def execute(data, argv, depth=0):
    """Executes a command."""

    if depth > MAX_DEPTH:
        data.reply('<img alt="" src="data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD//gAfQ29tcHJlc3NlZCBieSBqcGVnLXJlY29tcHJlc3P/2wCEAAQEBAQEBAQEBAQGBgUGBggHBwcHCAwJCQkJCQwTDA4MDA4MExEUEA8QFBEeFxUVFx4iHRsdIiolJSo0MjRERFwBBAQEBAQEBAQEBAYGBQYGCAcHBwcIDAkJCQkJDBMMDgwMDgwTERQQDxAUER4XFRUXHiIdGx0iKiUlKjQyNEREXP/CABEIAKUArgMBIgACEQEDEQH/xAAdAAAABwEBAQAAAAAAAAAAAAAAAQIDBAUGBwgJ/9oACAEBAAAAAPNurfjVK3gZJBhYACYz9sxWk7FJFgSdbj5LSgE1leWhDohRVYjfTBu2WaaqgVyJMpFkZjMwdLmek3MB/ouB2PBBLBGzcmChZ2567pARHGf5tiyZddkygRFrdTbAgYBY7mD8p0zASVr0ayCek01JSvFicYAZm2IVcXUN2iZtt42nO8Y5SYMGM+w9JR0/ZkvujyWXqnx5GMwDpCbD/X74F0fXVkym0nF+FgzNWZkSpZbnYFH1+2tl0NlzXz4tRmIagAvoG42mU6zIJmvwHndQUYhmYMl6/wBKWMtRJiYjzQowoQg4CCxcewXSJKU+W8moKEIKWYBN+zLQk17bOC4GswIpgGYOs9l6ANJ4Nyk1AwqMAsAM5n3hPUnh/HzWDAVFJZoDVAr2fpDZ8PWE0wsGIoMkwqpiR6t7TXy/EmJ1LhgzOCFoq61yI/s/pU6nwdwe40K1BJwQ7CoVnFZX9KOiF4n82I3jpgD/xAAbAQABBQEBAAAAAAAAAAAAAAABAAIFBgcDBP/aAAgBAhAAAACxLkDFez0IJw4MiIeq3e29H+cwOcUsusW9leZZ1ltqPjteqpMNFxywznSx3xFigsQl50e3TnFiPizuKXfWvSmImj042a3yaTxF5zHSWrdEmmv1B8pwl7SVybmYfYfPEaZ0X//EABwBAAEFAQEBAAAAAAAAAAAAAAABAwUGBwIECP/aAAgBAxAAAACDaaOJfxeYV1vl12YmLVTKu/1Gk/o925IHEukj3NI1Ctr66rmQL3ctZgY1qtUhRzib2SMhl8maKKh6tDlV8+UNgCXi2c1qo+EAmdV8zWP8gpctRj83nvHQQH/oRtvH5PQMM4T/xABFEAACAQIDAwgGBwQJBQAAAAABAgMEEQASIQUxQRATICIyUWFxBhRSgZGhMDNCYrHB0RUjU3IHNVRzgqLC4fCDkpOy0v/aAAgBAQABPwGCikks0t1Xu44jjjiGSNAo8OSSZVNjct7K6nEzzurW6nHL324X/TC82ADGOoRcf88OjoN+PEfQxaZ4uK9ZfLF7ccXw8qppfX2d5wXkfjkHcN/xwFVRZRpyJ1HaHg13Tz4jEs0cIu5392uIp4pvq393Hl6wsUNmBuPPFRRCaJayiGjrmaL8cvji2YFb/wDP1GOZdIIpybxt1c3ENusf16JI3nElVFH9rN4DHPTyMGjjy23FvHHq7HV5WJ8NMF5X3dQf5jhUA4e/jyzSrBG0h4fPAcVMKyIbPvXzGKhFqqcFF13geI3jCMVN1JDLuOIZBLEklt+/3cuyJbwyw/w2uPJsbTou1VQr/eDvHtDGyHVvWaZxcOM9jqDwOKykakcAawt2D+XJJURR9psetSyaQxHzbQY5mR9ZpT5LhYkTsqMXxfo7TB5hf5vyxRSZJcn2X/EYXqSZPsSajwcfrippn9YXmkY842iqNb8Rii2NWCECYxx7/E/LH7Gl/tMf/Yf1xJsurTshHH3WsfgcbOWaCu5uSNl5yJt/3deTmfUNqUxH1MzFV82HZxPAlRC8T7iND3eOJYKoSPHUSZSpsVXCQRJ9nXvOvRYr9o29/RmiEsbRnEuzKyGFZ8okgto8euW3A8RbCMainRgCWa1re34YoKIUy87MAalx1iNy/dXw6TxRy5OcW+Rw6+DLuwN2NtQ5JoZlH1gyt5ri4wcF1G84Akbsp720xzBPbkJ/l0/XCwom5R+fz6WyJ8kr099HGdPNd+PUaYVC1Sx2cX3aDzt38t+ltxR6mrH7Mq/PT88Wlbclh3sfywIAfrGLeG4YVFXsKF8voKOkesLZZAiqbHi/w/PFPSwUy/u49TvY7z7+VDCsqNVZjT7nCMVt97TeMNsWjdc0LzLm1uJMw+d8PsOoXWKoR/BxlPxGnyw9BXJ26RtOKEOP1wZFU5HORvZfqn4Hl2vMp5unVusGzsO7TQH6GSeKPtSAHu449ZkfSKI+b4VJc4keZsw3ZdMbKrKueRo5GDqiXLN2vAcjAkEA2Nt/dikpJ6qJxHUo1RF9ZFKLf4gw4Hyxsd6mJ5tn1NPInNjPEWHVyneAw0NuVlVxldAy9x1HzxJsfZ76iDmz3xMU+Q0x6QwVOy5oPV6mTmJVOrWJzjhfThgjeeJNyemarNpDEW8ToMZJpPrZrD2UwkMadlB+OL93JsWPLTSS21kkPwGnLHO1JPFWILmPtr7SHtD88Iyuqup6rC48jyvIkK55DZeJxe9rYr6aCspZKephMqNwG8HvXxGJoJaaV4J43SRDYhxlNu+3Stjx5GcL2iBhWZ+xGT59UYEMh7clvBcbLXLQU6gbgf8A2PQ2HNmpmp/4D5R/IdVwsqOhcHqgnU+BtiXaNFBFJUS1CiGMXdxdlUeJF8JULKgkjinMbC4b1eXKQf8ADiiqYhJNRo3OZLNEIwXbI32bDXqkWw61SxvL+z6jm1UsWIRbAa7nYHG2pKfbPo+m24KacQq68zOwW2r5CpsSbY0xbFugBK2qxe9tPlgU7H6yQ+S6fPCQxx6qmvfvPxxbTFsbKn6r0rb16y+IP+/IbDjjnYtBnGpyjzxsZ8tdIn8SD5xn/fFH1HqIjGjyRSsVecc5ZX6wyJoB3X36Yq432hTy0ldUSS08q5Xi0VSPcL4hRqZEigqJ0VAFQCVjl4favg1e0fXKuUVMskAjhjdosolJXMTuHWtfhY4EcMwziWWRW3M08jA/FsekKUVBsZqWENGJWVYoUkdU0bOTlBtpi1rYHRt0QWUqyGzLqCMUu0opcqTERy/5W8jjZ8EdTVEVC3hhi54rwbXq+Y8MNUGeGVamkHqRbmiUNyvjbwPEY2bFJT7YFNL24opgfvDq2b34yJzhlt18uW/hyqioLIoAvfD0iksySzRZjciJ8ov8Dja/o6KxXqUrJ2qETqiZwyWGtt2nngai/A/SEXFjr542DtFdmbQV5nPqrpzT3PVj10byGI0mjkYx5ZIJX5xTm1S44d44jHNR84Jsi85kyZuOXfby6F8SySof3cGfxzBcbaq9q0+zp5YKeJNLM3OF2VDoWAyjdi3Du6NuW2LdC3jiiq5KSWnUTSilEyF4VchCpOotwxYDQcNPd0iMwKsAQRYg8b42xsptl1WRdaeQnmW8vsnywMWxboW6b9hz904pH5ylpX9qFD/l5SQNTuwaumG+dPxwaykUFjUxgd7NYfPH7QoP7bT/APlX9cbe2rsmWgqKUTJUSuLIidaze1fhbG/X6S2KiUqrogu2QnwAtjZn9XbO7/Vo/wAOVlDaEXwciAmwAHuGNu7fhrI5KCiXNEe3KRo1tbJ+uLLvyj4Yt0bdG2Lckj82rP3YcPzUg3sfmx0xTpzUEEfsRovwHKcelm1Qrw7IR9XGeb/Sh/HkAxbFsWxbFsDFuk7rGAX0vu8fLEsjSNFcWGe+UeHfjXhv4eeNlVwrqKjmK5HkhVsp/Ed4xri+JJFijeVr5UUsba6DFXM1dPPVTduZy5+73D3DEDc5GCe1ubzGLfSSy5DkXV/w88WNyzm7d+D9cg+435cnoBPS7RoqvYdaiuad+fgvwR9+U8LNiTYMoJNLtFwPYnUSj4izfE4OytqrxpJPe8f458U+x6wzwy1ksIiRw/NRhiWK7rsbaA67seklMKPb+2adRZRVMw/6iiT/AFYSfmJVzDqOOse4jjjfu1HA/RzTamKM6gdZvZ/3wFtyH65f5GwxCi5OPR7av7I2vQbRzfuQ+SX+5fRvhvwNfy5Dj+kKHmvSV2A+tpIX992X8sO4KkpqV62KWQK3MX6hBMf/AM/RTyGKJ3AF8L1Rffrflb69f5G/EYTrkyH7LFQO62Mo50J9mRbkY9E6mSt9HdkTzG78wFJ78nUv77cv9JwttPZjDe1K4J/x4lGVc43ovy7sRk8ypG9FzjzXCnMqnvUH4i/Qtyf/xAAmEAEAAgEDBAIDAQEBAAAAAAABABEhMUFREGFxoYGRILHB8NEw/9oACAEBAAE/EM5wXUz88THQbTUvKwYCZWmR8m3zLIU29m5q9IE4CLs7PljrUYoXphTwf+GrXMNV1nvLU+HMSC8dp3TIrPIMnxqeZrPct/PQfEY0Vqjl6f8AMgR7TMOrDQBihLEyuz2lkZaUAL2NkHiCJkf0BxWjKWkUSzCP+PEz/wBtWhZjxZZuIOllJZRoVLly4AUoIthqsakpryGFw+dYadgEdCph8ncpL9E0OrvfJ7s8xmgC8HLiVGjzDaPmUg1dnTFEBaLlAcP8YYqVQcOD9p0uo28d31/2S1yhp/Rcm5EBa1rDG96qWO6gbR59+OSZobqpWICbDb9Rt0TIveiCZ8m973BMcvwYmhujfypbXrCXt/2JVbUP+RshjdqvOAPcbQ7FczuUin9YglBVeQ8DXuHh4GmNJbMMus4ezHMYkmzr+Dkl8haAtex8Rjq/aN77y0Sy7idruXUuEBWJtYldWboVg9zRgxYLYS2bqN9IiMg9aGjyWc4vcTrZ8r62mk44NoxyrnZqxalsNpatSVeQfkY2OcRZAiNDfBlmoJ3f1LYaKOAe7aWec6uFeXquM1p5itu6Vt1eqVA8e6VShHFNnpZpvKcxQq0L5jZqV+DTrWhV3lIcOlbrThAL7I/QZnyeUpqHiulPR6LRcVEFlETjb5fUWDd5+T+OgWhn4j068Bfxobj5gcOAKYS7qpl+f2S/m36Qi2T+IKz+prdOg+tZ37X8SzFOukMvDCboI8hZXEqV2ldoHafEWql7RavmD6EVVh4oq/8AFvFvatoR1xVXWrCEQ2yAAq5phs4DMx0wvAUpsWVotujerdYMHEdJWYqYjIifAZc5LYBHyPpLfI4J3ugO5EtbXKbVd1lSn8VvatP7cfrnUfc0893L3GhhBvchrZMPwvd9WyWaGv8AJHcgokDBhCxPMdOjg5oJoW0XwQyNHNRVZjj411VrEQADAS47CbzSH4CZgBF+pbwwMRHS2akXN/bn1NlfB/WBioeW3qOCK9a5rWv1DTKUhLQBcl4LJV4Hdkqwgmf5khGG2iNyl/efNZG2dkYKI2FAwDssEUhQG6CjUxA4gnSWGUwOYTI4DGi/qAGFuYPtb9VEkRuX7Fs1DmWlTlK8uUh3FmU1gvxEC7C+1c+I3OCdlgrQt3jnWDezOmHojMxwbb8lRt3HXfNYqfMKz0nAUAZoIEBIhwG7aTJrPaDibQvSJRJUfWl6azEANOx6mEshKlhKYS7NJVfg7127D/x3iT35aT6r7MtqzTtkATZyu5qElWQPoL1wJWwx5lQ26XCeBDel3KGwealRLEgIiVC9Vt95icRLhvVrUd41/wAtLQcM0ipFsBPD0xxDodQlSpUsqrVdLIIraEbAgN5CmubhK6XBCugI6chmGGj0Je9EnLNQOi1HBxAAgS7G93DExTaARN+TRmFAAAAA4CpUqBAnlKlaw7p5ypUvtLbrzo8SvQo6yBQDdtQeo1jNqadXMcZn1XYqG+OAKGFfNw1Y81aMludnJKIZmUO6BKgTymSVKlSpmzEaG1HK5C47evc2x1BUAaq0BGK8gaerhU9qAju0lbrmdfbFpi72JxTgQJTc5YfhUqVM8SpUqU1gGLUuoWXzN8KLXrDBAbpLIUwxdAALy4AhH2gaEjuCzMrO5zolKoKODEbW4dS3MqVKgSkpKhP6Gw7uhKcXDs1Tc9y+wv5QSD0VCyjVj2lX9jMAgZuBmUlJX8QqBK6oVsAyrsgeSJ7AbHvuIinWpcbGLjt3y0Uvv9sm8wBlrzNJUGUhaAasv+DhsR+qoPEplj/agJUCVKgSpUqutQ6gc02PK/kc1Yq01jIN7EcFk5wa4vuFLb9AZ+Z/li9HdHqiLtdtFXdjAoZJK4uuqK+oGAvVY4Hj6awqirC+SVPEp4gMpgPHUDEqMVAj3n+eIQoN71zfRU/+rI9rml7LwR0KBfZUZ40/GZRNIqoCnHBApw8uUejE0GlDXDlgtZ58bvgbSrVNIH4DN6lQNI5cBq9nAfuERZNi7rvF6ChkbaOxQ3eWIMLUjQTHu4txWza22PORjpEsZe2jp2JAAQYnfcuzFNUJd/8Ai7zENYPiiCVKlJRP/8QANhEAAgEDBAADBgIJBQAAAAAAAQIDAAQRBRIhMQYQQRMUIlFSYSBxByMkMjM0Q2Jyc4GR4fH/2gAIAQIBAT8ASNIuTTS/RTGt1YJOB3V3q9vY3FrHcrsSfIEx5G4eh+VPdW8JiDvt9qRsLdN+X4AG9KPPkzYcJU2EVpi21V7PoKk8UaLCfZm/QuOzyRXia70vVdGnNtcxSGEiRAGweO+KstXk1HR7jS7ls3EKe2tX/wBPnbXhPXW1e0MEx/aYR8X3HzoIx76pVRTwPi/Br9zc2Fr7/boHSI/GD6r9q8Q+K21WOC2tRJFFjMy5wWb/AG9KJrkDI9aR3jPtIyQR614TujZ67ZAOcSnYw+zUTknA4DEVjy67oHPRrxjYayYnvffFNivDRZ2/+0BuIBIGT2atLV1iEU0EUiYyrD1FSaXay8mLYf7TT6KP6cnP3rwt4SuVubfVLqaMwRtuQK2Sxrdu66JJ8xCRyWzQCL0K/SBO8ekQxLwskyn/AKrs9Vo9zIyGBm+JeR/jSI8nCIzfkKEE2Meyf/g1oNzc2cvsHgkML9ZHANHjacYzQ8sH6q214i0ZdZ054M/rlbfGfQNR0q7S79yuImjcHsjuodMexuYJFbK/EGNG9m2qiSFMfSAAaW+uQGDSMQfvWnXBN5btNdyIm8Z5JoDgdEHkEeoNY8sViuavLCC9iMc0Sk44YDkGtU0+bTnVGfcrdeRq2kWGWOR496qwJFWk8VxBHLAw2OowK2mgvzrFYPkBnqvFksLG1RGy4JyB6eQ7HGftVh4bluoRcSSmIN0pFaXpi6XCYFlMgJ3ZPoTWTWTWDWBWVJwKvr+K0R1MmJNpwo7Bq6MkoD8sSxZmrj51phEU8dxIgZFbo1GwkjjdcFNoINYHlgVuomtV1gWy+724Bk+qmleVi8jFmPbHurRlR9rjKPxTadaMeY+aubWKK3xGMDNaHqGQtnOSAP4deuKxWPKclbW6IOCBxTMWkYsSTSUP3qi5Cf41e/y5/OkZhPbkHBDrUXKEns48/wD/xAAxEQACAQMCBAQEBgMBAAAAAAABAgMABBEFEgYhMWEQEyJBICNRcRQVMlKBkUJDcqH/2gAIAQMBAT8AaTfTSYpn3VzonAzVnpE+oWt1NaMZJIMM8I67PrUVrcTLMyJu8nm4XqM+/iAx6UIHIBNM+4eHl/K3DrUGZGWFV3MeijqaThbXJ1LpYOFI5DkD/wC1wxb6npGuwi4tJUjmDRPlcj1dOdXujLp2twapZxAW058m6T/v/KuK+Hzpl0JrVAttMd32PuKWFV5t1oLj7UPHh+3ttQufy2d9hlHokHVX79q4d4TGkyT3N2Y5pc/JYjIVe3ehRG4jcOlMiSDY4BBNcUWy3mj3RZBmPDg9xXMhST1yayKyB0Hhsb9tcH3GjRyR2/4Ui8PWTG7+ielE4GQM1dThpi8Mzq2cFT0FJeXEfINuHek1Nh+uMGuJOJ4mhm063jYSuAH3DAUdq/T6Sc4OPDIpYkHtWRXBECSapNIeflRFv5Jx4alAkbiVV5P1P0IppI0AZ5FVe5pruAf7kx9xWuwWV1EJ47hPOXrg8yKHuCfHcfDQNWbSL9J8ZQnY/cGvzO1az/FQSq6kdQakvxdQyqQAfTspbC3y7yRh3J5liT/QptOtiVKxLkdq1G2AsrhYrRTJsOCAM115kYIGCPitL24tJQ8UjAZ5qTyIrTL+LUUdgm0xkA9j4Y54q6geaGWOOXazKQDVxBLbytFOPWGPP4jXC0FzHHJPJGVhlHpJ5ZYeDFhzzjvV9xJHbTGKOIS7ThmB5VqOoNqE5mMYQYxgfDz+laRo93qcsbRwnyA673bkMZq9jS2a3jDBYRGEVegyK2nqOf2qazlv4Lm2gfbJ5JbNPG0TvG4IcMQw7j4M1ke9cOcMSaiy3l5mO0Jyv1ehBFbQxwW8YRFKgKorX7YXVhIsTfNh+YoHXI61HqV7FgLKcd64bvJptU+bKfXGyj+K4t0ILJLqloMoWHnAdFP1+G0RXurVHGVLcxVuqpbwxIoCLGMKOgq4JCqR9VoqPIibHNi2TVwNs8oHICQiuHyRq1rz/dWoqpjniI9DwvuX2NOAHcDoCMf14NX/2Q==" />')
        raise Exception('maximum command depth exceeded')

    # drop command indicator if needed
    while argv[0][0] == '!':
        argv[0] = argv[0][1:]

    # Try and resolve a built-in command
    if argv[0] in command_dict:
        try:
            return command_dict[argv[0]].execute(data, argv[1:])
        except Exception as e:
            raise Exception('{}: {}'.format(argv[0], e))
    
    # Try and resolve an alias
    alias = data.db.resolve_alias(argv[0])

    if alias is None:
        raise Exception('{} is not a recognized command or alias'.format(argv[0]))

    next_argv = alias[1].split(' ') + argv[1:]

    # Drop command indicators from expanded argv
    while next_argv[0][0] == '!':
        next_argv[0] = next_argv[0][1:]

    # Expand alias and recombine arguments
    return execute(data, next_argv, depth + 1)
