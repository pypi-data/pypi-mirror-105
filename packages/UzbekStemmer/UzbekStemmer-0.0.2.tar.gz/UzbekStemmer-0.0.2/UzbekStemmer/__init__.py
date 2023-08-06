class UzbekStemmer:
    def QoshimchaniTekshirish(soz, qoshimcha):
        b = False
        if type(qoshimcha) != list:
            b = str(qoshimcha) == soz[-len(qoshimcha):]
        else:
            for x in qoshimcha:
                if (x == soz[-len(x):]):
                    b = True
                    break
        return b

    def QoshimchaniQirqish(soz, qoshimcha):
        if type(qoshimcha) != list:
            if UzbekStemmer.QoshimchaniTekshirish(soz, qoshimcha):
                return soz[:-len(qoshimcha)]
        else:
            for elem in qoshimcha:
                if UzbekStemmer.QoshimchaniTekshirish(soz, elem):
                    return soz[:-len(elem)]
        return soz

    def asos(soz, qoshimchalar, A , SuffixClass):

        stop = False
        #temp = ""
        Way=dict()
        #back = ""
        #oldRaw = 0
        for x in range(len(A)):
            y = 1
            while y < len(A[x]):
                if (type(A[x][y]) == list):
                    for elem in A[x][y]:
                        if UzbekStemmer.QoshimchaniTekshirish(soz, qoshimchalar[elem]):

                            # id=1 boshqa qoshimcha bor yo`qligini tekshirish
                            isgood = True
                            for i in range(1, len(qoshimchalar)):
                                if i == elem: continue
                                if type(qoshimchalar[i]) != list:
                                    if (UzbekStemmer.QoshimchaniTekshirish(qoshimchalar[i],
                                                              qoshimchalar[elem]) & UzbekStemmer.QoshimchaniTekshirish(soz,
                                                                                                          qoshimchalar[
                                                                                                              i])):
                                        isgood = False
                                        break
                                else:
                                    for j in range(len(qoshimchalar[i])):
                                        if (UzbekStemmer.QoshimchaniTekshirish(qoshimchalar[i][j],
                                                                  qoshimchalar[elem]) & UzbekStemmer.QoshimchaniTekshirish(soz,
                                                                                                              qoshimchalar[
                                                                                                                  i][
                                                                                                                  j])):
                                            isgood = False
                                            break
                                        if not (isgood):
                                            break

                            # id=2 qoshimchani qirqish
                            if isgood:
                                oldWord = soz
                                soz = UzbekStemmer.QoshimchaniQirqish(soz, qoshimchalar[elem])

                                if (len(soz) > 2) | (soz in ['u', 'bu', 'ol']):

                                    OldState=A[x][0]
                                    x = y - 1
                                    y = 0

                                    # create transition

                                    Final=True
                                    if A[x][-1]==-2:      Final=False

                                    transition={
                                        "SuffixClass": str(SuffixClass),
                                        "OldState": str(OldState),
                                        "SuffixNumber": elem,
                                        "Suffix": str(qoshimchalar[elem]),
                                        "NewState": str(A[x][0]),
                                        "Final": Final
                                    }
                                    Way[len(Way)+1]=transition

                                    #print(elem, " --> ", A[x][0])

                                    break
                                else:
                                    soz = oldWord
                                    stop = True
                                    break

                            else:
                                continue
                #Final
                elif A[x][y] == -1:
                    stop = True
                    break
                #Face way. Return to correct state
                elif A[x][y] == -2:
                    i = len(Way)
                    for x in range(i, 0, -1):
                        if Way[x]["Final"] == False:
                            soz = soz + Way[x]["Suffix"]
                            Way.pop(x)
                        else:
                            break
                    #soz += temp
                    stop = True
                    break

                y += 1

            if (stop): break

        return soz,Way

    def TensePerson(soz):
        qoshimchalar = {
            1: 'di',
            2: 'sa',
            3: 'm',
            4: 'k',
            5: 'lar',
            6: 'ng',
            7: 'ngiz',
            8: ['a', 'y'],
            9: 'man',
            10: 'miz',
            11: 'lik',
            12: 'san',
            13: 'siz',
            14: 'sin',
            15: 'gin',
            16: ['ing', 'ng'],
            17: ['ingiz', 'ngiz'],
            18: 'yap',
            19: 'ti',
            20: 'ar',
            21: 'mas',
            22: 'mi',
            23: 'kan',
            24: 'mish'
        }

        A = [
            ['A', 0, [1], [2, 14, 15, 16, 17, 20, 21], [3, 4, 6, 7], [5], [9, 10, 12, 13], [11], [22], [19], [23, 24],
             0, 0, -1],
            ['B', 0, 0, [8], 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['C', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['D', 0, 0, [1, 2], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['E', 0, [1], [2, 14, 15, 16, 17], [6, 7], 0, 0, 0, 0, [19], 0, [12, 13], 0, -2],
            ['F', 0, 0, [8, 18, 20, 21], 0, 0, 0, 0, 0, 0, [22, 23, 24], 0, 0, -2],
            ['G', 0, 0, [8], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['H', 0, [1], [2, 20, 21], [3, 4, 6, 7], 0, 0, [11], 0, [19], 0, [9, 10, 12, 13], [5], -2],
            ['I', 0, 0, [18], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['J', 0, 0, [20, 21], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['K', 0, 0, [8, 18], 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],
            ['L', 0, [1], [2], [6, 7], 0, 0, 0, 0, [19], 0, [12, 13], 0, -2]
        ]

        return UzbekStemmer.asos(soz, qoshimchalar, A, "Tense,Person suffixes")

    def Verb(soz):
        qoshimchalar = {
            1: ['gan', 'kan', 'qan'],
            2: 'moqda',
            3: ['ayotgan', 'yotgan'],
            4: 'moqchi',
            5: 'lay',
            6: 'ay',
            7: ['adigan', 'ydigan'],
            8: ['ayotir', 'yotir'],
            9: ['gancha', 'kancha', 'qancha'],
            10: ['guncha', 'kuncha', 'quncha'],
            11: 'gudek',
            12: ['gani', 'kani', 'qani'],
            13: ['ib', 'b'],
            14: ['uv', 'v'],
            15: ['ar', 'r'],
            16: ['ish', 'sh'],
            17: 'moq',
            18: ['moqlik', 'moqlig'],
            19: 'ma',
            20: 'may',
            21: 'mayin',
            22: ['maslik', 'maslig'],
            23: ['lik', 'lig']
        }
        A = [
            ['A', 0, [1, 3, 7, 8, 9, 10, 11, 12, 13], [2, 4, 5, 6, 14, 15, 16, 17, 18, 19, 20, 21, 22], [23], -1],
            ['B', 0, 0, [19], 0, -1],
            ['C', 0, 0, 0, 0, -1],
            ['D', 0, [1, 3], [2, 4, 5, 6], 0, -2]
        ]
        return UzbekStemmer.asos(soz, qoshimchalar, A, "Verb suffixes")

    def Relative(soz):
        qoshimchalar = {
            1: 'lat',
            2: ['tir', 'dir'],
            3: 'ir',
            4: 'sat',
            5: 'ar',
            6: ['in', 'n'],
            7: ['il', 'l'],
            8: 't',
            9: ['ish', 'sh'],
            10: ['gaz', 'kaz', 'qaz'],
            11: ['kiz', 'giz', 'qiz', "g'iz"],
            12: 'iz',
            13: 'ol'
        }
        A = [
            ['A', 0, [1, 3, 4, 5, 6, 8, 10, 11, 12], [2], [7, 9], [13], 0, -1],
            ['B', 0, 0, 0, 0, 0, 0, -1],
            ['C', 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 0, 0, 0, 0, -1],
            ['D', 0, [1, 3, 4, 5, 6, 7, 8, 9, 10, 11], 0, 0, 0, [2], -1],
            ['E', 0, [1, 3, 4, 5, 6, 8, 10, 11], [2], [7, 9], 0, 0, -1],
            ['F', 0, [3, 4, 6], 0, 0, 0, 0, -1]
        ]
        return UzbekStemmer.asos(soz, qoshimchalar, A, "Relative suffixes")

    def Derivational(soz):
        qoshimchalar = {
            1: ['lik', 'lig'],
            2: ['chilik', 'chilig'],
            3: 'on',
            4: 'aki',
            5: "do'z",
            6: 'dor',
            7: 'gar',
            8: 'in',
            9: 'iq',
            10: 'ma',
            11: 'ona',
            12: 'mand',
            13: 'oq',
            14: 'ot',
            15: 'qin',
            16: 'la',
            17: 'iz',
            18: 'ir',
            19: ['tir', 'dir'],
            20: 'lat',
            21: ['qich', 'kich', 'gich', "g'ich"],
            22: 'yi',
            23: 'siz',
            24: 'lan',
            25: 'lash',
            26: 'shunos',
            27: 'soz',
            28: 'zor',
            29: ['uvchan', 'chan'],
            30: 'paz',
            31: 'parast',
            32: 'parvar',
            33: 'xon',
            34: "xo’r",
            35: 'viy',
            36: 'vor',
            37: 'vorchi',
            38: 'voz',
            39: ['uvchi', 'vchi'],
            40: 'qoq',
            41: 'boz',
            42: 'kash',
            43: 'mas',
            44: 'li',
            45: 'kor',
            46: 'chi',
            47: 'dosh',
            48: 'doshli',
            49: 'gor',
            50: "go'y",
            51: 'goh',
            52: ['garchilik', 'garchilig'],
            53: 'a',
            54: 'iy',
            55: 'ak',
            56: 'an',
            57: 'at',
            58: 'larcha',
            59: 'ildoq',
            60: 'liq',
            61: 'simon',
            62: 'xona',
            63: ['imtir', 'mtir'],
            64: 'roq',
            65: 'don',
            66: 'bop',
            67: 'lay',
            68: 'layin',
            69: 'sira',
            70: 'lashtir',
            71: 'qila'
        }
        A = [
            ['A', 0, [1], [2],
             [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 26, 27, 28, 29, 30, 31, 32, 33,
              34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60,
              61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71], [21], [24, 25], [58], -1],
            ['B', 0, 0, 0,
             [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 22, 23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
              39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 0, 0, 0, -1],
            ['C', 0, 0, 0, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 0, 0, 0, -1],
            ['D', 0, 0, 0, 0, 0, 0, 0, -1],
            ['E', 0, 0, 0, [16, 17, 18, 19, 20], 0, 0, 0, -1],
            ['F', 0, 0, 0, [22, 23], 0, 0, 0, -2],
            ['G', 0, 0, 0,
             [22, 23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
              50], 0, 0, 0, -1]
        ]
        return UzbekStemmer.asos(soz, qoshimchalar, A, "Derivational suffixes")

    def Noun(soz):
        qoshimchalar = {
            1: ['im', 'm'],
            2: ['ing', 'ng'],
            3: ['imiz', 'miz'],
            4: ['ingiz', 'ngiz'],
            5: ['si', 'i'],
            6: 'ni',
            7: 'ning',
            8: 'da',
            9: 'dan',
            10: ['ga', 'ka', 'qa'],
            11: ['niki', 'iki'],
            12: 'dagi',
            13: 'day',
            14: 'dek',
            15: 'gina',
            16: 'mi',
            17: 'lar',
            18: 'san',
            19: 'man',
            20: 'siz',
            21: 'miz',
            22: 'kan',
            23: 'mish'

        }

        A = [
            ['A', 0, [1, 2, 3, 4, 5, 22, 23], [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], [16], [17], [18, 19, 20, 21], 0,
             0, 0, 0, 0, -1],
            ['B', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['C', 0, [1, 2, 3, 4, 5], 0, 0, 0, 0, 0, [17], 0, 0, 0, 0, -1],
            ['D', 0, [1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11, 12], 0, 0, 0, 0, [17], 0, 0, 0, 0, -1],
            ['E', 0, [1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], 0, 0, 0, [17], 0, 0, 0, 0, -1],
            ['F', 0, [1, 2, 3, 4, 5, 22, 23], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], [16],
             [18, 19, 20, 21], -1],
            ['G', 0, [1, 2, 3, 4, 5, 22, 23], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], [16], 0, -1],
            ['H', 0, [1], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['I', 0, [1, 2, 3, 4, 5], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            ['J', 0, [1, 2, 3, 4, 5], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], 0, 0, 0, -2],
            ['K', 0, [1, 2, 3, 4, 5], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], 0, 0, -1],
            ['L', 0, [1, 2, 3, 4, 5, 22, 23], 0, 0, 0, 0, 0, 0, [6, 7, 8, 9, 10, 11, 12], [13, 14, 15], [16], 0, -2]
        ]
        return UzbekStemmer.asos(soz, qoshimchalar, A, "Noun suffixes")

    def Prefixes(soz):
        Way=dict()
        qoshimchalar = {
            1: 'ba',
            2: 'be',
            3: 'bo',
            4: 'bar',
            5: 'no',
            6: 'ser',
            7: 'alla'
        }
        A = [
            ['A', 0, [1, 2, 3, 4, 5, 6, 7], -1],
            ['B', 0, 0, -1]
        ]
        B = [1, 2, 3, 4, 5, 6, 7]

        for x in B:
            if (str(qoshimchalar[x]) == soz[:len(str(qoshimchalar[x]))]) & (len(soz) - len(qoshimchalar[x]) > 1):
                soz = soz[len(str(qoshimchalar[x])):]
                transition = {
                    "SuffixClass": "Preffixes",
                    "OldState": "A",
                    "SuffixNumber": x,
                    "Suffix": str(qoshimchalar[x]),
                    "NewState": "B",
                    "Final": True
                }
                Way[len(Way) + 1] = transition
        return soz,Way

    def Number(soz):
        qoshimchalar = {
            1: ['inchi', 'nchi'],
            2: 'ta',
            3: 'tacha',
            4: 'larcha',
            5: 'ala',
            6: 'lab',
            7: 'ov',
            8: 'ovlab',
            9: 'ovlash',
            10: 'ovlashib',
            11: 'ovlon'

        }
        A = [
            ['A', 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], -1],
            ['B', 0, 0, -1]
        ]
        return UzbekStemmer.asos(soz, qoshimchalar, A, "Number suffixes")

    def JoinDict(dict1,dict2):
        for i in range(1,len(dict2)+1):
            dict1[len(dict1)+1] = dict2[i]
        return dict1

    def UzbekStemmer(word):
        words=[]
        ways=[]
        tempWord=""
        tempWay1=dict()
        tempWay2=dict()

    # way1 (Noun --> Number)
        tempWord=word
        tempWay1.clear()

        #Noun
        tempWord,tempWay2=UzbekStemmer.Noun(tempWord)
        tempWay1=UzbekStemmer.JoinDict(tempWay1,tempWay2)

        #Number
        tempWord,tempWay2=UzbekStemmer.Number(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        words.append(tempWord)
        ways.append(dict(tempWay1))



    # way2 (Noun --> Derivational --> Prefixes)
        tempWord = word
        tempWay1.clear()

        # Noun
        tempWord, tempWay2 = UzbekStemmer.Noun(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        #Derivational
        tempWord, tempWay2 = UzbekStemmer.Derivational(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        #Prefixes
        tempWord, tempWay2 = UzbekStemmer.Prefixes(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        words.append(tempWord)
        ways.append(dict(tempWay1))


    # way3 (Noun --> Verb --> Relative --> Derivational --> Prefixes)
        tempWord = word
        tempWay1.clear()

        # Noun
        tempWord, tempWay2 = UzbekStemmer.Noun(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        # Verb
        tempWord, tempWay2 = UzbekStemmer.Verb(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        # Relativa
        tempWord, tempWay2 = UzbekStemmer.Relative(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        # Derivational
        tempWord, tempWay2 = UzbekStemmer.Derivational(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        # Prefixes
        tempWord, tempWay2 = UzbekStemmer.Prefixes(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        words.append(tempWord)
        ways.append(dict(tempWay1))

    # way4 (TensePerson --> Verb --> Relative --> Derivational --> Prefixes)
        tempWord = word
        tempWay1.clear()

        # TensePerson
        tempWord, tempWay2 = UzbekStemmer.TensePerson(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        # Verb
        tempWord, tempWay2 = UzbekStemmer.Verb(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        # Relativa
        tempWord, tempWay2 = UzbekStemmer.Relative(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        # Derivational
        tempWord, tempWay2 = UzbekStemmer.Derivational(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        # Prefixes
        tempWord, tempWay2 = UzbekStemmer.Prefixes(tempWord)
        tempWay1 = UzbekStemmer.JoinDict(tempWay1, tempWay2)

        words.append(tempWord)
        ways.append(dict(tempWay1))

        #print(words)
        #print(ways)
        return min(words),ways[words.index(min(words))]