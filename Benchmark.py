from timeit import default_timer as timer

disable = True

globalTimers = {}
globalTimersConfig = {
    'Full turn': True,
    'Total CF': True,
    'Input': True,
    'Model': True,
    'Deepcopy': True,
    'Play turn': True
}


def tt(name, on=0, padding=0):
    if disable:
        return
    if not (name in globalTimers):
        globalTimers[name] = [0, 0, 0, padding]

    if not (name in globalTimersConfig):
        globalTimersConfig[name] = True

    if not globalTimersConfig[name]:
        return

    curr = globalTimers[name]
    if on:
        curr[0] = timer()
        curr[2] += 1
    else:
        curr[1] += timer()-curr[0]


def printTimers():
    if disable:
        return
    for key, value in globalTimers.items():
        if globalTimersConfig[key]:
            padding = '\t'*value[3]
            print(f'Timer: {padding}{key} {value[1]} times: {value[2]}')


