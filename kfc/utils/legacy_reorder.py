#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Lnicode fonts to Khmer Legacy Conversion
# Copyright(c) 2006-2008 Khmer Software Initiative
#               www.khmeros.info
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# See the LICENSE file for more details.
#
# Developed by:
#       Hok Kakada (hokkakada@khmeros.info)
#       Keo Sophon (keosophon@khmeros.info)
#       San Titvirak (titvirak@khmeros.info)
#       Seth Chanratha (sethchanratha@khmeros.info)
#
# This module reorder unicode string accordding unicode order
import unittest


# important character to test in order to form a cluster
SRAAA = chr(0x17B6)
SRAE = chr(0x17C1)
SRAOE = chr(0x17BE)
SRAOO = chr(0x17C4)
SRAYA = chr(0x17BF)
SRAIE = chr(0x17C0)
SRAAU = chr(0x17C5)
SRAII = chr(0x17B8)
SRAU = chr(0x17BB)
TRIISAP = chr(0x17CA)
MUUSIKATOAN = chr(0x17C9)
SAMYOKSANNYA = chr(0x17D0)

LA = chr(0x17A1)
NYO = chr(0x1789)
BA = chr(0x1794)
YO = chr(0x1799)
SA = chr(0x179F)
COENG = chr(0x17D2)
CORO = chr(0x17D2) + chr(0x179A)
CONYO = chr(0x17D2) + chr(0x1789)
SRAOM = chr(0x17C6)

MARK = chr(0x17EA)
# TODO: think about another relacement for the dotted circle;
DOTCIRCLE = u''

# possible combination for sra E
sraEcombining = {
    SRAOE: SRAII,
    SRAYA: SRAYA,
    SRAIE: SRAIE,
    SRAOO: SRAAA,
    SRAAU: SRAAU
}

CC_RESERVED = 0
CC_CONSONANT = 1    # Consonant of type 1 or independent vowel
CC_CONSONANT2 = 2    # Consonant of type 2
CC_CONSONANT3 = 3    # Consonant of type 3
CC_ZERO_WIDTH_NJ_MARK = 4    # Zero Width non joiner character (0x200C)
CC_CONSONANT_SHIFTER = 5
CC_ROBAT = 6    # Khmer special diacritic accent -treated differently in state table
CC_COENG = 7    # Subscript consonant combining character
CC_DEPENDENT_VOWEL = 8
CC_SIGN_ABOVE = 9
CC_SIGN_AFTER = 10
CC_ZERO_WIDTH_J_MARK = 11    # Zero width joiner character
CC_COUNT = 12    # This is the number of character classes


CF_CLASS_MASK = 0x0000FFFF

CF_CONSONANT = 0x01000000   # flag to speed up comparing
CF_SPLIT_VOWEL = 0x02000000   # flag for a split vowel -> the first part is added in front of the syllable
CF_DOTTED_CIRCLE = 0x04000000   # add a dotted circle if a character with this flag is the first in a
# syllable
CF_COENG = 0x08000000   # flag to speed up comparing
CF_SHIFTER = 0x10000000   # flag to speed up comparing
CF_ABOVE_VOWEL = 0x20000000   # flag to speed up comparing

# position flags
CF_POS_BEFORE = 0x00080000
CF_POS_BELOW = 0x00040000
CF_POS_ABOVE = 0x00020000
CF_POS_AFTER = 0x00010000
CF_POS_MASK = 0x000f0000

# simple classes, they are used in the state table (in this file) to control the length of a syllable
# they are also used to know where a character should be placed (location in reference to the base character)
# and also to know if a character, when independently displayed, should be displayed with a dotted-circle to
# indicate error in syllable construction
_xx = CC_RESERVED
_sa = CC_SIGN_ABOVE | CF_DOTTED_CIRCLE | CF_POS_ABOVE
_sp = CC_SIGN_AFTER | CF_DOTTED_CIRCLE | CF_POS_AFTER
_c1 = CC_CONSONANT | CF_CONSONANT
_c2 = CC_CONSONANT2 | CF_CONSONANT
_c3 = CC_CONSONANT3 | CF_CONSONANT
_rb = CC_ROBAT | CF_POS_ABOVE | CF_DOTTED_CIRCLE
_cs = CC_CONSONANT_SHIFTER | CF_DOTTED_CIRCLE | CF_SHIFTER
_dl = CC_DEPENDENT_VOWEL | CF_POS_BEFORE | CF_DOTTED_CIRCLE
_db = CC_DEPENDENT_VOWEL | CF_POS_BELOW | CF_DOTTED_CIRCLE
_da = CC_DEPENDENT_VOWEL | CF_POS_ABOVE | CF_DOTTED_CIRCLE | CF_ABOVE_VOWEL
_dr = CC_DEPENDENT_VOWEL | CF_POS_AFTER | CF_DOTTED_CIRCLE
_co = CC_COENG | CF_COENG | CF_DOTTED_CIRCLE

# split vowel
_va = _da | CF_SPLIT_VOWEL
_vr = _dr | CF_SPLIT_VOWEL


# Character class tables
# _xx character does not combine into syllable, such as numbers, puntuation marks, non-Khmer signs...
# _sa Sign placed above the base
# _sp Sign placed after the base
# _c1 Consonant of type 1 or independent vowel (independent vowels behave as type 1 consonants)
# _c2 Consonant of type 2 (only RO)
# _c3 Consonant of type 3
# _rb Khmer sign robat u17CC. combining mark for subscript consonants
# _cd Consonant-shifter
# _dl Dependent vowel placed before the base (left of the base)
# _db Dependent vowel placed below the base
# _da Dependent vowel placed above the base
# _dr Dependent vowel placed behind the base (right of the base)
# _co Khmer combining mark COENG u17D2, combines with the consonant or independent vowel following
#     it to create a subscript consonant or independent vowel
# _va Khmer split vowel in wich the first part is before the base and the second one above the base
# _vr Khmer split vowel in wich the first part is before the base and the second one behind (right of) the base

khmerCharClasses = [
    _c1, _c1, _c1, _c3, _c1, _c1, _c1, _c1, _c3, _c1, _c1, _c1, _c1, _c3, _c1, _c1,  # 1780 - 178F
    _c1, _c1, _c1, _c1, _c3, _c1, _c1, _c1, _c1, _c3, _c2, _c1, _c1, _c1, _c3, _c3,  # 1790 - 179F
    _c1, _c3, _c1, _c1, _c1, _c1, _c1, _c1, _c1, _c1, _c1, _c1, _c1, _c1, _c1, _c1,  # 17A0 - 17AF
    _c1, _c1, _c1, _c1, _dr, _dr, _dr, _da, _da, _da, _da, _db, _db, _db, _va, _vr,  # 17B0 - 17BF
    _vr, _dl, _dl, _dl, _vr, _vr, _sa, _sp, _sp, _cs, _cs, _sa, _rb, _sa, _sa, _sa,  # 17C0 - 17CF
    _sa, _sa, _co, _sa, _xx, _xx, _xx, _xx, _xx, _xx, _xx, _xx, _xx, _sa, _xx, _xx,  # 17D0 - 17DF
]


# khmerStateTable[][CC_COUNT] =
khmerStateTable = [
    # xx  c1  c2  c3 zwnj cs  rb  co  dv  sa  sp zwj
    [1,  2,  2,  2,  1,  1,  1,  6,  1,  1,  1,  2],  # 0 - ground state
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 1 - exit state (or sign to the right of the
    #      syllable)
    [-1, -1, -1, -1,  3,  4,  5,  6, 16, 17,  1, -1],  # 2 - Base consonant
    [-1, -1, -1, -1, -1,  4, -1, -1, 16, -1, -1, -1],  # 3 - First ZWNJ before a register shifter
    #      It can only be followed by a shifter or a vowel
    [-1, -1, -1, -1, 15, -1, -1,  6, 16, 17,  1, 14],  # 4 - First register shifter
    [-1, -1, -1, -1, -1, -1, -1, -1, 20, -1,  1, -1],  # 5 - Robat
    [-1,  7,  8,  9, -1, -1, -1, -1, -1, -1, -1, -1],  # 6 - First Coeng
    [-1, -1, -1, -1, 12, 13, -1, 10, 16, 17,  1, 14],  # 7 - First consonant of type 1 after coeng
    [-1, -1, -1, -1, 12, 13, -1, -1, 16, 17,  1, 14],  # 8 - First consonant of type 2 after coeng
    [-1, -1, -1, -1, 12, 13, -1, 10, 16, 17,  1, 14],  # 9 - First consonant or type 3 after ceong
    [-1, 11, 11, 11, -1, -1, -1, -1, -1, -1, -1, -1],  # 10 - Second Coeng (no register shifter before)
    [-1, -1, -1, -1, 15, -1, -1, -1, 16, 17,  1, 14],  # 11 - Second coeng consonant (or ind. vowel) no
    #      register shifter before
    [-1, -1, -1, -1, -1, 13, -1, -1, 16, -1, -1, -1],  # 12 - Second ZWNJ before a register shifter
    [-1, -1, -1, -1, 15, -1, -1, -1, 16, 17,  1, 14],  # 13 - Second register shifter
    [-1, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1],  # 14 - ZWJ before vowel
    [-1, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1],  # 15 - ZWNJ before vowel
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 17,  1, 18],  # 16 - dependent vowel
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  1, 18],  # 17 - sign above
    [-1, -1, -1, -1, -1, -1, -1, 19, -1, -1, -1, -1],  # 18 - ZWJ after vowel
    [-1,  1, -1,  1, -1, -1, -1, -1, -1, -1, -1, -1],  # 19 - Third coeng
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  1, -1]  # 20 - dependent vowel after a Robat
]


def getCharClass(uniChar):
    """
    input one unicode character;
    output an integer which is the Khmer type of the character or 0
    """
    # if (type(uniChar) != unicode):
    #     raise TypeError('only accept unicode character')

    if (len(uniChar) != 1):
        raise TypeError('only accept one character, but ' + str(len(uniChar)) + ' chars found.')

    ch = ord(uniChar[0])
    if (ch >= 0x1780):
        ch -= 0x1780
        if (ch < len(khmerCharClasses)):
            return khmerCharClasses[ch]
    return 0


def reorder(sin):
    """
    Given an input string of unicode cluster to reorder.
    The return is the visual based cluster (legacy style) string.
    """
    # if (type(sin) != unicode):
    #     raise TypeError('only accept unicode string')

    cursor = 0
    state = 0
    charCount = len(sin)
    result = u''

    while (cursor < charCount):
        reserved = ''
        signAbove = ''
        signAfter = ''
        base = ''
        robat = ''
        shifter = ''
        vowelBefore = ''
        vowelBelow = ''
        vowelAbove = ''
        vowelAfter = ''
        coeng = False
        cluster = ''

        coeng1 = ''
        coeng2 = ''

        shifterAfterCoeng = False

        while (cursor < charCount):

            curChar = sin[cursor]
            kChar = getCharClass(curChar)
            charClass = kChar & CF_CLASS_MASK
            state = khmerStateTable[state][charClass]
            if (state < 0):
                break

            # collect variable for cluster here

            if (kChar == _xx):
                reserved = curChar
            elif (kChar == _sa):        # Sign placed above the base
                signAbove = curChar
            elif (kChar == _sp):        # Sign placed after the base
                signAfter = curChar
            elif (kChar == _c1) or (kChar == _c2) or (kChar == _c3):    # Consonant
                if (coeng):
                    if (not coeng1):
                        coeng1 = COENG + curChar
                    else:
                        coeng2 = COENG + curChar
                    coeng = False
                else:
                    base = curChar
            elif (kChar == _rb):            # Khmer sign robat u17CC
                robat = curChar
            elif (kChar == _cs):            # Consonant-shifter
                if (coeng1):
                    shifterAfterCoeng = True
                shifter = curChar
            elif (kChar == _dl):            # Dependent vowel placed before the base
                vowelBefore = curChar
            elif (kChar == _db):            # Dependent vowel placed below the base
                vowelBelow = curChar
            elif (kChar == _da):            # Dependent vowel placed above the base
                vowelAbove = curChar
            elif (kChar == _dr):            # Dependent vowel placed behind the base
                vowelAfter = curChar
            elif (kChar == _co):            # Khmer combining mark COENG
                coeng = True
            elif (kChar == _va):            # Khmer split vowel, see _da
                vowelBefore = SRAE
                vowelAbove = sraEcombining[curChar]
            elif (kChar == _vr):            # Khmer split vowel, see _dr
                vowelBefore = SRAE
                vowelAfter = sraEcombining[curChar]

            cursor += 1
        # end of while (a cluster has found)

        # logic of vowel
        # determine if right side vowel should be marked
        if (coeng1 and vowelBelow):
            vowelBelow = MARK + vowelBelow
        elif ((base == LA or base == NYO) and vowelBelow):
            vowelBelow = MARK + vowelBelow
        elif (coeng1 and vowelBefore and vowelAfter):
            vowelAfter = MARK + vowelAfter

        # logic when cluster has coeng
        # should coeng be located on left side
        coengBefore = ''
        if (coeng1 == CORO):
            coengBefore = coeng1
            coeng1 = ''
        elif (coeng2 == CORO):
            coengBefore = MARK + coeng2
            coeng2 = ''
        if (coeng1 or coeng2):
            # NYO must change to other form when there is coeng
            if (base == NYO):
                base = MARK + base
                # coeng NYO must be marked
                if (coeng1 == CONYO):
                    coeng1 = MARK + coeng1

            if (coeng1 and coeng2):
                coeng2 = MARK + coeng2

        # logic of shifter with base character
        if (base and shifter):
            # special case apply to BA only
            if (vowelAbove) and (base == BA) and (shifter == TRIISAP):
                vowelAbove = MARK + vowelAbove
            elif (vowelAbove):
                shifter = MARK + shifter
            elif (signAbove == SAMYOKSANNYA) and (shifter == MUUSIKATOAN):
                shifter = MARK + shifter
            elif (signAbove and vowelAfter):
                shifter = MARK + shifter
            elif (signAbove):
                signAbove = MARK + signAbove
            # add another mark to shifter
            if (coeng1) and (vowelAbove or signAbove):
                shifter = MARK + shifter
            if (base == LA or base == NYO):
                shifter = MARK + shifter

        # uncomplete coeng
        if (coeng and not coeng1):
            coeng1 = COENG
        elif (coeng and not coeng2):
            coeng2 = MARK + COENG

        # render DOTCIRCLE for standalone sign or vowel
        if (not base) and (vowelBefore or coengBefore or robat or shifter or coeng1 or coeng2 or vowelAfter or vowelBelow or vowelAbove or signAbove or signAfter):
            base = DOTCIRCLE

        # place of shifter
        shifter1 = ''
        shifter2 = ''
        if (shifterAfterCoeng):
            shifter2 = shifter
        else:
            shifter1 = shifter

        specialCaseBA = False
        if (base == BA) and ((vowelAfter == SRAAA) or (vowelAfter == SRAAU) or (vowelAfter == MARK + SRAAA) or (vowelAfter == MARK + SRAAU)):
            # SRAAA or SRAAU will get a MARK if there is coeng, redefine to last char
            vowelAfter = vowelAfter[-1]
            specialCaseBA = True
            if (coeng1) and (coeng1[-1] in [BA, YO, SA]):
                specialCaseBA = False

        # cluster formation
        if (specialCaseBA):
            cluster = vowelBefore + coengBefore + base + vowelAfter + robat + shifter1 + coeng1 + coeng2 + shifter2 + vowelBelow + vowelAbove + signAbove + signAfter
        else:
            cluster = vowelBefore + coengBefore + base + robat + shifter1 + coeng1 + coeng2 + shifter2 + vowelBelow + vowelAbove + vowelAfter + signAbove + signAfter

        result += cluster + reserved
        state = 0
    # end of while
    return result


class TestReordering(unittest.TestCase):

    def testKhmerType(self):
        # make sure the types are correct
        self.assertEqual(getCharClass(chr(0x177F)), 0)
        self.assertEqual(getCharClass(chr(0x1780)), _c1)
        self.assertEqual(getCharClass(chr(0x1790)), _c1)
        self.assertEqual(getCharClass(chr(0x17A0)), _c1)
        self.assertEqual(getCharClass(chr(0x17B0)), _c1)
        self.assertEqual(getCharClass(chr(0x17C0)), _vr)
        self.assertEqual(getCharClass(chr(0x17D0)), _sa)
        self.assertEqual(getCharClass(chr(0x17D4)), 0)
        self.assertEqual(getCharClass(chr(0x17ff)), 0)

    def testReordering(self):
        # low vowel under coeng go deeper
        self.assertEqual(reorder(u'ខ្នុ'), u'ខ្ន' + MARK + u'ុ')
        self.assertEqual(reorder(u'ត្រូ'), u'្រត' + MARK + u'ូ')
        self.assertEqual(reorder(u'ព្យួ'), u'ព្យ' + MARK + u'ួ')
        # vowel under LA or NYO go deeper
        self.assertEqual(reorder(u'ឡូ'), u'ឡ' + MARK + u'ូ')
        self.assertEqual(reorder(u'ញួ'), u'ញ' + MARK + u'ួ')
        # mark vowel after when there is coeng
        self.assertEqual(reorder(u'ក្បៀ'), u'េក្ប' + MARK + u'ៀ')

        # coeng RO must on left side
        self.assertEqual(reorder(u'ក្រ'), u'្រក')
        self.assertEqual(reorder(u'ស្ត្រ'), MARK + u'្រស្ត')
        # mark NYO when there is coeng
        self.assertEqual(reorder(u'ញ្ជ'), MARK + u'ញ្ជ')
        # coeng NYO under NYO is marked
        self.assertEqual(reorder(u'ញ្ញ'), MARK + u'ញ' + MARK + u'្ញ')
        # coeng NYO under other is normal
        self.assertEqual(reorder(u'ជ្ញ'), u'ជ្ញ')
        # coeng1 and coeng2, mark coeng2
        self.assertEqual(reorder(u'ក្ស្ម'), u'ក្ស' + MARK + u'្ម')

        # PA has no modification
        self.assertEqual(reorder(u'ប៉'), u'ប៉')
        # special case BA TRISSAP, mark vowel above
        self.assertEqual(reorder(u'ប៊ី'), u'ប៊' + MARK + u'ី')
        # base and shifter and vowel above, mark shifter
        self.assertEqual(reorder(u'ប៉ី'), u'ប' + MARK + u'៉ី')
        self.assertEqual(reorder(u'ស៊ី'), u'ស' + MARK + u'៊ី')
        # base and muusikatoan and samyok-sannya, mark shifter
        self.assertEqual(reorder(u'នំប៉័ង'), u'នំប' + MARK + u'៉' + u'័ង')
        # shifter and sign above and vowel after, mark shifter
        self.assertEqual(reorder(u'ស៊ាំ'), u'ស' + MARK + u'៊' + u'ាំ')
        # shifter and sign above, mark sign
        self.assertEqual(reorder(u'អ៊ំ'), u'អ៊' + MARK + u'ំ')
        # double mark shifter when there is ceong and sign or vowel above
        self.assertEqual(reorder(u'ប្ប៉័ង'), u'ប្ប' + MARK + MARK + u'៉' + u'័ង')

        # uncomplete coeng is still keep
        self.assertEqual(reorder(u'ក្'), u'ក្')
        self.assertEqual(reorder(u'ក្ក្'), u'ក្ក' + MARK + u'្')

        # render standalone vowel or sign with DOTCIRCLE
        self.assertEqual(reorder(u'ា'), DOTCIRCLE + u'ា')
        self.assertEqual(reorder(u'េ'), u'េ' + DOTCIRCLE)
        self.assertEqual(reorder(u'ើ'), u'េ' + DOTCIRCLE + u'ី')
        self.assertEqual(reorder(u'ំ'), DOTCIRCLE + u'ំ')
        self.assertEqual(reorder(u'ោះ'), u'េ' + DOTCIRCLE + u'ា' + DOTCIRCLE + u'ះ')

        # shifter is after ceong
        self.assertEqual(reorder(u'ន្ស៊ី'), u'ន្ស' + MARK + MARK + u'៊ី')

        # special case BA and sra A, get alway near to each other
        self.assertEqual(reorder(u'ប្រា'), u'្របា')
        self.assertEqual(reorder(u'ប្ដា'), u'បា្ដ')
        self.assertEqual(reorder(u'ប៉ា'), u'បា៉')
        self.assertEqual(reorder(u'ប្រៅ'), u'េ្របៅ')
        self.assertEqual(reorder(u'ប្ដៅ'), u'េបៅ្ដ')
        self.assertEqual(reorder(u'ប៉ៅ'), u'េបៅ៉')
        # except there is coeng between them
        self.assertEqual(reorder(u'ប្បា'), u'ប្បា')

        # other test of prevention
        # simple rendering
        self.assertEqual(reorder(u'គេ'), u'េគ')
        self.assertEqual(reorder(u'គោ'), u'េគា')
        self.assertEqual(reorder(u'កៅ'), u'េកៅ')
        self.assertEqual(reorder(u'លើ'), u'េលី')
        self.assertEqual(reorder(u'បៀ'), u'េបៀ')
        self.assertEqual(reorder(u'តឿ'), u'េតឿ')
        self.assertEqual(reorder(u'កាំ'), u'កាំ')
        # reorder of more than one cluster
        self.assertEqual(reorder(u'កាប់គោ'), u'កាប់េគា')
        self.assertEqual(reorder(u'ខាងលើ'), u'ខាងេលី')
        self.assertEqual(reorder(u'ចំពោះ'), u'ចំេពាះ')
        # mix with english text
        self.assertEqual(reorder(u'កកុះwelcomeកុម្ភៈ'), u'កកុះwelcomeកុម្ភៈ')
        # two shifter or 3 vowel or 4 sign
        self.assertEqual(reorder(u'៊៊'), DOTCIRCLE + u'៊' + DOTCIRCLE + u'៊')
        self.assertEqual(reorder(u'ាិី'), DOTCIRCLE + u'ា' + DOTCIRCLE + u'ិ' + DOTCIRCLE + u'ី')
        self.assertEqual(reorder(u'ំះ័'), DOTCIRCLE + u'ំ' + DOTCIRCLE + u'ះ' + DOTCIRCLE + u'័')
        # muusikatoan not convert when vowel is not high
        self.assertEqual(reorder(u'ម៉្ងៃ'), u'ៃម៉្ង')
        # two coengs with vowel that place on left and right (some bigger than normal)
        self.assertEqual(reorder(u'កញ្ច្រៀវ'), u'កេ' + MARK + u'្រ' + MARK + u'ញ្ច' + MARK + u'ៀវ')
        self.assertEqual(reorder(u'កញ្ច្រោង'), u'កេ' + MARK + u'្រ' + MARK + u'ញ្ច' + MARK + u'ាង')
        # vowel which under coeng go one step deeper
        self.assertEqual(reorder(u'ប្ដូ'), u'ប្ដ' + MARK + u'ូ')
        # don't break the sign
        self.assertEqual(reorder(u'ចុះ'), u'ចុះ')
        self.assertEqual(reorder(u'នុ៎ះ'), u'នុ៎ះ')
        # change sign OM, not shifter
        self.assertEqual(reorder(u'អ៊ុំ'), u'អ៊ុ' + MARK + u'ំ')
        # this is two cluster
        self.assertEqual(reorder(u'ាក'), DOTCIRCLE + u'ាក')


if __name__ == '__main__':
    unittest.main()
