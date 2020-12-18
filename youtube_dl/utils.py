def make_time(time):
    hour = 0
    minute = time // 60
    if minute > 59:
        hour = minute // 60
        minute = minute % 60
    second = time % 60

    if hour != 0:
        return "%s:%s:%s" % (str(hour), str(minute), str(second))
    else:
        return "%s:%s" % (str(minute), str(second))


def make_size(size):
    mb = 0
    kb = size // 1024 + 1
    if kb > 1024:
        mb = kb // 1024
        left = (kb % 1024) // 100

    if mb != 0:
        return "%s.%s MB" % (str(mb), str(left))
    return "%s KB" % kb
