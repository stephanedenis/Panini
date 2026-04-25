#!/usr/bin/env python3
"""
§104 — Fondations astronomiques : précisions cosmiques + référentiels célestes
================================================================================

Extension de §103 vers le haut (cosmos) et latéralement (référentiels non
géocentrés). Quatre raffinements simultanés :

1. **Échelle géo étendue vers le cosmique** — depuis le mètre jusqu'au
   rayon de Hubble (1.4e26 m). Le plancher Planck reste pertinent (échelle
   quantique de l'univers primordial).

2. **Échelle temps étendue vers le cosmique** — depuis la seconde jusqu'à
   l'âge de l'univers (4.35e17 s). Le plancher Planck temps reste valide
   (premier instant de l'univers).

3. **Coordonnées célestes alternatives** à (lat, lon) — le système solaire,
   la Galaxie et l'univers ne sont pas géocentrés. Frames supportés :
   ICRS / FK5 / galactic / ecliptic / heliocentric / barycentric / CMB.

4. **Distinguer `occurred_at` et `observed_at`** — un événement astronomique
   a deux dates : l'instant cosmique de production (référentiel local de la
   source) et l'instant d'arrivée du front d'onde sur Terre. Le `light-travel
   time` les sépare. SN 1987A : *occurred* il y a ~168 000 ans dans le LMC ;
   *observed* le 23 février 1987 à Kamiokande puis Las Campanas.

Le graphe causal §103 (CAUSALITÉ = 195) reste valide tel quel — le sens
« progéniteur » dans l'évolution stellaire (nuage → protoétoile → MS →
géante → SN → résidu compact) suit le même `LIEN_GÉNÉALOGIQUE = 55`.

Sortie :
  - research/nipada/encyclopedie/astronomie/precisions_cosmiques.json
  - research/nipada/encyclopedie/astronomie/objets_celestes.json
  - research/nipada/encyclopedie/astronomie/evenements_astronomiques.json
"""

from __future__ import annotations

import json
from functools import reduce
from operator import mul
from pathlib import Path
from typing import TypedDict

REPO_ROOT = Path(__file__).resolve().parent.parent
ENC_DIR = REPO_ROOT / "research" / "nipada" / "encyclopedie"
ASTRO_DIR = ENC_DIR / "astronomie"


# ══════════════════════════════════════════════════════════════════════════════
# 1. PRÉCISIONS COSMIQUES (extension de §103 vers le haut)
# ══════════════════════════════════════════════════════════════════════════════

# Constantes physiques (SI)
PARSEC_M = 3.0857e16            # 1 pc
LIGHT_YEAR_M = 9.4607e15        # 1 ly
ASTRONOMICAL_UNIT_M = 1.496e11  # 1 UA
SOLAR_RADIUS_M = 6.957e8        # R☉
EARTH_RADIUS_M = 6.371e6        # R⊕
HUBBLE_RADIUS_M = 1.4e26        # c/H₀ avec H₀=67.4 km/s/Mpc
JULIAN_YEAR_S = 3.15576e7       # année julienne (365.25 jours)
AGE_UNIVERSE_S = 13.787e9 * JULIAN_YEAR_S  # 13.787 Gyr Planck 2018

# Extension géo : depuis 1 m jusqu'au rayon de Hubble.
# Format identique à §103 : (class, meters, exemple).
PRECISIONS_COSMIQUES_GEO: list[tuple[str, float, str]] = [
    ("rayon_hubble",         HUBBLE_RADIUS_M,           "horizon cosmologique observable"),
    ("gigaparsec",           1e3 * 1e6 * PARSEC_M,      "structure à grande échelle (Gpc)"),
    ("hectomegaparsec",      1e2 * 1e6 * PARSEC_M,      "superamas / vide cosmique"),
    ("megaparsec",           1e6 * PARSEC_M,            "Mpc — distance amas voisin (Virgo ≈ 16.5 Mpc)"),
    ("hectokiloparsec",      1e2 * 1e3 * PARSEC_M,      "Groupe local (~1 Mpc)"),
    ("decakiloparsec",       1e1 * 1e3 * PARSEC_M,      "diamètre Voie lactée (~30 kpc)"),
    ("kiloparsec",           1e3 * PARSEC_M,            "kpc — distance Sgr A* (~8 kpc)"),
    ("hectoparsec",          1e2 * PARSEC_M,            "amas globulaire ; bras spiral local"),
    ("decaparsec",           1e1 * PARSEC_M,            "voisinage stellaire dense"),
    ("parsec",               PARSEC_M,                  "pc — Proxima Cen (1.30 pc)"),
    ("annee_lumiere",        LIGHT_YEAR_M,              "ly (équivalent ≈ 0.307 pc)"),
    ("decasysteme_solaire",  1e3 * ASTRONOMICAL_UNIT_M, "héliopause (~120 UA)"),
    ("systeme_solaire",      1e2 * ASTRONOMICAL_UNIT_M, "ceinture de Kuiper (~50 UA)"),
    ("orbite_externe",       1e1 * ASTRONOMICAL_UNIT_M, "Saturne ≈ 9.5 UA"),
    ("unite_astronomique",   ASTRONOMICAL_UNIT_M,       "UA — distance Terre-Soleil"),
    ("gigametre",            1e9,                       "Gm — diamètre Jupiter (140 Gm)"),
    ("rayon_solaire",        SOLAR_RADIUS_M,            "R☉ — étoile de séquence principale"),
    ("rayon_terrestre",      EARTH_RADIUS_M,            "R⊕"),
    ("megametre",            1e6,                       "Mm — diamètre lunaire (3.5 Mm)"),
    # Plancher : on retombe sur les classes §103 à partir de planete (1e7) déjà couvertes.
]

# Extension temps : depuis 1 seconde jusqu'à l'âge de l'univers.
PRECISIONS_COSMIQUES_TEMPS: list[tuple[str, float, str]] = [
    ("age_univers",          AGE_UNIVERSE_S,            "13.787 Gyr (Planck 2018)"),
    ("gigaannee",            1e9 * JULIAN_YEAR_S,       "Gyr — formation Voie lactée (~13.6 Gyr)"),
    ("hectomegaannee",       1e8 * JULIAN_YEAR_S,       "période orbitale galactique (~230 Myr)"),
    ("decamegaannee",        1e7 * JULIAN_YEAR_S,       "vie d'une étoile O massive (~10 Myr)"),
    ("megaannee",            1e6 * JULIAN_YEAR_S,       "Myr — phases d'évolution stellaire"),
    ("hectokiloannee",       1e5 * JULIAN_YEAR_S,       "âge SN 1987A (vue depuis le LMC)"),
    ("decakiloannee",        1e4 * JULIAN_YEAR_S,       "civilisations préhistoriques tardives"),
    ("kiloannee",            1e3 * JULIAN_YEAR_S,       "kyr — vie d'une supernova rémanente jeune"),
    # Plancher : on retombe sur les classes §103 (eon_geologique=1e16 s, etc.)
    # NOTE: kiloannee ≈ 3.16e10 s couvre la lacune entre §103.eon_geologique
    # (1e16 s) et §103.epoque_historique (1e10 s) — voir validation.
]


def _index(seq: list[tuple[str, float, str]]) -> dict[str, dict]:
    return {cls: {"value": v, "exemple": ex, "rank": i}
            for i, (cls, v, ex) in enumerate(seq)}


GEO_INDEX = _index(PRECISIONS_COSMIQUES_GEO)
TEMPS_INDEX = _index(PRECISIONS_COSMIQUES_TEMPS)


# ══════════════════════════════════════════════════════════════════════════════
# 2. RÉFÉRENTIELS CÉLESTES
# ══════════════════════════════════════════════════════════════════════════════

FRAMES = {
    "ICRS":         "International Celestial Reference System (quasi-inertiel, défini par quasars)",
    "FK5_J2000":    "Fifth Fundamental Catalogue à l'époque J2000.0",
    "galactic":     "Coordonnées galactiques (l, b) ; centre = Sgr A* ; plan = Voie lactée",
    "ecliptic":     "Plan de l'écliptique (orbite terrestre) ; utilisé en mécanique céleste",
    "heliocentric": "Centré sur le Soleil ; sans correction de mouvement",
    "ssb":          "Solar System Barycentric (point de Lagrange massique du système solaire)",
    "lsr":          "Local Standard of Rest (référentiel des étoiles voisines moyennes)",
    "cmb":          "Référentiel comobile du fond diffus cosmologique (« vrai immobile »)",
    "geocentric":   "Centré sur le centre de masse de la Terre (sans rotation)",
    "topocentric":  "Centré sur l'observateur en surface (avec rotation et altitude)",
}


# ══════════════════════════════════════════════════════════════════════════════
# 3. SCHÉMAS
# ══════════════════════════════════════════════════════════════════════════════

class CoordonneesCelestes(TypedDict):
    frame: str                          # une clé de FRAMES
    # Position angulaire : selon le frame, (ra,dec) ou (l,b) ou (λ,β)
    ra_deg: float | None                # ascension droite OU longitude galactique l
    dec_deg: float | None               # déclinaison OU latitude galactique b
    # Distance et précision (le concept §103 reste valide, élargi)
    distance_m: float | None            # NULL si non mesuré (objets cosmologiques z seul)
    distance_precision_class: str | None  # clé de GEO_INDEX ou §103
    distance_precision_meters: float | None
    # Méthode de détermination (impacte la précision)
    distance_method: str | None         # "parallax", "spectroscopic_parallax", "cepheid",
                                        # "type_ia_sn", "redshift_hubble_law", "GW_standard_siren"
    # Position dépend du temps (mouvement propre, parallaxe annuelle)
    epoch: str                          # "J2000.0", "J2024.5", etc.
    pm_ra_mas_yr: float | None          # mouvement propre en RA (mas/an)
    pm_dec_mas_yr: float | None         # mouvement propre en Dec
    radial_velocity_km_s: float | None  # vitesse radiale héliocentrique
    parallax_mas: float | None          # parallaxe annuelle (mas)
    redshift_z: float | None            # cosmologique pour les sources lointaines


class IdentifiantsCatalogues(TypedDict):
    """Cross-references vers les grands catalogues astronomiques."""
    common_names: list[str]             # ["Soleil", "Sun", "Sol", "太陽", "सूर्य"…]
    hd: str | None                      # Henry Draper Catalogue
    hip: str | None                     # Hipparcos
    gaia_dr3: str | None                # Gaia Data Release 3
    messier: str | None                 # M1, M31, …
    ngc: str | None                     # NGC 224, …
    simbad: str | None                  # identifiant principal SIMBAD
    other: dict[str, str]               # catalogues spécialisés (2MASS, IRAS, PSR, GW…)


class ObjetCeleste(TypedDict):
    """
    Objet astronomique persistant. Joue le rôle d'« auteur » pour les
    événements astronomiques où il est sujet (étoile progénitrice de SN,
    pulsar émetteur, etc.) ; nipada_type = 2002 (COORDONNÉE_VITALE), même
    signature qu'un auteur humain — un objet céleste est un sujet situé.
    """
    id: str
    nipada_type: int                    # 2002 = être × orientation × sujet × temps
    nipada_atoms: list[int]
    classe: str                         # "etoile", "planete", "trou_noir", "galaxie",
                                        # "amas", "nebuleuse", "pulsar", "fond_cosmologique"
    sous_classe: str | None             # MS_G2V, supermassif, spirale_SBc, etc.
    coords: CoordonneesCelestes
    catalogues: IdentifiantsCatalogues
    masse_kg: float | None
    luminosite_w: float | None
    age_s: float | None                 # âge de l'objet (si applicable et estimable)
    age_precision_class: str | None
    notes: str


class EvenementAstronomique(TypedDict):
    """
    Étend Evenement de §103 avec deux temps distincts (occurred / observed)
    et coordonnées célestes en lieu et place de lieu géoréférencé.

    nipada_type :
      2730  = ÉVÉNEMENT (sans sujet : éclipse vue depuis Terre, FRB anonyme)
      30030 = ÉVÉNEMENT_INDIVIDUEL (avec sujet stellaire identifié)
      510510 = ÉVÉNEMENT_MODAL (prédiction, événement attendu)
    """
    id: str
    nipada_type: int
    nipada_atoms: list[int]
    has_sujets: bool
    name: str | None
    description: str

    # Deux temps distincts
    occurred_at: dict                   # DateImprecise : instant cosmique local
    observed_at: dict | None            # DateImprecise : arrivée sur Terre (None si non encore observé)
    light_travel_time_s: float | None   # observed - occurred (en secondes)

    # Localisation céleste plutôt que terrestre
    coords: CoordonneesCelestes

    # Sujets (objets célestes impliqués)
    sujets: list[str]                   # objet_ids
    causes: list[str]                   # event_ids antécédents
    effets: list[str]                   # event_ids conséquents
    notes: str


# ══════════════════════════════════════════════════════════════════════════════
# 4. SEED — 7 OBJETS CÉLESTES
# ══════════════════════════════════════════════════════════════════════════════

OBJETS: list[ObjetCeleste] = [
    {
        "id": "soleil",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "classe": "etoile", "sous_classe": "G2V (séquence principale)",
        "coords": {
            "frame": "heliocentric",
            "ra_deg": None, "dec_deg": None,
            "distance_m": 0.0, "distance_precision_class": "rayon_solaire",
            "distance_precision_meters": SOLAR_RADIUS_M,
            "distance_method": None,
            "epoch": "J2000.0",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": 0.0, "parallax_mas": None, "redshift_z": 0.0,
        },
        "catalogues": {
            "common_names": ["Soleil", "Sun", "Sol", "太陽", "सूर्य", "الشمس", "Ηλιος"],
            "hd": None, "hip": None, "gaia_dr3": None,
            "messier": None, "ngc": None, "simbad": "Sun",
            "other": {},
        },
        "masse_kg": 1.989e30, "luminosite_w": 3.828e26,
        "age_s": 4.6e9 * JULIAN_YEAR_S,
        "age_precision_class": "hectomegaannee",
        "notes": "Étoile de référence ; définit le référentiel heliocentric.",
    },
    {
        "id": "proxima_centauri",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "classe": "etoile", "sous_classe": "M5.5Ve (naine rouge à éruptions)",
        "coords": {
            "frame": "ICRS",
            "ra_deg": 217.4290, "dec_deg": -62.6795,
            "distance_m": 1.301 * PARSEC_M,
            "distance_precision_class": "decaparsec",
            "distance_precision_meters": 1e1 * PARSEC_M / 1000,  # parallaxe Gaia ≈ 0.001 pc
            "distance_method": "parallax",
            "epoch": "J2016.0",
            "pm_ra_mas_yr": -3781.741, "pm_dec_mas_yr": 769.465,
            "radial_velocity_km_s": -22.4, "parallax_mas": 768.0665, "redshift_z": None,
        },
        "catalogues": {
            "common_names": ["Proxima Centauri", "Proxima Cen", "α Cen C"],
            "hd": None, "hip": "70890", "gaia_dr3": "5853498713190525696",
            "messier": None, "ngc": None, "simbad": "Proxima Cen",
            "other": {"glasse": "GJ 551"},
        },
        "masse_kg": 0.1221 * 1.989e30, "luminosite_w": 0.0017 * 3.828e26,
        "age_s": 4.85e9 * JULIAN_YEAR_S,
        "age_precision_class": "hectomegaannee",
        "notes": "Étoile la plus proche du Soleil ; héberge Proxima b, c, d.",
    },
    {
        "id": "sanduleak_69_202",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "classe": "etoile", "sous_classe": "B3Ia (supergéante bleue) — progénitrice SN 1987A",
        "coords": {
            "frame": "ICRS",
            "ra_deg": 83.86658, "dec_deg": -69.26978,
            "distance_m": 49.97 * 1e3 * PARSEC_M,
            "distance_precision_class": "kiloparsec",
            "distance_precision_meters": 1e3 * PARSEC_M,
            "distance_method": "eclipsing_binary_LMC",
            "epoch": "J2000.0",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": 286.0, "parallax_mas": None, "redshift_z": None,
        },
        "catalogues": {
            "common_names": ["Sanduleak −69° 202", "Sk -69 202"],
            "hd": None, "hip": None, "gaia_dr3": None,
            "messier": None, "ngc": None, "simbad": "Sk -69 202",
            "other": {"sanduleak": "Sk -69 202"},
        },
        "masse_kg": 18.0 * 1.989e30, "luminosite_w": 1.0e5 * 3.828e26,
        "age_s": 1.0e7 * JULIAN_YEAR_S,
        "age_precision_class": "decamegaannee",
        "notes": "Disparue le 23 fév 1987 (heure terrestre) ; vestige = "
                 "hypothétique étoile à neutrons non encore détectée dans SN 1987A.",
    },
    {
        "id": "sgr_a_etoile",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "classe": "trou_noir", "sous_classe": "supermassif (centre galactique)",
        "coords": {
            "frame": "galactic",
            "ra_deg": 0.0, "dec_deg": 0.0,   # centre du frame galactique par construction
            "distance_m": 8.178 * 1e3 * PARSEC_M,
            "distance_precision_class": "decaparsec",
            "distance_precision_meters": 1e1 * PARSEC_M * 1.3,
            "distance_method": "S_star_orbits",
            "epoch": "J2000.0",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None, "redshift_z": None,
        },
        "catalogues": {
            "common_names": ["Sagittarius A*", "Sgr A*"],
            "hd": None, "hip": None, "gaia_dr3": None,
            "messier": None, "ngc": None, "simbad": "Sgr A*",
            "other": {},
        },
        "masse_kg": 4.297e6 * 1.989e30, "luminosite_w": None,
        "age_s": None,
        "age_precision_class": None,
        "notes": "Trou noir supermassif au centre de la Voie lactée. "
                 "Image directe par EHT en 2022.",
    },
    {
        "id": "gw150914_bh1",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "classe": "trou_noir", "sous_classe": "stellaire (~36 M☉ pré-fusion)",
        "coords": {
            "frame": "ICRS",
            # GW150914 est mal localisé (sky area ~600 deg²) — précision angulaire faible
            "ra_deg": 112.5, "dec_deg": -70.0,   # centre approximatif région crédible
            "distance_m": 410 * 1e6 * PARSEC_M,
            "distance_precision_class": "hectomegaparsec",
            "distance_precision_meters": 160 * 1e6 * PARSEC_M,  # ±160 Mpc
            "distance_method": "GW_standard_siren",
            "epoch": "J2015.7",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None, "redshift_z": 0.09,
        },
        "catalogues": {
            "common_names": ["GW150914 progénitor 1"],
            "hd": None, "hip": None, "gaia_dr3": None,
            "messier": None, "ngc": None, "simbad": None,
            "other": {"ligo": "GW150914-bh1"},
        },
        "masse_kg": 35.6 * 1.989e30, "luminosite_w": None,
        "age_s": None,
        "age_precision_class": None,
        "notes": "Pré-fusion. Existe seulement comme état antérieur au merger.",
    },
    {
        "id": "gw150914_bh2",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "classe": "trou_noir", "sous_classe": "stellaire (~30 M☉ pré-fusion)",
        "coords": {
            "frame": "ICRS",
            "ra_deg": 112.5, "dec_deg": -70.0,
            "distance_m": 410 * 1e6 * PARSEC_M,
            "distance_precision_class": "hectomegaparsec",
            "distance_precision_meters": 160 * 1e6 * PARSEC_M,
            "distance_method": "GW_standard_siren",
            "epoch": "J2015.7",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None, "redshift_z": 0.09,
        },
        "catalogues": {
            "common_names": ["GW150914 progénitor 2"],
            "hd": None, "hip": None, "gaia_dr3": None,
            "messier": None, "ngc": None, "simbad": None,
            "other": {"ligo": "GW150914-bh2"},
        },
        "masse_kg": 30.6 * 1.989e30, "luminosite_w": None,
        "age_s": None,
        "age_precision_class": None,
        "notes": "Pré-fusion. Compagnon binaire de gw150914_bh1.",
    },
    {
        "id": "cmb",
        "nipada_type": 2002, "nipada_atoms": [2, 7, 11, 13],
        "classe": "fond_cosmologique", "sous_classe": "rayonnement de corps noir T=2.7255 K",
        "coords": {
            "frame": "cmb",
            "ra_deg": None, "dec_deg": None,        # fond isotrope par définition
            "distance_m": 14.0e9 * LIGHT_YEAR_M,    # distance comobile à la surface de dernière diffusion
            "distance_precision_class": "gigaparsec",
            "distance_precision_meters": 1e9 * PARSEC_M,
            "distance_method": "comoving_distance_LCDM",
            "epoch": "J2000.0",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None, "redshift_z": 1089.8,
        },
        "catalogues": {
            "common_names": ["fond diffus cosmologique", "CMB", "rayonnement fossile"],
            "hd": None, "hip": None, "gaia_dr3": None,
            "messier": None, "ngc": None, "simbad": None,
            "other": {"planck_collaboration": "CMB"},
        },
        "masse_kg": None, "luminosite_w": None,
        "age_s": (13.787e9 - 0.0003787e9) * JULIAN_YEAR_S,  # depuis le Big Bang
        "age_precision_class": "megaannee",
        "notes": "Origine : recombinaison à z=1089.8, ~378 000 ans après le Big Bang. "
                 "Définit le seul référentiel quasi-absolu de l'univers observable.",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# 5. SEED — 6 ÉVÉNEMENTS ASTRONOMIQUES (graphe causal)
# ══════════════════════════════════════════════════════════════════════════════

EVENEMENTS_ASTRO: list[EvenementAstronomique] = [
    {
        "id": "big_bang",
        "nipada_type": 2730, "nipada_atoms": [2, 3, 5, 7, 13],
        "has_sujets": False,
        "name": "Big Bang",
        "description": "Singularité initiale ; t = 0 dans le modèle ΛCDM standard. "
                       "Limite de validité de la physique connue (échelles de Planck).",
        "occurred_at": {"iso": "-13787000000",
                        "precision_class": "megaannee",
                        "precision_seconds": 1e6 * JULIAN_YEAR_S,
                        "uncertain": True,
                        "notes": "13.787 ± 0.020 Gyr (Planck 2018)"},
        "observed_at": None,                  # le Big Bang lui-même n'est pas observable directement
        "light_travel_time_s": None,
        "coords": {
            "frame": "cmb",
            "ra_deg": None, "dec_deg": None,
            "distance_m": None, "distance_precision_class": None,
            "distance_precision_meters": None,
            "distance_method": None,
            "epoch": "J2000.0",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None,
            "redshift_z": float("inf"),
        },
        "sujets": [],
        "causes": [],
        "effets": ["recombinaison_cmb"],
        "notes": "Événement-frontière. Cause sans cause antécédente connue.",
    },
    {
        "id": "recombinaison_cmb",
        "nipada_type": 2730, "nipada_atoms": [2, 3, 5, 7, 13],
        "has_sujets": False,
        "name": "Recombinaison (surface de dernière diffusion)",
        "description": "Découplage matière-rayonnement ~378 000 ans après le Big Bang. "
                       "Émission du fond diffus cosmologique observable aujourd'hui.",
        "occurred_at": {"iso": "-13786622000",
                        "precision_class": "kiloannee",
                        "precision_seconds": 1e3 * JULIAN_YEAR_S,
                        "uncertain": True,
                        "notes": "z = 1089.8 ± 0.2 (Planck 2018)"},
        "observed_at": {"iso": "1965-05-20",   # détection Penzias & Wilson
                        "precision_class": "annee",
                        "precision_seconds": JULIAN_YEAR_S,
                        "uncertain": False,
                        "notes": "Première détection radio par Penzias & Wilson, Holmdel NJ"},
        "light_travel_time_s": 13.787e9 * JULIAN_YEAR_S - 378e3 * JULIAN_YEAR_S,
        "coords": {
            "frame": "cmb",
            "ra_deg": None, "dec_deg": None,    # observé sur tout le ciel
            "distance_m": 14.0e9 * LIGHT_YEAR_M,
            "distance_precision_class": "gigaparsec",
            "distance_precision_meters": 1e9 * PARSEC_M,
            "distance_method": "comoving_distance_LCDM",
            "epoch": "J2000.0",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None,
            "redshift_z": 1089.8,
        },
        "sujets": [],
        "causes": ["big_bang"],
        "effets": [],
        "notes": "Premier événement astronomique observable. "
                 "occurred_at et observed_at séparés de ~13.79 Gyr.",
    },
    {
        "id": "sn_1987a_explosion",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Supernova 1987A (explosion progénitrice)",
        "description": "Effondrement gravitationnel du cœur de Sanduleak −69° 202 "
                       "dans le Grand Nuage de Magellan. Émission massive de neutrinos "
                       "puis flash optique trois heures plus tard.",
        "occurred_at": {"iso": "-0166013-02-23",  # ~168 000 ans avant 1987 (LMC à 50 kpc)
                        "precision_class": "hectokiloannee",
                        "precision_seconds": 1e5 * JULIAN_YEAR_S,
                        "uncertain": True,
                        "notes": "Date locale dans le LMC ; calculée depuis observed_at "
                                 "− light_travel_time. Précision dominée par incertitude "
                                 "sur la distance LMC (±5%)."},
        "observed_at": {"iso": "1987-02-23T07:35:35Z",
                        "precision_class": "seconde",
                        "precision_seconds": 1.0,
                        "uncertain": False,
                        "notes": "Première détection : neutrinos à Kamiokande-II, IMB, "
                                 "Baksan le 23 fév 1987 07:35:35 UTC. Optique ~3h plus tard "
                                 "à Las Campanas."},
        "light_travel_time_s": 49.97e3 * PARSEC_M / 2.998e8,  # 50 kpc / c ≈ 5.3e12 s ≈ 168 000 yr
        "coords": {
            "frame": "ICRS",
            "ra_deg": 83.86658, "dec_deg": -69.26978,
            "distance_m": 49.97 * 1e3 * PARSEC_M,
            "distance_precision_class": "kiloparsec",
            "distance_precision_meters": 1e3 * PARSEC_M,
            "distance_method": "eclipsing_binary_LMC",
            "epoch": "J2000.0",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": 286.0, "parallax_mas": None, "redshift_z": None,
        },
        "sujets": ["sanduleak_69_202"],
        "causes": [],
        "effets": ["sn_1987a_neutrinos_terre", "sn_1987a_flash_optique_terre"],
        "notes": "Le SUJET (Sanduleak −69° 202) cesse d'exister en tant qu'étoile "
                 "lors de cet événement. Discordance temporelle radicale entre "
                 "occurred_at (Pléistocène) et observed_at (1987) : 168 000 ans.",
    },
    {
        "id": "sn_1987a_neutrinos_terre",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Détection des neutrinos de SN 1987A",
        "description": "Arrivée du flux de neutrinos à Kamiokande-II (Japon), IMB (USA) "
                       "et Baksan (URSS). 24 événements neutrinos détectés en ~13 secondes.",
        "occurred_at": {"iso": "1987-02-23T07:35:35Z",
                        "precision_class": "seconde",
                        "precision_seconds": 1.0,
                        "uncertain": False,
                        "notes": "Burst de 13 secondes ; consensus inter-détecteurs"},
        "observed_at": {"iso": "1987-02-23T07:35:35Z",
                        "precision_class": "seconde",
                        "precision_seconds": 1.0,
                        "uncertain": False,
                        "notes": "Identique à occurred_at par construction (event terrestre)"},
        "light_travel_time_s": 0.0,
        "coords": {
            "frame": "topocentric",
            "ra_deg": 83.86658, "dec_deg": -69.26978,  # direction d'arrivée
            "distance_m": 0.0,                          # détection = ici
            "distance_precision_class": "kilometre",
            "distance_precision_meters": 1e3,
            "distance_method": None,
            "epoch": "J1987.15",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None, "redshift_z": None,
        },
        "sujets": ["sanduleak_69_202"],
        "causes": ["sn_1987a_explosion"],
        "effets": [],
        "notes": "Particularité : occurred_at == observed_at car l'événement EST la détection. "
                 "Le neutrino est presque sans masse → arrive ~3h avant le photon (le photon "
                 "est ralenti par sa traversée de l'enveloppe stellaire en explosion).",
    },
    {
        "id": "sn_1987a_flash_optique_terre",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Détection optique de SN 1987A",
        "description": "Découverte visuelle par Ian Shelton à Las Campanas (Chili) "
                       "et Albert Jones (Nouvelle-Zélande). Magnitude apparente +4.5 au pic.",
        "occurred_at": {"iso": "1987-02-24T05:30:00Z",
                        "precision_class": "heure",
                        "precision_seconds": 3600.0,
                        "uncertain": False,
                        "notes": "~21h45 après le burst neutrinos, soit ~3h après "
                                 "le déclenchement optique réel"},
        "observed_at": {"iso": "1987-02-24T05:30:00Z",
                        "precision_class": "heure",
                        "precision_seconds": 3600.0,
                        "uncertain": False,
                        "notes": "Identique à occurred_at"},
        "light_travel_time_s": 0.0,
        "coords": {
            "frame": "topocentric",
            "ra_deg": 83.86658, "dec_deg": -69.26978,
            "distance_m": 0.0,
            "distance_precision_class": "kilometre",
            "distance_precision_meters": 1e3,
            "distance_method": None,
            "epoch": "J1987.15",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None, "redshift_z": None,
        },
        "sujets": ["sanduleak_69_202"],
        "causes": ["sn_1987a_explosion"],
        "effets": [],
        "notes": "Plus brillante SN visible à l'œil nu depuis SN 1604 (Kepler).",
    },
    {
        "id": "gw150914_merger",
        "nipada_type": 30030, "nipada_atoms": [2, 3, 5, 7, 11, 13],
        "has_sujets": True,
        "name": "Fusion de trous noirs GW150914",
        "description": "Première détection directe d'ondes gravitationnelles. "
                       "Coalescence de deux trous noirs stellaires (~36 + ~30 M☉ → ~63 M☉ + "
                       "3 M☉c² rayonnés). Détection par LIGO Hanford et Livingston.",
        "occurred_at": {"iso": "-1305000000",   # ~1.3 Gyr avant 2015
                        "precision_class": "hectomegaannee",
                        "precision_seconds": 1e8 * JULIAN_YEAR_S,
                        "uncertain": True,
                        "notes": "z = 0.09 ± 0.04 → ~1.3 Gyr lookback time avec H₀ Planck"},
        "observed_at": {"iso": "2015-09-14T09:50:45Z",
                        "precision_class": "milliseconde",
                        "precision_seconds": 1e-3,
                        "uncertain": False,
                        "notes": "Délai inter-détecteurs LIGO H1/L1 : 6.9 ms"},
        "light_travel_time_s": 1.3e9 * JULIAN_YEAR_S,
        "coords": {
            "frame": "ICRS",
            "ra_deg": 112.5, "dec_deg": -70.0,   # localisation très imprécise
            "distance_m": 410 * 1e6 * PARSEC_M,
            "distance_precision_class": "hectomegaparsec",
            "distance_precision_meters": 160 * 1e6 * PARSEC_M,
            "distance_method": "GW_standard_siren",
            "epoch": "J2015.7",
            "pm_ra_mas_yr": None, "pm_dec_mas_yr": None,
            "radial_velocity_km_s": None, "parallax_mas": None, "redshift_z": 0.09,
        },
        "sujets": ["gw150914_bh1", "gw150914_bh2"],
        "causes": [],
        "effets": [],
        "notes": "Précision temporelle (ms) extrême malgré une localisation angulaire "
                 "imprécise (~600 deg² en aire crédible). Inverse exact du couple "
                 "précision SN 1987A (s + arcsec).",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Validation
# ══════════════════════════════════════════════════════════════════════════════

def _validate() -> list[str]:
    errors = []

    # 1. Précisions strictement décroissantes
    for label, seq in [("GEO_COSMIQUE", PRECISIONS_COSMIQUES_GEO),
                       ("TEMPS_COSMIQUE", PRECISIONS_COSMIQUES_TEMPS)]:
        for i in range(len(seq) - 1):
            if seq[i][1] <= seq[i + 1][1]:
                errors.append(f"{label}: ordre violé entre {seq[i][0]} et {seq[i+1][0]}")

    # 2. Cohérence atomique des objets célestes (tous = 2002)
    obj_ids = {o["id"] for o in OBJETS}
    for o in OBJETS:
        prod = reduce(mul, o["nipada_atoms"])
        if prod != o["nipada_type"]:
            errors.append(f"OBJETS/{o['id']}: ∏{o['nipada_atoms']}={prod} ≠ {o['nipada_type']}")
        if o["coords"]["frame"] not in FRAMES:
            errors.append(f"OBJETS/{o['id']}: frame '{o['coords']['frame']}' inconnu")

    # 3. Événements astronomiques
    evt_ids = {e["id"] for e in EVENEMENTS_ASTRO}
    for e in EVENEMENTS_ASTRO:
        prod = reduce(mul, e["nipada_atoms"])
        if prod != e["nipada_type"]:
            errors.append(f"EVT/{e['id']}: ∏{e['nipada_atoms']}={prod} ≠ {e['nipada_type']}")
        if e["has_sujets"] and 11 not in e["nipada_atoms"]:
            errors.append(f"EVT/{e['id']}: has_sujets=True mais SUJET(11) absent")
        if not e["has_sujets"] and 11 in e["nipada_atoms"]:
            errors.append(f"EVT/{e['id']}: has_sujets=False mais SUJET(11) présent")
        # sujets référencent des objets connus
        for s in e["sujets"]:
            if s not in obj_ids:
                errors.append(f"EVT/{e['id']}.sujets: '{s}' inconnu")
        # frame valide
        if e["coords"]["frame"] not in FRAMES:
            errors.append(f"EVT/{e['id']}: frame '{e['coords']['frame']}' inconnu")
        # causes/effets référencent des événements existants
        for ref in e["causes"]:
            if ref not in evt_ids:
                errors.append(f"EVT/{e['id']}.causes: '{ref}' inconnu")
        for ref in e["effets"]:
            if ref not in evt_ids:
                errors.append(f"EVT/{e['id']}.effets: '{ref}' inconnu")
        # cohérence light_travel_time (si renseigné)
        if e["light_travel_time_s"] is not None and e["light_travel_time_s"] < 0:
            errors.append(f"EVT/{e['id']}: light_travel_time_s négatif")

    # 4. Symétrie graphe causal (causes ↔ effets)
    by_id = {e["id"]: e for e in EVENEMENTS_ASTRO}
    for e in EVENEMENTS_ASTRO:
        for c in e["causes"]:
            if e["id"] not in by_id[c]["effets"]:
                errors.append(f"EVT/{c}.effets manque '{e['id']}' (asymétrie)")
        for f_id in e["effets"]:
            if e["id"] not in by_id[f_id]["causes"]:
                errors.append(f"EVT/{f_id}.causes manque '{e['id']}' (asymétrie)")

    return errors


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    W = 78
    print("═" * W)
    print("  §104 — Fondations astronomiques : précisions cosmiques + référentiels")
    print("═" * W)
    print(f"\n  Précisions GEO cosmiques   : {len(PRECISIONS_COSMIQUES_GEO):2d} classes")
    print(f"    {PRECISIONS_COSMIQUES_GEO[0][0]:<25s} = {PRECISIONS_COSMIQUES_GEO[0][1]:.3e} m")
    print(f"    {PRECISIONS_COSMIQUES_GEO[-1][0]:<25s} = {PRECISIONS_COSMIQUES_GEO[-1][1]:.3e} m")
    print(f"  Précisions TEMPS cosmiques : {len(PRECISIONS_COSMIQUES_TEMPS):2d} classes")
    print(f"    {PRECISIONS_COSMIQUES_TEMPS[0][0]:<25s} = {PRECISIONS_COSMIQUES_TEMPS[0][1]:.3e} s")
    print(f"    {PRECISIONS_COSMIQUES_TEMPS[-1][0]:<25s} = {PRECISIONS_COSMIQUES_TEMPS[-1][1]:.3e} s")
    print(f"  Référentiels célestes      : {len(FRAMES):2d}")
    print(f"  Objets célestes            : {len(OBJETS):2d}")
    print(f"  Événements astronomiques   : {len(EVENEMENTS_ASTRO):2d}")

    print("\n  ── Validation ──")
    errors = _validate()
    if errors:
        for e in errors:
            print(f"    ✗ {e}")
        raise SystemExit(1)
    print("  ✓ précisions cosmiques (geo + temps) strictement décroissantes")
    print("  ✓ objets célestes : nipada_type=2002 cohérent, frames valides")
    print("  ✓ événements : ∏atoms == type, has_sujets ↔ SUJET(11)")
    print("  ✓ événements : sujets/causes/effets référencent des entités existantes")
    print("  ✓ light_travel_time_s ≥ 0")
    print("  ✓ graphe causal symétrique (causes ↔ effets)")

    print("\n  ── Discordance temporelle radicale (occurred_at vs observed_at) ──")
    for e in EVENEMENTS_ASTRO:
        if e["light_travel_time_s"] and e["light_travel_time_s"] > 0:
            ltt_yr = e["light_travel_time_s"] / JULIAN_YEAR_S
            print(f"    {e['id']:<32s} Δt = {ltt_yr:.3e} ans-lumière")

    ASTRO_DIR.mkdir(parents=True, exist_ok=True)
    out_prec = ASTRO_DIR / "precisions_cosmiques.json"
    out_obj = ASTRO_DIR / "objets_celestes.json"
    out_evt = ASTRO_DIR / "evenements_astronomiques.json"

    with out_prec.open("w", encoding="utf-8") as f:
        json.dump({
            "version": "§104",
            "constants": {
                "PARSEC_M": PARSEC_M, "LIGHT_YEAR_M": LIGHT_YEAR_M,
                "ASTRONOMICAL_UNIT_M": ASTRONOMICAL_UNIT_M,
                "SOLAR_RADIUS_M": SOLAR_RADIUS_M, "EARTH_RADIUS_M": EARTH_RADIUS_M,
                "HUBBLE_RADIUS_M": HUBBLE_RADIUS_M,
                "JULIAN_YEAR_S": JULIAN_YEAR_S, "AGE_UNIVERSE_S": AGE_UNIVERSE_S,
            },
            "geo":   {"index": GEO_INDEX,
                      "ordered": [list(t) for t in PRECISIONS_COSMIQUES_GEO]},
            "temps": {"index": TEMPS_INDEX,
                      "ordered": [list(t) for t in PRECISIONS_COSMIQUES_TEMPS]},
            "frames": FRAMES,
        }, f, ensure_ascii=False, indent=2)
    with out_obj.open("w", encoding="utf-8") as f:
        json.dump({"version": "§104", "objets": OBJETS},
                  f, ensure_ascii=False, indent=2)
    with out_evt.open("w", encoding="utf-8") as f:
        json.dump({"version": "§104", "evenements": EVENEMENTS_ASTRO},
                  f, ensure_ascii=False, indent=2)

    print(f"\n  Sortie :")
    for p in (out_prec, out_obj, out_evt):
        print(f"    {p.relative_to(REPO_ROOT)}")
    print("═" * W)


if __name__ == "__main__":
    main()
