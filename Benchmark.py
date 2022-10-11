from timeit import default_timer as timer

globalDict = {}

def tt(name, on=0):
    if not (name in globalDict):
        globalDict[name] = [0, 0]
    curr = globalDict[name]
    if on:
        curr[0] = timer()
    else:
        curr[1] += timer()-curr[0]
