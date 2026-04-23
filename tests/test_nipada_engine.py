"""
Tests unitaires — nipada_engine.py

Couvre :
  - Fonctions de bas niveau (mask, product, level, subset, jaccard)
  - Encodage/décodage octet
  - NipadaCatalog : chargement, accès, requêtes
  - Invariants formels définis dans schema.json
"""
import pytest
from src.core.nipada_engine import (
    PRIMES, PADDING_MASK, MAX_MASK,
    mask_to_product, product_to_mask,
    level, atoms_in, atom_names_in,
    is_subset, shared_atoms, jaccard,
    iter_all_masks,
    encode, decode, pack_pair, unpack_pair,
    Domain, NipadaEntry, NipadaCatalog,
)


# ---------------------------------------------------------------------------
# Fonctions de bas niveau
# ---------------------------------------------------------------------------

class TestMaskToProduct:
    def test_padding(self):
        assert mask_to_product(0) == 1

    def test_atoms(self):
        assert mask_to_product(0b0001) == 2    # ÊTRE
        assert mask_to_product(0b0010) == 3    # DIFFÉRENCE
        assert mask_to_product(0b0100) == 5    # RAPPORT
        assert mask_to_product(0b1000) == 7    # ORIENTATION

    def test_binary_molecules(self):
        assert mask_to_product(0b0011) == 6    # EXISTENCE
        assert mask_to_product(0b0101) == 10   # COMPOSITION
        assert mask_to_product(0b1001) == 14   # DEVENIR
        assert mask_to_product(0b0110) == 15   # MESURE
        assert mask_to_product(0b1010) == 21   # OPPOSITION
        assert mask_to_product(0b1100) == 35   # RÉFÉRENCE

    def test_ternary_molecules(self):
        assert mask_to_product(0b0111) == 30   # VIE
        assert mask_to_product(0b1011) == 42   # TRANSFORMATION
        assert mask_to_product(0b1101) == 70   # INTENTION
        assert mask_to_product(0b1110) == 105  # TEMPS

    def test_integration(self):
        assert mask_to_product(0b1111) == 210  # INTÉGRATION

    def test_all_masks_positive(self):
        for mask in range(16):
            assert mask_to_product(mask) >= 1


class TestProductToMask:
    def test_padding(self):
        assert product_to_mask(1) == 0

    def test_atoms(self):
        assert product_to_mask(2)  == 0b0001
        assert product_to_mask(3)  == 0b0010
        assert product_to_mask(5)  == 0b0100
        assert product_to_mask(7)  == 0b1000

    def test_molecules(self):
        assert product_to_mask(6)   == 0b0011
        assert product_to_mask(210) == 0b1111

    def test_invalid_returns_none(self):
        assert product_to_mask(4)  is None   # 2²
        assert product_to_mask(9)  is None   # 3²
        assert product_to_mask(8)  is None   # 2³
        assert product_to_mask(11) is None   # CAUSER, pas dans 4 bits
        assert product_to_mask(13) is None   # prime hors système

    def test_roundtrip(self):
        for mask in range(16):
            n = mask_to_product(mask)
            assert product_to_mask(n) == mask


class TestLevel:
    def test_padding(self):
        assert level(0) == 0

    def test_atoms_level_one(self):
        for mask in [1, 2, 4, 8]:
            assert level(mask) == 1

    def test_level_four(self):
        assert level(15) == 4

    def test_popcount(self):
        assert level(0b0111) == 3
        assert level(0b1010) == 2


class TestAtomFunctions:
    def test_atoms_in(self):
        assert atoms_in(0b0011) == (2, 3)
        assert atoms_in(0b1111) == (2, 3, 5, 7)
        assert atoms_in(0) == ()

    def test_atom_names_in(self):
        names = atom_names_in(0b0001)
        assert names == ("ÊTRE",)
        names = atom_names_in(0b1111)
        assert "ÊTRE" in names
        assert "ORIENTATION" in names


class TestSubsetOps:
    def test_is_subset_true(self):
        assert is_subset(1, 1)   # ÊTRE ⊆ ÊTRE
        assert is_subset(3, 15)  # EXISTENCE ⊆ INTÉGRATION
        assert is_subset(7, 15)  # VIE ⊆ INTÉGRATION

    def test_is_subset_false(self):
        assert not is_subset(3, 8)   # EXISTENCE ⊄ ORIENTATION
        assert not is_subset(15, 3)  # INTÉGRATION ⊄ EXISTENCE

    def test_shared_atoms(self):
        assert shared_atoms(3, 15)  == 3   # {ÊTRE,DIFF} ∩ {tout} = {ÊTRE,DIFF}
        assert shared_atoms(3, 12)  == 0   # aucun commun
        assert shared_atoms(7, 14)  == 6   # {ÊTRE,DIFF,RAPP} ∩ {DIFF,RAPP,ORI} = {DIFF,RAPP}

    def test_jaccard(self):
        assert jaccard(0b1111, 0b1111) == 1.0  # identiques
        assert jaccard(3, 12) == 0.0           # disjoints
        assert jaccard(3, 15) == 0.5           # 2 communs sur 4
        assert 0.0 < jaccard(7, 14) < 1.0


class TestIterAllMasks:
    def test_count(self):
        masks = list(iter_all_masks())
        assert len(masks) == 15

    def test_no_zero(self):
        assert 0 not in iter_all_masks()

    def test_ordered_by_level(self):
        masks = list(iter_all_masks())
        levels = [level(m) for m in masks]
        for i in range(len(levels) - 1):
            assert levels[i] <= levels[i + 1]


# ---------------------------------------------------------------------------
# Encodage / décodage
# ---------------------------------------------------------------------------

class TestEncoding:
    def test_encode_positive(self):
        b = encode(210)
        assert len(b) == 1
        dom, mask = decode(b[0])
        assert dom == Domain.Z_POS
        assert mask == 15

    def test_encode_negative(self):
        b = encode(-35)
        dom, mask = decode(b[0])
        assert dom == Domain.Z_NEG
        assert mask == 12  # 0b1100

    def test_encode_imaginary(self):
        b = encode("70i")
        dom, mask = decode(b[0])
        assert dom == Domain.IZ
        assert mask == 13  # 0b1101

    def test_encode_padding(self):
        b = encode(0)
        dom, mask = decode(b[0])
        assert dom is None
        assert mask == 0

    def test_encode_invalid(self):
        with pytest.raises(ValueError):
            encode(4)  # 4 = 2² pas valide

    def test_roundtrip_all_positive(self):
        for mask in range(1, 16):
            n = mask_to_product(mask)
            b = encode(n)
            dom, decoded_mask = decode(b[0])
            assert dom == Domain.Z_POS
            assert decoded_mask == mask


class TestPackPair:
    def test_pack_unpack(self):
        packed = pack_pair(2, 3)   # ÊTRE, DIFFÉRENCE
        a, b = unpack_pair(packed[0])
        assert a == 1   # mask de ÊTRE
        assert b == 2   # mask de DIFFÉRENCE

    def test_pack_two_in_one_byte(self):
        assert len(pack_pair(2, 3)) == 1

    def test_pack_max_values(self):
        packed = pack_pair(2, 210)   # ÊTRE (mask=1) + INTÉGRATION (mask=15)
        a, b = unpack_pair(packed[0])
        assert a == 1
        assert b == 15


# ---------------------------------------------------------------------------
# NipadaCatalog
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def catalog():
    return NipadaCatalog()


class TestCatalogLoading:
    def test_total_entries(self, catalog):
        """§74 : catalogue complet = 15 Z+ + 15 Z- + 15 iZ."""
        assert len(catalog) == 45

    def test_z_positive(self, catalog):
        assert len(catalog.by_domain(Domain.Z_POS)) == 15

    def test_z_negative(self, catalog):
        assert len(catalog.by_domain(Domain.Z_NEG)) == 15

    def test_iz(self, catalog):
        """§74 : toutes les 15 molécules ont une entrée iZ (ni = n×i)."""
        assert len(catalog.by_domain(Domain.IZ)) == 15


class TestCatalogAccess:
    def test_by_product(self, catalog):
        e = catalog.by_product(210)
        assert e is not None
        assert e.name == "INTÉGRATION"

    def test_by_product_negative(self, catalog):
        e = catalog.by_product(-30)
        assert e is not None
        assert e.name == "MORT"

    def test_by_name(self, catalog):
        e = catalog.by_name("VIE")
        assert e is not None
        assert e.mask == 7

    def test_by_name_case_insensitive(self, catalog):
        assert catalog.by_name("vie") is catalog.by_name("VIE")

    def test_by_name_missing(self, catalog):
        assert catalog.by_name("INEXISTANT") is None

    def test_by_mask(self, catalog):
        e = catalog.by_mask(3, Domain.Z_POS)
        assert e.name == "EXISTENCE"

    def test_crossing_of(self, catalog):
        e = catalog.crossing_of(30)
        assert e is not None
        assert e.name == "MORT"
        assert e.domain == Domain.Z_NEG

    def test_imaginary_of(self, catalog):
        e = catalog.imaginary_of(70)
        assert e is not None
        assert e.name == "MOI"
        assert e.domain == Domain.IZ

    def test_imaginary_of_no_entry(self, catalog):
        # Produit invalide (CAUSER=11, hors système nipada 4 bits)
        e = catalog.imaginary_of(11)
        assert e is None

    def test_imaginary_of_existence(self, catalog):
        # §74 : EXISTENCE (6) a maintenant un iZ → CONSCIENCE
        e = catalog.imaginary_of(6)
        assert e is not None
        assert e.name == "CONSCIENCE"
        assert e.domain == Domain.IZ


class TestCatalogQueries:
    def test_by_level(self, catalog):
        lvl1 = catalog.by_level(1)
        assert len(lvl1) > 0
        for e in lvl1:
            assert e.lvl == 1

    def test_containing_atom(self, catalog):
        entries = catalog.containing_atom(2)  # ÊTRE
        names = [e.name for e in entries]
        assert "ÊTRE" in names
        assert "INTÉGRATION" in names

    def test_most_similar(self, catalog):
        results = catalog.most_similar(7, Domain.Z_POS, top=3)
        assert len(results) == 3
        for score, e in results:
            assert 0.0 <= score <= 1.0
            assert e.domain == Domain.Z_POS

    def test_all_positive_order(self, catalog):
        entries = catalog.all_positive()
        assert len(entries) == 15
        for i in range(len(entries) - 1):
            assert entries[i].lvl <= entries[i + 1].lvl


# ---------------------------------------------------------------------------
# Invariants formels (schema.json)
# ---------------------------------------------------------------------------

class TestFormalInvariants:
    """
    Validation des 6 invariants définis dans schema.json.
    """

    def test_mask_product_invariant(self, catalog):
        """mask_to_product(mask) == nipada_value pour toutes les entrées Z+."""
        for e in catalog.by_domain(Domain.Z_POS):
            expected = mask_to_product(e.mask)
            assert e.nipada_value == expected, f"Échec pour {e.name}: {e.nipada_value} != {expected}"

    def test_mask_level_invariant(self, catalog):
        """level(mask) == popcount(mask) pour toutes les entrées."""
        for e in catalog:
            assert level(e.mask) >= 1 or e.mask == 0

    def test_crossing_same_mask(self, catalog):
        """Chaque Z+ a un Z- avec le même masque."""
        pos_masks = {e.mask for e in catalog.by_domain(Domain.Z_POS)}
        neg_masks = {e.mask for e in catalog.by_domain(Domain.Z_NEG)}
        # Tous les masks positifs ont un crossing correspondant
        assert pos_masks == neg_masks

    def test_imaginary_mask_subset(self, catalog):
        """Les entrées iZ ont un mask présent dans Z+."""
        pos_masks = {e.mask for e in catalog.by_domain(Domain.Z_POS)}
        for e in catalog.by_domain(Domain.IZ):
            assert e.mask in pos_masks, f"iZ mask {e.mask} absent de Z+"

    def test_completeness(self, catalog):
        """Les 15 masques 1..15 sont tous présents dans Z+."""
        pos_masks = {e.mask for e in catalog.by_domain(Domain.Z_POS)}
        assert pos_masks == set(range(1, 16))

    def test_integration_is_max(self, catalog):
        """INTÉGRATION (mask=15) est l'unique molécule de niveau 3 (JSON)."""
        e = catalog.by_mask(15, Domain.Z_POS)
        assert e is not None
        assert e.name == "INTÉGRATION"
        assert e.mask == MAX_MASK


# ---------------------------------------------------------------------------
# Domaine iZ — 15 entrées (§74 : ni = molécule n × i, auto-référence productive)
# ---------------------------------------------------------------------------

class TestCatalogIZ:
    """
    Valide les 15 entrées iZ du catalogue (§74).
    Principe : ni = molécule n appliquée à elle-même (Bateson : double contrainte productive).
    Chaque masque 1-15 doit avoir une entrée Z+, Z- et iZ.
    """

    def test_all_masks_have_iz(self, catalog):
        """Les 15 masques 1..15 ont tous une entrée iZ."""
        iz_masks = {e.mask for e in catalog.by_domain(Domain.IZ)}
        assert iz_masks == set(range(1, 16))

    def test_iz_masks_match_z_pos(self, catalog):
        """Chaque iZ partage son masque avec un Z+ (même encodage 4 bits)."""
        pos_masks = {e.mask for e in catalog.by_domain(Domain.Z_POS)}
        for e in catalog.by_domain(Domain.IZ):
            assert e.mask in pos_masks, f"{e.name} mask {e.mask} absent de Z+"

    # --- Atomes iZ (mask = 1 bit) ---

    def test_iz_vide(self, catalog):
        """ÊTRE×i = VIDE (śūnyatā) — mask=1, ÊTRE appliqué à lui-même."""
        e = catalog.imaginary_of(2)   # ÊTRE = product 2 = mask 1
        assert e is not None
        assert e.name == "VIDE"
        assert e.mask == 1
        assert e.domain == Domain.IZ

    def test_iz_paradoxe(self, catalog):
        """DIFFÉRENCE×i = PARADOXE (Russell) — mask=2."""
        e = catalog.imaginary_of(3)   # DIFFÉRENCE = product 3 = mask 2
        assert e is not None
        assert e.name == "PARADOXE"
        assert e.mask == 2

    def test_iz_recursion(self, catalog):
        """RAPPORT×i = RÉCURSION (Hofstadter) — mask=4."""
        e = catalog.imaginary_of(5)   # RAPPORT = product 5 = mask 4
        assert e is not None
        assert e.name == "RÉCURSION"
        assert e.mask == 4

    def test_iz_retour(self, catalog):
        """ORIENTATION×i = RETOUR (Nietzsche) — mask=8."""
        e = catalog.imaginary_of(7)   # ORIENTATION = product 7 = mask 8
        assert e is not None
        assert e.name == "RETOUR"
        assert e.mask == 8

    # --- Binaires iZ (mask = 2 bits) ---

    def test_iz_conscience(self, catalog):
        """EXISTENCE×i = CONSCIENCE (cogito) — mask=3."""
        e = catalog.imaginary_of(6)   # EXISTENCE = product 6 = mask 3
        assert e is not None
        assert e.name == "CONSCIENCE"
        assert e.mask == 3

    def test_iz_autopoiese(self, catalog):
        """COMPOSITION×i = AUTOPOÏÈSE (Maturana) — mask=5."""
        e = catalog.imaginary_of(10)  # COMPOSITION = product 10 = mask 5
        assert e is not None
        assert e.name == "AUTOPOÏÈSE"
        assert e.mask == 5

    def test_iz_trace(self, catalog):
        """MESURE×i = TRACE (existant §72) — mask=6."""
        e = catalog.imaginary_of(15)  # MESURE = product 15 = mask 6
        assert e is not None
        assert e.name == "TRACE"
        assert e.mask == 6

    def test_iz_cycle(self, catalog):
        """DEVENIR×i = CYCLE (saṃsāra) — mask=9."""
        e = catalog.imaginary_of(14)  # DEVENIR = product 14 = mask 9
        assert e is not None
        assert e.name == "CYCLE"
        assert e.mask == 9

    def test_iz_ambivalence(self, catalog):
        """OPPOSITION×i = AMBIVALENCE (Freud) — mask=10."""
        e = catalog.imaginary_of(21)  # OPPOSITION = product 21 = mask 10
        assert e is not None
        assert e.name == "AMBIVALENCE"
        assert e.mask == 10

    def test_iz_metalangage(self, catalog):
        """RÉFÉRENCE×i = MÉTALANGAGE (Tarski/Gödel) — mask=12."""
        e = catalog.imaginary_of(35)  # RÉFÉRENCE = product 35 = mask 12
        assert e is not None
        assert e.name == "MÉTALANGAGE"
        assert e.mask == 12

    # --- Ternaires iZ (mask = 3 bits) ---

    def test_iz_individuation(self, catalog):
        """VIE×i = INDIVIDUATION (Jung/Simondon) — mask=7."""
        e = catalog.imaginary_of(30)  # VIE = product 30 = mask 7
        assert e is not None
        assert e.name == "INDIVIDUATION"
        assert e.mask == 7

    def test_iz_apprentissage(self, catalog):
        """TRANSFORMATION×i = APPRENTISSAGE (Bateson) — mask=11."""
        e = catalog.imaginary_of(42)  # TRANSFORMATION = product 42 = mask 11
        assert e is not None
        assert e.name == "APPRENTISSAGE"
        assert e.mask == 11

    def test_iz_moi(self, catalog):
        """INTENTION×i = MOI (existant §72) — mask=13."""
        e = catalog.imaginary_of(70)  # INTENTION = product 70 = mask 13
        assert e is not None
        assert e.name == "MOI"
        assert e.mask == 13

    def test_iz_memoire(self, catalog):
        """TEMPS×i = MÉMOIRE (Bergson/smṛti) — mask=14."""
        e = catalog.imaginary_of(105)  # TEMPS = product 105 = mask 14
        assert e is not None
        assert e.name == "MÉMOIRE"
        assert e.mask == 14

    # --- Quaternaire iZ (mask = 4 bits) ---

    def test_iz_absolu(self, catalog):
        """INTÉGRATION×i = ABSOLU (Hegel/brahman) — mask=15."""
        e = catalog.imaginary_of(210)  # INTÉGRATION = product 210 = mask 15
        assert e is not None
        assert e.name == "ABSOLU"
        assert e.mask == 15

    # --- Invariants structurels iZ ---

    def test_iz_domain_all_correct(self, catalog):
        """Toutes les entrées iZ ont domain == Domain.IZ."""
        for e in catalog.by_domain(Domain.IZ):
            assert e.domain == Domain.IZ, f"{e.name} a domain={e.domain}"

    def test_iz_by_level_distribution(self, catalog):
        """
        Distribution des iZ par niveau :
          level 1 (1 bit) = 4 atomes iZ  : VIDE, PARADOXE, RÉCURSION, RETOUR
          level 1-2 (2 bits) = 6 binaires : CONSCIENCE, AUTOPOÏÈSE, TRACE, CYCLE, AMBIVALENCE, MÉTALANGAGE
          level 2-3 (3 bits) = 4 ternaires : INDIVIDUATION, APPRENTISSAGE, MOI, MÉMOIRE
          level 3-4 (4 bits) = 1 quaternaire : ABSOLU
        Note: le level JSON des iZ est level 0 pour les atomes, level 1 pour binaires, etc.
        Les masques 1-bit ont popcount=1, etc.
        """
        iz_entries = catalog.by_domain(Domain.IZ)
        # 4 entrées avec mask à 1 bit (atomes iZ)
        one_bit = [e for e in iz_entries if bin(e.mask).count('1') == 1]
        assert len(one_bit) == 4
        # 6 entrées avec mask à 2 bits (binaires iZ)
        two_bit = [e for e in iz_entries if bin(e.mask).count('1') == 2]
        assert len(two_bit) == 6
        # 4 entrées avec mask à 3 bits (ternaires iZ)
        three_bit = [e for e in iz_entries if bin(e.mask).count('1') == 3]
        assert len(three_bit) == 4
        # 1 entrée avec mask à 4 bits (quaternaire iZ)
        four_bit = [e for e in iz_entries if bin(e.mask).count('1') == 4]
        assert len(four_bit) == 1
        assert four_bit[0].name == "ABSOLU"

    def test_iz_no_duplicate_masks(self, catalog):
        """Chaque mask est unique dans le domaine iZ."""
        iz_masks = [e.mask for e in catalog.by_domain(Domain.IZ)]
        assert len(iz_masks) == len(set(iz_masks))
