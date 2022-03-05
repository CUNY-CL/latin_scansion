"""Unit tests for scansion.py."""

import functools
import logging
import unittest

import pynini

import latin_scansion


class ScansionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with pynini.Far("grammars/all.far", "r") as far:
            cls.scan_verse = functools.partial(
                latin_scansion.scan_verse,
                far["NORMALIZE"],
                far["PRONOUNCE"],
                far["VARIABLE"],
                far["SYLLABLE"],
                far["WEIGHT"],
                far["HEXAMETER"],
            )

    # Tests all features of the first verse's markup.
    def test_aen_1_1(self):
        text = "Arma virumque canō, Trojae quī prīmus ab ōris"
        verse = self.scan_verse(text, 1)
        self.assertEqual(verse.number, 1)
        self.assertEqual(verse.text, text)
        self.assertEqual(
            verse.norm, "arma virumque canō trojae quī prīmus ab ōris"
        )
        self.assertEqual(
            verse.raw_pron, "arma wirũːkwe kanoː trojjaj kwiː priːmus ab oːris"
        )
        self.assertEqual(
            verse.var_pron, "arma wirũːkwe kanoː trojjaj kwiː priːmus‿ab‿oːris"
        )

        # Tests foot structures.
        self.assertEqual(verse.foot[0].type, latin_scansion.Foot.DACTYL)
        self.assertEqual(verse.foot[1].type, latin_scansion.Foot.DACTYL)
        self.assertEqual(verse.foot[2].type, latin_scansion.Foot.SPONDEE)
        self.assertEqual(verse.foot[3].type, latin_scansion.Foot.SPONDEE)
        self.assertEqual(verse.foot[4].type, latin_scansion.Foot.DACTYL)
        self.assertEqual(verse.foot[5].type, latin_scansion.Foot.SPONDEE)

        # Tests syllable weights.
        self.assertEqual(
            verse.foot[0].syllable[0].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[0].syllable[1].weight, latin_scansion.Syllable.LIGHT
        )
        self.assertEqual(
            verse.foot[0].syllable[2].weight, latin_scansion.Syllable.LIGHT
        )
        self.assertEqual(
            verse.foot[1].syllable[0].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[1].syllable[1].weight, latin_scansion.Syllable.LIGHT
        )
        self.assertEqual(
            verse.foot[1].syllable[2].weight, latin_scansion.Syllable.LIGHT
        )
        self.assertEqual(
            verse.foot[2].syllable[0].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[2].syllable[1].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[3].syllable[0].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[3].syllable[1].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[4].syllable[0].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[4].syllable[1].weight, latin_scansion.Syllable.LIGHT
        )
        self.assertEqual(
            verse.foot[4].syllable[2].weight, latin_scansion.Syllable.LIGHT
        )
        self.assertEqual(
            verse.foot[2].syllable[0].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[5].syllable[1].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[5].syllable[0].weight, latin_scansion.Syllable.HEAVY
        )
        self.assertEqual(
            verse.foot[5].syllable[1].weight, latin_scansion.Syllable.HEAVY
        )

        # Tests subsyllabic units.
        self.assertEqual(verse.foot[0].syllable[0].nucleus, "a")
        self.assertEqual(verse.foot[0].syllable[0].coda, "r")
        self.assertEqual(verse.foot[0].syllable[1].onset, "m")
        self.assertEqual(verse.foot[0].syllable[1].nucleus, "a")
        self.assertEqual(verse.foot[0].syllable[2].onset, "w")
        self.assertEqual(verse.foot[0].syllable[2].nucleus, "i")
        self.assertEqual(verse.foot[1].syllable[0].onset, "r")
        self.assertEqual(verse.foot[1].syllable[0].nucleus, "ũː")
        self.assertEqual(verse.foot[1].syllable[1].onset, "kw")
        self.assertEqual(verse.foot[1].syllable[1].nucleus, "e")
        self.assertEqual(verse.foot[1].syllable[2].onset, "k")
        self.assertEqual(verse.foot[1].syllable[2].nucleus, "a")
        self.assertEqual(verse.foot[2].syllable[0].onset, "n")
        self.assertEqual(verse.foot[2].syllable[0].nucleus, "oː")
        self.assertEqual(verse.foot[2].syllable[1].onset, "tr")
        self.assertEqual(verse.foot[2].syllable[1].nucleus, "o")
        self.assertEqual(verse.foot[2].syllable[1].coda, "j")
        self.assertEqual(verse.foot[3].syllable[0].onset, "j")
        self.assertEqual(verse.foot[3].syllable[0].nucleus, "a")
        self.assertEqual(verse.foot[3].syllable[0].coda, "j")
        self.assertEqual(verse.foot[3].syllable[1].onset, "kw")
        self.assertEqual(verse.foot[3].syllable[1].nucleus, "iː")
        self.assertEqual(verse.foot[4].syllable[0].onset, "pr")
        self.assertEqual(verse.foot[4].syllable[0].nucleus, "iː")
        self.assertEqual(verse.foot[4].syllable[1].onset, "m")
        self.assertEqual(verse.foot[4].syllable[1].nucleus, "u")
        self.assertEqual(verse.foot[4].syllable[2].onset, "s")
        self.assertEqual(verse.foot[4].syllable[2].nucleus, "a")
        self.assertEqual(verse.foot[5].syllable[0].onset, "b")
        self.assertEqual(verse.foot[5].syllable[0].nucleus, "oː")
        self.assertEqual(verse.foot[5].syllable[1].onset, "r")
        self.assertEqual(verse.foot[5].syllable[1].nucleus, "i")
        self.assertEqual(verse.foot[5].syllable[1].coda, "s")

    # Scans verse 1.534, which is clearly defective (and in this case, it's
    # entirely possible Virgil never finished it).
    def test_aen_1_534(self):
        text = "Hic cursus fuit,"
        verse = self.scan_verse(text)
        self.assertEqual(verse.norm, "hic cursus fuit")
        self.assertTrue(verse.defective)

    # Tests that the grammar does not unnecessarily apply resyllabification.
    def test_aen_1_26(self):
        text = "exciderant animō; manet altā mente repostum"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "ekskiderant animoː manet‿altaː mente repostũː"
        )

    # Tests that the grammar does not unnecessarily apply elision.
    def test_aen_1_42(self):
        text = "Ipsa Jovis rapidum jaculāta ē nūbibus ignem"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "ipsa jowis rapidũː jakulaːta̶ ̶eː nuːbibus‿iŋnẽː"
        )

    def test_aen_1_247(self):
        text = "Hīc tamen ille urbem Patavī sēdēsque locāvit"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "hiːk tamen‿ille̶ ̶urbẽː patawiː seːdeːskwe lokaːwit",
        )

    def test_aen_1_254(self):
        text = "Ollī subrīdēns hominum sator atque deōrum"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "olliː subriːdeːns hominũː sator‿atkwe deoːrũː"
        )

    def test_aen_1_450(self):
        text = "Hōc prīmum in lūcō nova rēs oblāta timōrem"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "hoːk priːmũ̶ː̶ ̶in luːkoː nowa reːs oblaːta timoːrẽː",
        )

    def test_aen_1_477(self):
        text = "lōra tenēns tamen; huic cervīxque comaeque trahuntur"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "loːra teneːns tamen‿h̶ujk kerwiːkskwe komajkwe trahuntur",
        )

    def test_aen_1_593(self):
        text = "argentum Pariusve lapis circumdatur aurō."
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "argentũː pariuswe lapis kirkumdatur‿awroː"
        )

    def test_aen_1_649(self):
        text = "et circumtextum croceō vēlāmen acanthō,"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "et kirkumtekstũː krokeoː weːlaːmen‿akantoː"
        )

    def test_aen_1_682(self):
        text = "nē quā scīre dolōs mediusve occurrere possit."
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "neː kwaː skiːre doloːs mediuswe̶ ̶okkurrere possit",
        )

    def test_aen_1_697(self):
        text = "pallamque et pictum croceō vēlāmen acanthō."
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "pallãːkwe̶ ̶et piktũː krokeoː weːlaːmen‿akantoː"
        )

    # Tests handling of brackets.
    def test_aen_2_77(self):
        text = "[Ille haec dēpositā tandem formīdine fātur:]"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.norm, "ille haec dēpositā tandem formīdine fātur"
        )
        self.assertFalse(verse.defective)

    # No poetic license rules required.
    def test_aen_2_202(self):
        text = "Lāocoön, ductus Neptūnō sorte sacerdōs,"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "laːokoon duktus neptuːnoː sorte sakerdoːs"
        )

    # Elision.
    def test_aen_2_219(self):
        text = "bis medium amplexī, bis collō squāmea circum"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "bis mediũ̶ː̶ ̶ampleksiː bis kolloː skwaːmea kirkũː",
        )

    # Elision.
    def test_aen_2_278(self):
        text = "squālentem barbam et concrētōs sanguine crīnīs"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "skwaːlentẽː barbã̶ː̶ ̶et koŋkreːtoːs saŋgwine kriːniːs",
        )

    # Defective verse – first syllable is short.
    def test_aen_2_506(self):
        text = "procubuēre tenent danaī quā dēficit ignis"
        verse = self.scan_verse(text)
        self.assertTrue(verse.defective)

    @unittest.skip("Requires diastole.")
    def test_aen_2_675(self):
        text = "haerebat parvumque patrī tendēbat iūlum"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "hajrebat parwumkwe patriː tendeːba tiuːlũː"
        )

    @unittest.skip("Requires diastole.")
    def test_aen_2_744(self):
        text = "vēnimus hīc demum collēctīs omnibus ūna"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "weːnimu siːk demũː kolleːktiːs omnibu suːna"
        )

    def test_aen_2_764(self):
        text = "praedam adservābant hūc undique trōja gaza"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "prajdã̶ː̶ ̶adserwaːbant huːk undikwe troːïa gazza"
        )

    def test_aen_3_158(self):
        text = "īdem ventūrōs tollēmus in astra nepōtēs"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "iːdẽː wentuːroːs tolleːmus‿in‿astra nepoːteːs"
        )

    # Synizesis.
    def test_aen_3_161(self):
        text = "Mūtandae sēdēs. Nōn haec tibi lītora suāsit"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "muːtandaj seːdeːs noːn hajk tibi liːtora su͡aːsit"
        )

    def test_aen_3_365(self):
        text = "sōla novum dictūque nefās Harpyja Celaenō"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "soːla nowũː diktuːkwe nefaːs harpujja kelajnoː"
        )

    def test_aen_3_464(self):
        text = "dōna dehinc aurō gravia ac sectō elephantō"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "doːna dehiŋk awroː grawia̶ ̶ak sektoː elepantoː"
        )

    @unittest.skip("Requires diastole.")
    def test_aen_3_517(self):
        text = "armātumque aurō circumspicit Ōriōna"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "armaːtũːkwe awroː kirkumspiki toːriːoːna"
        )

    def test_aen_3_567(self):
        text = "ter spūmam ēlīsam et rōrantia vīdimus astra."
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "ter spuːmã̶ː̶ ̶eːliːsã̶ː̶ ̶et roːrantia wiːdimus‿astra",
        )

    @unittest.skip("Requires diastole.")
    def test_aen_4_146(self):
        text = "Crētesque Dryopesque fremunt pictīque Agathyrsī:"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "kreːteskweː druopeskwe fremunt piktiːkwe agatursiː",
        )

    def test_aen_4_302(self):
        text = "Thyjas, ubi audītō stimulant trietērica Bacchō"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "tujjas‿ubi̶ ̶awdiːtoː stimulant trieteːrika bakkoː",
        )

    def test_aen_4_324(self):
        text = "(hoc sōlum nōmen quoniam dē conjuge restat)?"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "hok soːlũː noːmen kwoniãː deː konjuge restat"
        )

    def test_aen_4_369(self):
        text = "Num flētū ingemuit nostrō? Num lūmina flexit?"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "nũː fleːtu̶ː̶ ̶iŋgemuit nostroː nũː luːmina fleksit",
        )

    def test_aen_4_569(self):
        text = "Heja age, rumpe morās. Varium et mūtābile semper"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "hejja̶ ̶age rumpe moraːs wariũ̶ː̶ ̶et muːtaːbile semper",
        )

    @unittest.skip("Requires diastole.")
    def test_aen_4_617(self):
        text = "auxilium implōret videatque indigna suorum"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "awksiliimploːret wideatkwindiŋna suoːrũː"
        )

    @unittest.skip(
        "bijugoː defies conventional var_pronounciation rules in that the "
        "intervocalic j is not geminate; perhaps j-gemination is not "
        "triggered in derived environments."
    )
    def test_aen_5_144(self):
        text = "Nōn tam praecipitēs bijugō certāmine campum"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "noːn tãː prajkipiteːs bijugoː kertaːmine kampũː"
        )

    @unittest.skip("Requires diastole.")
    def test_aen_5_306(self):
        text = "Gnōsia bina dabō lēvātō lūcida ferrō"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "ŋnoːsia biːna daboː leːwaːtoː luːkida ferroː"
        )

    def test_aen_5_352(self):
        text = "dat Saliō villīs onerōsum atque unguibus aureīs."
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron,
            "dat salioː williːs oneroːsũ̶ː̶ ̶atkwe̶ ̶uŋgwibus‿awre͡iːs",
        )

    @unittest.skip("Requires diastole.")
    def test_aen_5_520(self):
        text = "qui tamen āeriās tēlum contorsit in aurās"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "kwiː tame naːeriaːs teːlũː kontorsi ti nawraːs"
        )

    @unittest.skip("Requires diastole.")
    def test_aen_5_687(self):
        text = '"Juppiter omnipotēns, si nōndum exōsus ad ūnum'
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "juppite romnipoteːns siː noːndeksoːsu sa duːnũː"
        )

    def test_aen_5_870(self):
        text = '"Ō nimium caelō et pelagō cōnfīse serēnō'
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "oː nimiũː kajlo̶ː̶ ̶et pelagoː koːnfiːse sereːnoː"
        )

    @unittest.skip("Requires synizesis, but Cj is not a valid onset.")
    def test_aen_6_412(self):
        text = "dēturbat, laxatque forōs; simul accipit alveō"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "deːturbat laksatkwe foroːs simu lakkipi talwjoː"
        )

    @unittest.skip("Requires synizesis and diastole.")
    def test_aen_6_447(self):
        text = "Euadnēnque et Pāsiphaēn; hīs Lāodamīa"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "eːwadneːŋkwet paːsipaeːn hiːs laːodamiːa"
        )

    @unittest.skip("Requires systole.")
    def test_aen_6_507(self):
        text = "Nōmen et arma locum servant; tē, amīce, nequīvī"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "noːme ne tarma lokũː serwant te amiːke nekwiːwiː"
        )

    @unittest.skip("Requires diastole.")
    def test_aen_6_637(self):
        text = "Hīs demum exāctīs, perfectō mūnere dīvae,"
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "hiːs deːmeksaːktiːs perfektoː muːnere diːwaj"
        )

    @unittest.skip("Requires diastole.")
    def test_aen_6_695(self):
        text = 'Ille autem: "Tua me, genitor, tua trīstis imāgō'
        verse = self.scan_verse(text)
        self.assertEqual(
            verse.var_pron, "illawtẽː tua meː genitor tua triːsti simaːgoː"
        )


if __name__ == "__main__":
    logging.disable("CRITICAL")
    unittest.main()
