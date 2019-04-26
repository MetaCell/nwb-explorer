import quantities as pq

def guessUnits(label):
    if not hasattr(pq, label):
        l = label.lower().replace(' ', '')
        if 'milisec' in l:
            return 'ms'
        elif 'sec' in l:
            return 's'
        elif 'milivol' in l:
            return 'mV'
        elif 'volt' in l:
            return 'V'
        elif 'picoamp' in l:
            return 'pA'
        elif 'nanoamp' in l:
            return 'nA'
        elif 'microamp' in l:
            return 'uA'
        elif 'miliamp' in l:
            return 'mA'
        elif 'amp' in l:
            return 'A'

    return label 