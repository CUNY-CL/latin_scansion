"""Unit tests for scansion.py."""

import functools
import logging
import unittest

import pynini

import scansion


class ScansionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with pynini.Far("../grammars/all.far", "r") as far:
            cls.scan_line = functools.partial(
                scansion.scan_line,
                far["NORMALIZE"],
                far["PRONOUNCE"],
                far["VARIABLE"],
                far["METER"],
            )

    # Tests all features of the first line's markup.
    def test_aen_1_1(self):
        text = "Arma virumque canō, Trojae quī prīmus ab ōris"
        line = self.scan_line(text, 1)
        self.assertEqual(line.line_number, 1)
        self.assertEqual(line.text, text)
        self.assertEqual(
            line.norm, "arma virumque canō trojae quī prīmus ab ōris"
        )
        self.assertEqual(
            line.pron, "arma wirũːkwe kanoː trojjaj kwiː priːmu sa boːris"
        )

    # Scans line 1.534, which is clearly defective (and in this case, it's
    # entirely possible Virgil never finished it).
    def test_aen_1_534(self):
        text = "Hic cursus fuit,"
        line = self.scan_line(text)
        self.assertEqual(line.norm, "hic cursus fuit")
        self.assertTrue(line.defective)

    # Tests that the grammar does not unnecessarily apply resyllabification.
    def test_aen_1_26(self):
        text = "exciderant animō; manet altā mente repostum"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "ekskiderant animoː mane taltaː mente repostũː"
        )

    # Tests that the grammar does not unnecessarily apply elision.
    def test_aen_1_26(self):
        text = "Ipsa Jovis rapidum jaculāta ē nūbibus ignem"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "ipsa jowis rapidũː jakulaːteː nuːbibu siŋnẽː"
        )

    def test_aen_1_247(self):
        text = "Hīc tamen ille urbem Patavī sēdēsque locāvit"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "hiːk tame nillurbẽː patawiː seːdeːskwe lokaːwit"
        )

    def test_aen_1_254(self):
        text = "Ollī subrīdēns hominum sator atque deōrum"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "olliː subriːdeːns hominũː sato ratkwe deoːrũː"
        )

    def test_aen_1_450(self):
        text = "Hōc prīmum in lūcō nova rēs oblāta timōrem"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "hoːk priːmin luːkoː nowa reːs oblaːta timoːrẽː"
        )

    def test_aen_1_477(self):
        text = "lōra tenēns tamen; huic cervīxque comaeque trahuntur"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "loːra teneːns tame nujk kerwiːkskwe komajkwe trahuntur"
        )

    def test_aen_1_593(self):
        text = "argentum Pariusve lapis circumdatur aurō."
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "argentũː pariuswe lapis kirkumdatu rawroː"
        )

    def test_aen_1_649(self):
        text = "et circumtextum croceō vēlāmen acanthō,"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "et kirkumtekstũː krokeoː weːlaːme nakantoː"
        )

    def test_aen_1_682(self):
        text = "nē quā scīre dolōs mediusve occurrere possit."
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "neː kwaː skiːre doloːs mediuswokkurrere possit"
        )

    def test_aen_1_697(self):
        text = "pallamque et pictum croceō vēlāmen acanthō."
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "pallãːkwet piktũː krokeoː weːlaːme nakantoː"
        )

    # Tests handling of brackets.
    def test_aen_2_77(self):
        text = "[Ille haec dēpositā tandem formīdine fātur:]"
        line = self.scan_line(text)
        self.assertEqual(
            line.norm, "ille haec dēpositā tandem formīdine fātur"
        )
        self.assertFalse(line.defective)

    # No poetic license rules required.
    def test_aen_2_202(self):
        text = "Lāocoön, ductus Neptūnō sorte sacerdōs,"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "laːokoon duktus neptuːnoː sorte sakerdoːs"
        )

    # Elision.
    def test_aen_2_219(self):
        text = "bis medium amplexī, bis collō squāmea circum"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "bis mediampleksiː bis kolloː skwaːmea kirkũː"
        )

    # Elision.
    def test_aen_2_278(self):
        text = "squālentem barbam et concrētōs sanguine crīnīs"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "skwaːlentẽː barbet koŋkreːtoːs saŋgwine kriːniːs"
        )

    # Defective line – first syllable is short.
    def test_aen_2_506(self):
        text = "procubuēre tenent danaī quā dēficit ignis"
        line = self.scan_line(text)
        self.assertTrue(line.defective)

    @unittest.skip("Requires diastole")
    def test_aen_2_675(self):
        text = "haerebat parvumque patrī tendēbat iūlum"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "hajrebat parwumkwe patriː tendeːba tiuːlũː"
        )

    @unittest.skip("Requires diastole")
    def test_aen_2_744(self):
        text = "vēnimus hīc demum collēctīs omnibus ūna"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "weːnimu siːk demũː kolleːktiːs omnibu suːna"
        )

    # "Trōia" is technically diastole, but Pharr takes
    # care of that as he did not rewrite the intervocalic "i" as "j".
    def test_aen_2_764(self):
        text = "praedam adservābant hūc undique trōia gaza"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "prajdadserwaːbant huːk undikwe troːia gazza"
        )
    
    # Not sure how to scan.
    def test_aen_3_158(self):
        text = "īdem ventūrōs tollemus in astra nepōtēs"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "iːdẽː wentuːroːs tollemus in astra nepoːteːs"
        )

    # Synizesis.
    def test_aen_3_161(self):
        text = "Mūtandae sēdēs. Nōn haec tibi lītora suāsit"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "muːtandaj seːdeːs noːn hajk tibi liːtora swaːsit"
        )

    # Harpyia is probably harpja?
    def test_aen_3_365(self):
        text = "sōla novum dictūque nefās Harpyia Celaenō"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "soːla nowũː diktuːkwe nefaːs harpuja kelajnoː"
        )

    # Check with Pharr.
    def test_aen_3_464(self):
        text = "dōna dehinc aurō gravia sectōque elephantō"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "doːna dehink awroː grawiac sektoːkwelepantoː"
        )

    @unittest.skip("Requires diastole")
    def test_aen_3_517(self):
        text = "armātumque aurō circumspicit Ōriōna"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "armaːtũːkwe awroː kirkumspiki toːriːoːna"
        )

    # Not sure how to scan.
    def test_aen_3_567(self):
        text = "ter spūmam ēlisam et rōrantia vīdimus astra."
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "ter spuːmeːlisa met roːrantia wiːdimu sastra"
        )

    @unittest.skip("Requires diastole")
    def test_aen_4_146(self):
        text = "Crētesque Dryopesque fremunt pictīque Agathyrsī:"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "kreːteskweː druopeskwe fremunt piktiːkwe agatursiː"
        )

    # Might want to geminate intervocalic "i"s as well.
    def test_aen_4_302(self):
        text = "Thyias, ubi audītō stimulant trietērica Bacchō"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "tujja subawdiːtoː stimulant trieteːrika bakkoː"
        )

    # Not sure how to scan.
    def test_aen_4_324(self):
        text = "(hoc solum nōmen quoniam dē conjuge restat)?"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, ""
        )

    # Space?
    def test_aen_4_369(self):
        text = " Num flētū ingemuit nostrō? Num lūmina flexit?"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "nũː fleːtiŋgemuit nostroː nũː luːmina fleksit"
        )

    # Might want to geminate intervocalic "i"s as well.
    def test_aen_4_569(self):
        text = "Heia age, rumpe morās. Varium et mūtābile semper"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "hejjage rumpe moraːs wariet muːtaːbile semper"
        )

    # Requires diastole in suoːrũː?
    def test_aen_4_617(self):
        text = "auxilium implōret videatque indigna suorum"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "awksiliimploːret wideatkwindiŋna suoːrũː"
        )

    # The pron grammar rewrites bijugō as bijjugoː, but it shouldn't
    # geminate.
    def test_aen_5_144(self):
        text = "Nōn tam praecipitēs bijugō certāmine campum"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "noːn tãː prajkipiteːs bijugoː kertaːmine kampũː"
        )

    @unittest.skip("Requires diastole")
    def test_aen_5_306(self):
        text = "Gnōsia bina dabō lēvātō lūcida ferrō"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "ŋnoːsia biːna daboː leːwaːtoː luːkida ferroː"
        )

    # Diaresis of "ī".
    def test_aen_5_352(self):
        text = "dat Salīo villīs onerōsum atque unguibus aureīs."
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "dat salioː williːs oneroːsatkwuŋgwibu sawrejs"
        )

    @unittest.skip("Requires diastole")
    def test_aen_5_520(self):
        text = "qui tamen āeriās tēlum contorsit in aurās"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "kwiː tame naːeriaːs teːlũː kontorsi ti nawraːs"
        )

    @unittest.skip("Requires diastole")
    def test_aen_5_687(self):
        text = '"Juppiter omnipotēns, si nōndum exōsus ad ūnum'
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "juppite romnipoteːns siː noːndeksoːsu sa duːnũː"
        )
    
    # Not sure how to scan.
    def test_aen_5_870(self):
        text = '"Ō nimium caelō et pelagō cōnfise serēnō'
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, ""
        )

    # Synizesis with "e".
    def test_aen_6_412(self):
        text = "dēturbat, laxatque forōs; simul accipit alveō"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "deːturbat laksatkwe foroːs simu lakkipi talwjoː"
        )

    # Synizesis of "eu". Might have to geminate "w" diphthongs?
    def test_aen_6_447(self):
        text = "Euadnēnque et Pāsiphaēn; hīs Lāodamīa"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "ewadneːŋkwet paːsipaeːn hiːs laːodamiːa"
        )

    @unittest.skip("Requires systole")
    def test_aen_6_507(self):
        text = "Nōmen et arma locum servant; tē, amīce, nequīvī"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "noːme ne tarma lokũː serwant te amiːke nekwiːwiː"
        )

    @unittest.skip("Requires diastole")
    def test_aen_6_637(self):
        text = "Hīs demum exāctīs, perfectō mūnere dīvae,"
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "hiːs deːmeksaːktiːs perfektoː muːnere diːwaj"
        )

    @unittest.skip("Requires diastole")
    def test_aen_6_695(self):
        text = 'Ille autem: "Tua me, genitor, tua trīstis imāgō'
        line = self.scan_line(text)
        self.assertEqual(
            line.pron, "illawtẽː tua meː genitor tua triːsti simaːgoː"
        )

if __name__ == "__main__":
    logging.disable("CRITICAL")
    unittest.main()
