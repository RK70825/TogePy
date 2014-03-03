def findBestOffTypings():
    seenTypes = {}
    typings = []
    for type1 in ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 
                  'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric',
                  'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']:
        for type2 in ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 
                      'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass',
                      'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']:
            if type1 == type2:
                currTyping = [type1]
                currEffDmg = sum(calcSTABTypes([type1]).values())
            else:
                currTyping = [type1, type2]
                currEffDmg = sum(calcSTABTypes(currTyping).values())
            if type2 + ' ' + type1 not in seenTypes.keys():
                seenTypes[type1 + ' ' + type2] = 1
                heapq.heappush(typings, (currEffDmg, currTyping))
    return [heapq.heappop(typings) for i in range(len(typings))]

def findBestDefTypings():
    seenTypes = {}
    defTypings = []
    for type1 in ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 
                  'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric',
                  'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']:
        for type2 in ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 
                      'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass',
                      'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']:
            if type1 == type2:
                currTyping = [type1]
                currEffDmg = sum(calcDefType([type1]).values())
            else:
                currTyping = [type1, type2]
                currEffDmg = sum(calcDefType(currTyping).values())
            if type2 + ' ' + type1 not in seenTypes.keys():
                seenTypes[type1 + ' ' + type2] = 1
                heapq.heappush(defTypings, (currEffDmg, currTyping))
    return [heapq.heappop(defTypings) for i in range(len(defTypings))]

def findBestTypings(use_f1 = False):
    seenTypes = {}
    typings = []
    for type1 in ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 
                  'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric',
                  'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']:
        for type2 in ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 
                      'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass',
                      'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']:
            if type1 == type2:
                currTyping = [type1]
                currDefEffDmg = 18.0*(1.0/sum(calcDefType([type1]).values()))
                currOffEffDmg = sum(calcTypeEff([type1]).values())
                if use_f1:
                    currEffDmg = f1(currDefEffDmg, currOffEffDmg)
                else:
                    currEffDmg = currDefEffDmg*currOffEffDmg
            else:
                currTyping = [type1, type2]
                currDefEffDmg = 18.0*(1.0/sum(calcDefType(currTyping).values()))
                currOffEffDmg = sum(calcSTABTypings(currTyping).values())
                if use_f1:
                    currEffDmg = f1(currDefEffDmg, currOffEffDmg)
                else:
                    currEffDmg = currDefEffDmg*currOffEffDmg
            if type2 + ' ' + type1 not in seenTypes.keys():
                seenTypes[type1 + ' ' + type2] = 1
                heapq.heappush(typings, (currEffDmg, currTyping))
    return [heapq.heappop(typings) for i in range(len(typings))]

def heapSort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]