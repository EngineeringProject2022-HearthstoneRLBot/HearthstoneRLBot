class Hero:
    Druid = 2
    Hunter = 3
    Mage = 4
    Paladin = 5
    Priest = 6
    Rogue = 7
    Shaman = 8
    Warlock = 9
    Warrior = 10

    AllHeros = [Druid, Hunter, Mage, Paladin, Priest, Rogue, Shaman, Warlock, Warrior]


class PlayerDecks:
    decks = {'BasicDruid': ['EX1_169', 'EX1_169', 'CS2_005', 'CS2_005', 'CS2_189', 'CS2_189', 'CS2_120', 'CS2_120',
                            'CS2_009',
                            'CS2_009', 'CS2_013', 'CS2_013', 'CS2_007', 'CS2_007', 'CS2_127', 'CS2_127', 'CS2_182',
                            'CS2_182',
                            'CS2_119', 'CS2_119', 'DS1_055', 'DS1_055', 'EX1_593', 'EX1_593', 'CS2_200', 'CS2_200',
                            'CS2_162',
                            'CS2_162', 'CS2_201', 'CS2_201'],
             'BasicHunter': ['DS1_185', 'DS1_185', 'CS2_171', 'CS2_171', 'DS1_175', 'DS1_175', 'DS1_184', 'DS1_184',
                             'CS2_172',
                             'CS2_172', 'CS2_120', 'CS2_120', 'CS2_141', 'CS2_141', 'CS2_122', 'CS2_122', 'CS2_196',
                             'CS2_196',
                             'CS2_127', 'CS2_127', 'DS1_070', 'DS1_070', 'DS1_183', 'DS1_183', 'CS2_119', 'CS2_119',
                             'CS2_150',
                             'CS2_150', 'CS2_201', 'CS2_201'],
             'BasicMage': ['CFM_623', 'CFM_623', 'CS2_168', 'CS2_168', 'CS2_025', 'CS2_025', 'CS2_172', 'CS2_172',
                           'EX1_050',
                           'EX1_050', 'CS2_120', 'CS2_120', 'CS2_023', 'CS2_023', 'CS2_122', 'CS2_122', 'CS2_124',
                           'CS2_124',
                           'CS2_029', 'CS2_029', 'CS2_119', 'CS2_119', 'CS2_022', 'CS2_022', 'CS2_179', 'CS2_179',
                           'EX1_593',
                           'EX1_593', 'CS2_200', 'CS2_200'],
             'BasicPaladin': ['CS2_087', 'CS2_087', 'CS1_042', 'CS1_042', 'EX1_371', 'EX1_371', 'CS2_091', 'CS2_091',
                              'CS2_171', 'CS2_171', 'CS2_089', 'CS2_089', 'CS2_141', 'CS2_141', 'CS2_122', 'CS2_122',
                              'CS2_147', 'CS2_147',
                              'CS2_094', 'CS2_094', 'CS2_131', 'CS2_131', 'EX1_593', 'EX1_593', 'CS2_150', 'CS2_150',
                              'CS2_162',
                              'CS2_162', 'CS2_222', 'CS2_222'],
             'BasicPriest': ['CS2_189', 'CS2_189', 'CS1_130', 'CS1_130', 'CS2_235', 'CS2_235', 'CS2_004', 'CS2_004',
                             'EX1_011',
                             'EX1_011', 'EX1_192', 'EX1_192', 'CS2_172', 'CS2_172', 'CS2_121', 'CS2_121', 'CS2_234',
                             'CS2_234',
                             'EX1_019', 'EX1_019', 'CS2_127', 'CS2_127', 'CS2_182', 'CS2_182', 'CS2_179', 'CS2_179',
                             'EX1_399',
                             'EX1_399', 'CS2_201', 'CS2_201'],
             'BasicRogue': ['CS2_072', 'CS2_072', 'CS2_074', 'CS2_074', 'CS2_189', 'CS2_189', 'CS1_042', 'CS1_042',
                            'CS2_075',
                            'CS2_075', 'CS2_172', 'CS2_172', 'EX1_050', 'EX1_050', 'EX1_581', 'EX1_581', 'CS2_141',
                            'CS2_141',
                            'EX1_025', 'EX1_025', 'CS2_147', 'CS2_147', 'CS2_131', 'CS2_131', 'CS2_076', 'CS2_076',
                            'EX1_593',
                            'EX1_593', 'CS2_150', 'CS2_150'],
             'BasicShaman': ['CS2_041', 'CS2_041', 'CS2_037', 'CS2_037', 'CS2_171', 'CS2_171', 'CS2_121', 'CS2_121',
                             'CS2_045',
                             'CS2_045', 'CS2_039', 'CS2_039', 'CS2_122', 'CS2_122', 'CS2_124', 'CS2_124', 'CS2_182',
                             'CS2_182',
                             'EX1_246', 'EX1_246', 'CS2_179', 'CS2_179', 'CS2_187', 'CS2_187', 'CS2_226', 'CS2_226',
                             'CS2_200',
                             'CS2_200', 'CS2_213', 'CS2_213'],
             'BasicWarlock': ['CS2_168', 'CS2_168', 'CS2_065', 'CS2_065', 'EX1_011', 'EX1_011', 'CS2_142', 'CS2_142',
                              'CS2_120', 'CS2_120', 'EX1_306', 'EX1_306', 'CS2_061', 'CS2_061', 'CS2_057', 'CS2_057',
                              'CS2_124', 'CS2_124',
                              'CS2_182', 'CS2_182', 'CS2_062', 'CS2_062', 'CS2_197', 'CS2_197', 'DS1_055', 'DS1_055',
                              'CS2_213',
                              'CS2_213', 'CS2_186', 'CS2_186'],
             'BasicWarrior': ['CS2_168', 'CS2_168', 'CS2_108', 'CS2_108', 'CS2_121', 'CS2_121', 'CS2_105', 'CS2_105',
                              'EX1_506', 'EX1_506', 'CS2_106', 'CS2_106', 'CS2_196', 'CS2_196', 'CS2_103', 'CS2_103',
                              'EX1_084', 'EX1_084',
                              'CS2_124', 'CS2_124', 'EX1_025', 'EX1_025', 'CS2_179', 'CS2_179', 'EX1_399', 'EX1_399',
                              'CS2_200',
                              'CS2_200', 'CS2_162', 'CS2_162'],
             'MidrangeDruid': ['EX1_169', 'EX1_169', 'AT_037', 'AT_037', 'AT_038', 'EX1_154', 'EX1_154', 'CS2_011',
                               'CS2_011',
                               'CS2_013', 'CS2_013', 'EX1_166', 'EX1_166', 'AT_039', 'AT_039', 'EX1_165', 'EX1_165',
                               'EX1_571',
                               'EX1_571', 'NEW1_008', 'NEW1_008', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284', 'FP1_030',
                               'BRM_028', 'GVG_110', 'CS2_012', 'CS2_012'],
             'AgroHunter': ['LOOT_222', 'LOOT_222', 'LOOT_258', 'LOOT_258', 'UNG_912', 'UNG_912', 'EX1_066', 'UNG_915',
                            'UNG_915', 'LOOT_413', 'LOOT_413', 'NEW1_031', 'NEW1_031', 'ICC_419', 'ICC_419', 'EX1_539',
                            'EX1_539',
                            'EX1_538', 'GIL_828', 'GIL_828', 'LOOT_077', 'DS1_070', 'DS1_070', 'GIL_650', 'EX1_048',
                            'EX1_048', 'DS1_178',
                            'EX1_531', 'EX1_534', 'EX1_534'],
             'MechMage': ['NEW1_012', 'CS2_024', 'CS2_024', 'GVG_002', 'GVG_002', 'GVG_003', 'CS2_029', 'CS2_029',
                          'GVG_004',
                          'GVG_004', 'CS2_033', 'CS2_033', 'EX1_559', 'GVG_082', 'GVG_082', 'GVG_013', 'GVG_013',
                          'GVG_085',
                          'GVG_085', 'GVG_006', 'GVG_006', 'GVG_044', 'GVG_044', 'GVG_102', 'GVG_078', 'FP1_030',
                          'GVG_115',
                          'GVG_110', 'GVG_096', 'GVG_096'],
             'ControlPaladin': ['EX1_360', 'EX1_619', 'EX1_619', 'CS2_089', 'EX1_382', 'EX1_382', 'CS2_093', 'CS2_093',
                                'LOE_017', 'LOE_017', 'CS2_097', 'CS2_097', 'AT_104', 'EX1_354', 'EX1_383', 'NEW1_020',
                                'NEW1_020',
                                'EX1_007', 'EX1_007', 'EX1_085', 'EX1_005', 'CS2_179', 'CS2_179', 'EX1_048', 'EX1_564',
                                'NEW1_041',
                                'EX1_032', 'EX1_016', 'EX1_298', 'EX1_572'],
             'ControlPriest': ['EX1_621', 'EX1_621', 'GVG_012', 'GVG_012', 'CS2_235', 'CS2_235', 'CS2_004', 'CS2_004',
                               'FP1_001', 'FP1_001', 'EX1_622', 'EX1_622', 'EX1_339', 'EX1_339', 'NEW1_020', 'NEW1_020',
                               'FP1_009',
                               'CS2_181', 'CS2_181', 'EX1_591', 'EX1_591', 'CS1_112', 'FP1_012', 'FP1_012', 'CS2_186',
                               'EX1_091', 'AT_132',
                               'GVG_008', 'GVG_008', 'EX1_572'],
             'OilRogue': ['CS2_072', 'CS2_072', 'EX1_145', 'EX1_145', 'CS2_074', 'CS2_074', 'CS2_233', 'CS2_233',
                          'EX1_124',
                          'EX1_124', 'EX1_581', 'EX1_581', 'EX1_613', 'EX1_129', 'EX1_129', 'EX1_134', 'EX1_134',
                          'GVG_022',
                          'GVG_022', 'CS2_077', 'CS2_077', 'EX1_012', 'CS2_117', 'CS2_117', 'GVG_096', 'NEW1_026',
                          'NEW1_026',
                          'EX1_284', 'EX1_284', 'FP1_030'],
             'MidrangeShaman': ['EX1_245', 'GVG_038', 'GVG_038', 'EX1_565', 'EX1_565', 'CS2_045', 'CS2_045', 'EX1_248',
                                'EX1_248',
                                'EX1_259', 'EX1_259', 'EX1_575', 'EX1_246', 'EX1_246', 'EX1_567', 'CS2_042', 'CS2_042',
                                'NEW1_010',
                                'EX1_012', 'FP1_002', 'FP1_002', 'EX1_093', 'EX1_093', 'GVG_096', 'GVG_096', 'GVG_069',
                                'EX1_284',
                                'EX1_284', 'FP1_030', 'GVG_110'],
             'DemonZoo': ['EX1_319', 'EX1_319', 'EX1_316', 'EX1_316', 'CS2_065', 'CS2_065', 'LOE_023', 'LOE_023',
                          'BRM_006',
                          'BRM_006', 'EX1_304', 'GVG_045', 'GVG_045', 'FP1_022', 'FP1_022', 'EX1_310', 'EX1_310',
                          'GVG_021',
                          'CS2_188', 'CS2_188', 'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'FP1_007', 'FP1_007',
                          'CS2_203',
                          'EX1_093', 'EX1_093', 'GVG_110'],
             'MidrangeWarrior': ['CS2_108', 'CS2_108', 'EX1_410', 'EX1_410', 'EX1_402', 'EX1_402', 'EX1_603', 'EX1_603',
                                 'BRM_015',
                                 'CS2_106', 'CS2_106', 'EX1_606', 'EX1_606', 'FP1_021', 'FP1_021', 'EX1_407', 'GVG_053',
                                 'GVG_053',
                                 'EX1_414', 'EX1_007', 'EX1_007', 'EX1_005', 'EX1_558', 'FP1_012', 'FP1_012', 'EX1_016',
                                 'EX1_249',
                                 'GVG_110', 'EX1_561', 'EX1_572'],
             'FastDruid': ['EX1_169', 'EX1_169', 'EX1_154', 'EX1_154', 'CS2_011', 'CS2_011', 'CS2_013', 'CS2_013',
                           'EX1_166',
                           'EX1_166', 'CS2_012', 'CS2_012', 'EX1_165', 'EX1_165', 'EX1_571', 'NEW1_008', 'NEW1_008',
                           'EX1_573',
                           'FP1_001', 'EX1_085', 'FP1_005', 'FP1_005', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284',
                           'EX1_558',
                           'FP1_012', 'EX1_016', 'GVG_110'],
             'FaceHunter': ['GVG_043', 'GVG_043', 'BRM_013', 'BRM_013', 'NEW1_031', 'NEW1_031', 'EX1_536', 'EX1_536',
                            'EX1_539',
                            'EX1_539', 'EX1_538', 'EX1_538', 'CS2_188', 'CS2_188', 'EX1_008', 'EX1_008', 'EX1_029',
                            'EX1_029',
                            'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'AT_084', 'AT_084', 'EX1_089', 'EX1_089',
                            'AT_087',
                            'AT_087', 'CS2_203', 'CS2_203'],
             'FlamewalkerTempoMage': ['EX1_277', 'EX1_277', 'NEW1_012', 'NEW1_012', 'GVG_001', 'GVG_001', 'CS2_024',
                                      'CS2_024',
                                      'GVG_003', 'GVG_003', 'BRM_002', 'BRM_002', 'CS2_029', 'CS2_029', 'EX1_608',
                                      'EX1_608',
                                      'CS2_032', 'CS2_032', 'EX1_066', 'EX1_066', 'GVG_096', 'GVG_096', 'EX1_284',
                                      'EX1_284',
                                      'FP1_012', 'FP1_012', 'FP1_030', 'EX1_016', 'GVG_110', 'EX1_298'],
             'MurlocPaladin': ['GVG_058', 'GVG_058', 'EX1_382', 'EX1_382', 'GVG_059', 'GVG_061', 'GVG_061', 'CS2_093',
                               'CS2_093',
                               'LOE_017', 'CS2_097', 'BRM_001', 'EX1_354', 'LOE_026', 'FP1_001', 'CS2_173', 'CS2_173',
                               'NEW1_019',
                               'EX1_096', 'EX1_096', 'EX1_507', 'EX1_507', 'EX1_595', 'EX1_062', 'GVG_096', 'GVG_096',
                               'GVG_069',
                               'GVG_069', 'FP1_012', 'GVG_110'],
             'DragonPriest': ['CS2_235', 'CS2_235', 'CS2_004', 'CS2_004', 'BRM_004', 'BRM_004', 'EX1_622', 'EX1_622',
                              'CS2_234',
                              'AT_116', 'AT_116', 'FP1_023', 'GVG_010', 'GVG_010', 'CS1_112', 'CS1_112', 'CS2_186',
                              'NEW1_020',
                              'BRM_033', 'BRM_033', 'BRM_020', 'AT_017', 'AT_017', 'EX1_284', 'EX1_284', 'BRM_034',
                              'BRM_034',
                              'AT_123', 'BRM_031', 'EX1_572']}

    BasicDruid = decks['BasicDruid']
    BasicHunter = decks['BasicHunter']
    BasicMage = decks['BasicMage']
    BasicPaladin = decks['BasicPaladin']
    BasicPriest = decks['BasicPriest']
    BasicRogue = decks['BasicRogue']
    BasicShaman = decks['BasicShaman']
    BasicWarlock = decks['BasicWarlock']
    BasicWarrior = decks['BasicWarrior']
    MidrangeDruid = decks['MidrangeDruid']
    AgroHunter = decks['AgroHunter']
    MechMage = decks['MechMage']
    ControlPaladin = decks['ControlPaladin']
    ControlPriest = decks['ControlPriest']
    OilRogue = decks['OilRogue']
    MidrangeShaman = decks['MidrangeShaman']
    DemonZoo = decks['DemonZoo']
    MidrangeWarrior = decks['MidrangeWarrior']
    FastDruid = decks['FastDruid']
    FaceHunter = decks['FaceHunter']
    FlamewalkerTempoMage = decks['FlamewalkerTempoMage']
    MurlocPaladin = decks['MurlocPaladin']
    DragonPriest = decks['DragonPriest']


class HeroDecks:
    BasicDruid = "BasicDruid", Hero.Druid, PlayerDecks.BasicDruid
    BasicHunter = "BasicHunter", Hero.Hunter, PlayerDecks.BasicHunter
    BasicMage = "BasicMage", Hero.Mage, PlayerDecks.BasicMage
    BasicPaladin = "BasicPaladin", Hero.Paladin, PlayerDecks.BasicPaladin
    BasicPriest = "BasicPriest", Hero.Priest, PlayerDecks.BasicPriest
    BasicRogue = "BasicRogue", Hero.Rogue, PlayerDecks.BasicRogue
    BasicShaman = "BasicShaman", Hero.Shaman, PlayerDecks.BasicShaman
    BasicWarlock = "BasicWarlock", Hero.Warlock, PlayerDecks.BasicWarlock
    BasicWarrior = "BasicWarrior", Hero.Warrior, PlayerDecks.BasicWarrior
    MidrangeDruid = "MidrangeDruid", Hero.Druid, PlayerDecks.MidrangeDruid
    AgroHunter = "AgroHunter", Hero.Hunter, PlayerDecks.AgroHunter
    MechMage = "MechMage", Hero.Mage, PlayerDecks.MechMage
    ControlPaladin = "ControlPaladin", Hero.Paladin, PlayerDecks.ControlPaladin
    ControlPriest = "ControlPriest", Hero.Priest, PlayerDecks.ControlPriest
    OilRogue = "OilRogue", Hero.Rogue, PlayerDecks.OilRogue
    MidrangeShaman = "MidrangeShaman", Hero.Shaman, PlayerDecks.MidrangeShaman
    DemonZoo = "DemonZoo", Hero.Warlock, PlayerDecks.DemonZoo
    MidrangeWarrior = "MidrangeWarrior", Hero.Warrior, PlayerDecks.MidrangeWarrior
    FastDruid = "FastDruid", Hero.Druid, PlayerDecks.FastDruid
    FaceHunter = "FaceHunter", Hero.Hunter, PlayerDecks.FaceHunter
    FlamewalkerTempoMage = "FlamewalkerTempoMage", Hero.Mage, PlayerDecks.FlamewalkerTempoMage
    MurlocPaladin = "MurlocPaladin", Hero.Paladin, PlayerDecks.MurlocPaladin
    DragonPriest = "DragonPriest", Hero.Priest, PlayerDecks.DragonPriest
    AllDecks = [BasicDruid, BasicHunter, BasicMage, BasicPaladin, BasicPriest, BasicRogue, BasicShaman, BasicWarlock,
                BasicWarrior, MidrangeDruid, AgroHunter, MechMage,
                ControlPaladin, ControlPriest, OilRogue, MidrangeShaman, DemonZoo, MidrangeWarrior, FastDruid,
                FaceHunter, FlamewalkerTempoMage, MurlocPaladin, DragonPriest]

    @staticmethod
    def HeroDeck(hero):
        heroDecks = []
        for deck in HeroDecks.AllDecks:
            if deck[1] == hero:
                heroDecks.append(deck)
        return heroDecks

    @staticmethod
    def HeroFromDeckName(deckname):
        for deck in HeroDecks.AllDecks:
            if deck[0] == deckname:
                return deck[1]
        return None


class PlayerType:
    Random = 1
    Modeled = 2
    Manual = 3
