#!/usr/bin/env python3
"""
§86→§94 — Lacunes nipada : corpus étendu multi-genre + matrice de confusion
===========================================================================
Version §94 : corpus massivement étendu (FR/EN 20 + DE/ES/ZH/IT/PT 10)
  §87 — narration : [13, 78, 273]  TEMPS+DEVENIR+SUCCESSION
  §88 — question  : [143, 165, 11] INTERROGATION(11×13)+JUGEMENT+SUJET
  §89 — introspection : [2310, 22, 26] +ÉVOLUTION(2×13)
  §91 — pré-filtre syntaxique QUESTION(?/wh) +0.12 + INTROSPECTION(1re pers.)
  §92 — copule définitoire (est la/le/l'/ce qui) → DÉFINITION +0.10
         introspection 1p sans "?" → +0.12 ; avec "?" → +0.02
  §93 — bonus définition +0.14 + c'est+inf (FR) + to+V+is+to+V (EN)
  §94 — corpus 245→(630+) ; +IT +PT ; 14→30 adversariaux ;
         copule IT/PT (è/é + article), wh-mot IT/PT, 1re pers. io/eu

Corpus : 20 phrases × 7 types × FR/EN  +  10 × 7 types × DE/ES/ZH/IT/PT
         = 630 phrases de test + 30 cas adversariaux (15 FR + 15 EN testés)

Output → research/nipada/falsification/nipada_lacunes_report.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.core.nipada_v6 import NipadaV6Synthesizer, MODES_V6  # noqa: E402

OUTPUT = REPO_ROOT / "research" / "nipada" / "falsification" / "nipada_lacunes_report.json"


# ── NumPy 2.0 JSON helpers ────────────────────────────────────────────────────
class _NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.bool_): return bool(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super().default(obj)


def _to_native(obj):
    if isinstance(obj, dict): return {k: _to_native(v) for k, v in obj.items()}
    if isinstance(obj, list): return [_to_native(v) for v in obj]
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, np.floating): return float(obj)
    if isinstance(obj, np.bool_): return bool(obj)
    return obj


# ── Modes V6 (§87/§88/§89) + langues §94 (IT/PT) ─────────────────────────────
MODES = MODES_V6
MODE_NAMES = list(MODES.keys())
LANGS = ["fr", "en", "de", "es", "zh", "it", "pt"]

CORPUS: dict[str, dict[str, list[str]]] = {'description': {'fr': ["L'eau est une molécule composée de deux atomes d'hydrogène liés à un atome "
                        "d'oxygène.",
                        "Un arbre se distingue d'un arbuste par un tronc unique qui s'élève à plus d'un "
                        'mètre.',
                        "La lumière visible est un rayonnement électromagnétique de longueur d'onde entre "
                        '380 et 780 nm.',
                        "Un prédateur est un organisme qui capture et ingère d'autres organismes pour se "
                        'nourrir.',
                        "Le cerveau humain est un organe d'environ 1,3 kg constitué d'environ 86 milliards "
                        'de neurones.',
                        'Un triangle équilatéral possède trois côtés égaux et trois angles de 60 degrés '
                        'chacun.',
                        "L'ADN est une macromolécule en double hélice dont les brins portent les "
                        'instructions génétiques.',
                        'Paris est traversée par la Seine et divisée en vingt arrondissements numérotés en '
                        'spirale.',
                        "Un algorithme est une séquence finie d'opérations élémentaires résolvant un "
                        'problème donné.',
                        "La gravitation attire les masses l'une vers l'autre en proportion de leur produit.",
                        'La Tour Eiffel mesure 330 mètres de haut et pèse environ 10 100 tonnes au total.',
                        'Le cœur humain bat en moyenne 70 fois par minute et pompe près de 5 litres de sang.',
                        'Un volcan est une ouverture dans la croûte terrestre par laquelle le magma remonte '
                        'en surface.',
                        'Un processeur contient des milliards de transistors gravés sur une plaquette de '
                        'silicium.',
                        'Le désert du Sahara couvre neuf millions de kilomètres carrés sur onze pays '
                        'africains.',
                        'Une cellule eucaryote contient un noyau délimité par une membrane et divers '
                        'organites.',
                        'Le chat domestique possède trente-deux muscles dans chaque oreille, orientables '
                        'indépendamment.',
                        "La fourmi ouvrière porte jusqu'à cinquante fois son propre poids sans difficulté "
                        'apparente.',
                        'Les anneaux de Saturne sont composés de milliards de fragments de glace et de '
                        'roche.',
                        'Le boulanger pétrit la pâte, la laisse lever, puis la cuit à haute température dans '
                        'un four.'],
                 'en': ['Water is a molecule composed of two hydrogen atoms covalently bonded to one oxygen '
                        'atom.',
                        'A tree differs from a shrub by having a single trunk rising more than one meter '
                        'above ground.',
                        'Visible light is electromagnetic radiation with wavelengths ranging from 380 to 780 '
                        'nanometers.',
                        'A predator is an organism that captures and consumes other organisms for '
                        'sustenance.',
                        'The human brain weighs about 1.3 kg and contains approximately 86 billion neurons.',
                        'An equilateral triangle has three equal sides and three angles of 60 degrees each.',
                        'DNA is a double-helix macromolecule whose strands carry the genetic instructions '
                        'for living organisms.',
                        'Paris is divided into twenty arrondissements arranged in a spiral pattern.',
                        'An algorithm is a finite sequence of elementary operations designed to solve a '
                        'specific problem.',
                        'Gravity attracts masses toward each other in proportion to their product.',
                        'The Eiffel Tower stands 330 meters tall and weighs approximately 10,100 tonnes in '
                        'total.',
                        'The human heart beats on average 70 times per minute and pumps nearly 5 litres of '
                        'blood.',
                        "A volcano is an opening in the Earth's crust through which magma rises to the "
                        'surface.',
                        'A processor contains billions of transistors etched onto a wafer of silicon.',
                        'The Sahara desert covers nine million square kilometers across eleven African '
                        'countries.',
                        'A eukaryotic cell contains a nucleus bounded by a membrane and various organelles.',
                        'The domestic cat has thirty-two muscles in each ear, each movable independently.',
                        'A worker ant can carry up to fifty times its own body weight without apparent '
                        'difficulty.',
                        "Saturn's rings are composed of billions of ice and rock fragments orbiting the "
                        'planet.',
                        'The baker kneads the dough, lets it rise, then bakes it at high temperature in an '
                        'oven.'],
                 'de': ['Wasser ist ein Molekül aus zwei Wasserstoffatomen, die kovalent an ein '
                        'Sauerstoffatom gebunden sind.',
                        'Ein Baum unterscheidet sich von einem Strauch durch einen Stamm, der mehr als einen '
                        'Meter aufragt.',
                        'Sichtbares Licht ist elektromagnetische Strahlung mit Wellenlängen zwischen 380 und '
                        '780 Nanometern.',
                        'Ein Raubtier ist ein Organismus, der andere Organismen einfängt und frisst, um sich '
                        'zu ernähren.',
                        'Das menschliche Gehirn ist ein Organ von etwa 1,3 kg mit rund 86 Milliarden '
                        'Neuronen.',
                        'Der Eiffelturm ist 330 Meter hoch und wiegt insgesamt etwa 10 100 Tonnen.',
                        'Das menschliche Herz schlägt im Durchschnitt 70 Mal pro Minute und pumpt fast 5 '
                        'Liter Blut.',
                        'Ein Vulkan ist eine Öffnung in der Erdkruste, durch die Magma an die Oberfläche '
                        'steigt.',
                        'Ein Prozessor enthält Milliarden von Transistoren, die auf einen Siliziumwafer '
                        'geätzt sind.',
                        'Die Sahara bedeckt neun Millionen Quadratkilometer und erstreckt sich über elf '
                        'afrikanische Länder.'],
                 'es': ['El agua es una molécula formada por dos átomos de hidrógeno enlazados a un átomo de '
                        'oxígeno.',
                        'Un árbol se distingue de un arbusto por poseer un tronco único que se eleva más de '
                        'un metro.',
                        'La luz visible es una radiación electromagnética con longitudes de onda entre 380 y '
                        '780 nm.',
                        'Un depredador es un organismo que captura y consume a otros organismos para '
                        'alimentarse.',
                        'El cerebro humano pesa unos 1,3 kg y está formado por aproximadamente 86 000 '
                        'millones de neuronas.',
                        'La Torre Eiffel mide 330 metros de altura y pesa aproximadamente 10 100 toneladas '
                        'en total.',
                        'El corazón humano late en promedio 70 veces por minuto y bombea casi 5 litros de '
                        'sangre.',
                        'Un volcán es una abertura en la corteza terrestre por la que el magma asciende a la '
                        'superficie.',
                        'Un procesador contiene miles de millones de transistores grabados sobre una oblea '
                        'de silicio.',
                        'El desierto del Sahara cubre nueve millones de kilómetros cuadrados en once países '
                        'africanos.'],
                 'zh': ['水是由两个氢原子与一个氧原子通过共价键连接而成的分子。',
                        '乔木与灌木的区别在于前者拥有一根高于一米的单一主干。',
                        '可见光是波长在380至780纳米之间的电磁辐射。',
                        '捕食者是捕获并消费其他生物以维持生存的生物体。',
                        '人类大脑约重1.3公斤，由约860亿个神经元组成。',
                        '埃菲尔铁塔高330米，总重约10100吨。',
                        '人类心脏每分钟平均跳动70次，泵送近5升血液。',
                        '火山是地壳上让岩浆上升到地表的开口。',
                        '处理器在硅晶圆上蚀刻有数十亿个晶体管。',
                        '撒哈拉沙漠覆盖九百万平方公里，横跨十一个非洲国家。'],
                 'it': ["L'acqua è una molecola composta da due atomi di idrogeno legati a un atomo di "
                        'ossigeno.',
                        'Un albero si distingue da un arbusto per un tronco unico che si eleva oltre un '
                        'metro.',
                        "La luce visibile è una radiazione elettromagnetica con lunghezza d'onda tra 380 e "
                        '780 nanometri.',
                        'Il cervello umano pesa circa 1,3 kg e contiene circa 86 miliardi di neuroni.',
                        'La Torre Eiffel è alta 330 metri e pesa complessivamente circa 10 100 tonnellate.',
                        'Il cuore umano batte in media 70 volte al minuto e pompa quasi 5 litri di sangue.',
                        "Un vulcano è un'apertura nella crosta terrestre attraverso la quale il magma risale "
                        'in superficie.',
                        'Un processore contiene miliardi di transistor incisi su una piastrina di silicio.',
                        'Il deserto del Sahara copre nove milioni di chilometri quadrati in undici paesi '
                        'africani.',
                        'Una cellula eucariote contiene un nucleo delimitato da una membrana e vari '
                        'organelli.'],
                 'pt': ['A água é uma molécula composta por dois átomos de hidrogénio ligados a um átomo de '
                        'oxigénio.',
                        'Uma árvore distingue-se de um arbusto por ter um tronco único que se eleva mais de '
                        'um metro.',
                        'A luz visível é uma radiação electromagnética com comprimentos de onda entre 380 e '
                        '780 nanómetros.',
                        'O cérebro humano pesa cerca de 1,3 kg e contém aproximadamente 86 mil milhões de '
                        'neurónios.',
                        'A Torre Eiffel tem 330 metros de altura e pesa cerca de 10 100 toneladas no total.',
                        'O coração humano bate em média 70 vezes por minuto e bombeia quase 5 litros de '
                        'sangue.',
                        'Um vulcão é uma abertura na crosta terrestre através da qual o magma sobe à '
                        'superfície.',
                        'Um processador contém milhares de milhões de transístores gravados numa pastilha de '
                        'silício.',
                        'O deserto do Sahara cobre nove milhões de quilómetros quadrados em onze países '
                        'africanos.',
                        'Uma célula eucariota contém um núcleo delimitado por uma membrana e vários '
                        'organelos.']},
 'définition': {'fr': ['La liberté est la faculté de se donner sa propre loi sans la subir comme une '
                       'contrainte extérieure.',
                       'La justice est la disposition constante et perpétuelle à rendre à chacun ce qui lui '
                       'revient.',
                       "L'amour est la reconnaissance de l'autre comme une fin en soi, jamais réductible à "
                       'un moyen.',
                       "Le temps est la mesure du mouvement selon l'avant et l'après, selon la formulation "
                       "d'Aristote.",
                       "La conscience est la présence d'un sujet à lui-même dans l'acte même de connaître ou "
                       'de percevoir.',
                       'Une hypothèse est une proposition provisoire posée pour rendre compte de faits '
                       'observés.',
                       'La beauté est ce qui provoque un plaisir immédiat, universel et désintéressé dans la '
                       'contemplation.',
                       "Le droit est l'ensemble des règles qui organisent la vie en société, garanties par "
                       'la contrainte publique.',
                       "L'identité personnelle est ce qui fait qu'un être reste lui-même à travers le "
                       'changement du temps.',
                       "La vérité est l'adéquation entre ce qu'un énoncé affirme et l'état de fait qu'il "
                       'prétend décrire.',
                       "Le courage est la fermeté de l'âme face à ce qui menace, maintenue malgré la peur "
                       'ressentie.',
                       'La sagesse est la capacité de discerner le bien praticable dans les circonstances '
                       'concrètes.',
                       'Un nombre premier est un entier naturel strictement supérieur à un, divisible '
                       'seulement par un et lui-même.',
                       'La démocratie est le régime dans lequel le pouvoir politique procède du peuple tout '
                       'entier.',
                       "Un théorème est une proposition qu'on démontre à partir d'axiomes par une chaîne "
                       'déductive valide.',
                       "L'amitié est la relation désintéressée entre deux êtres qui se veulent mutuellement "
                       'du bien.',
                       "La mémoire est la faculté par laquelle l'esprit conserve et restitue ce qui a été "
                       'vécu.',
                       "Le souverain est celui qui détient le pouvoir de décider dans l'état d'exception.",
                       "Une contradiction est la coprésence simultanée d'une affirmation et de sa négation "
                       'sur le même objet.',
                       "L'éducation est le processus par lequel une société transmet aux nouvelles "
                       'générations ses savoirs et ses valeurs.'],
                'en': ["Freedom is the capacity to give oneself one's own law without experiencing it as "
                       'external constraint.',
                       'Justice is the constant and perpetual disposition to give each person what is due to '
                       'them.',
                       'Love is the recognition of another as an end in themselves, never reducible to a '
                       'mere means.',
                       'Time is the measure of movement according to before and after, as Aristotle '
                       'formulated it.',
                       'Consciousness is the presence of a subject to itself in the very act of knowing or '
                       'perceiving.',
                       'A hypothesis is a provisional proposition advanced to account for observed facts.',
                       'Beauty is what provokes an immediate, universal and disinterested pleasure in '
                       'contemplation.',
                       'Law is the ensemble of rules organizing social life, guaranteed by public coercion.',
                       'Personal identity is what makes a being remain itself through the changes of time.',
                       'Truth is the correspondence between what a proposition asserts and the state of '
                       'affairs it describes.',
                       'Courage is the firmness of the soul in the face of what threatens, maintained '
                       'despite felt fear.',
                       'Wisdom is the capacity to discern the practicable good within concrete '
                       'circumstances.',
                       'A prime number is the natural integer strictly greater than one, divisible only by '
                       'one and itself.',
                       'Democracy is the regime in which political power proceeds from the people as a '
                       'whole.',
                       'A theorem is the proposition that is demonstrated from axioms through a valid '
                       'deductive chain.',
                       'Friendship is the disinterested relation between two beings who mutually will each '
                       "other's good.",
                       'Memory is the faculty by which the mind preserves and restores what has been lived '
                       'through.',
                       'The sovereign is the one who holds the power to decide in the state of exception.',
                       'A contradiction is the simultaneous co-presence of an assertion and its negation '
                       'about the same object.',
                       'Education is the process by which a society transmits to new generations its '
                       'knowledge and values.'],
                'de': ['Freiheit ist die Fähigkeit, sich selbst ein Gesetz zu geben, ohne es als äußeren '
                       'Zwang zu erleben.',
                       'Gerechtigkeit ist die beständige Bereitschaft, jedem das zu geben, was ihm zusteht.',
                       'Liebe ist die Anerkennung des anderen als Zweck an sich selbst, nie als bloßes '
                       'Mittel.',
                       'Zeit ist das Maß der Bewegung nach Vorher und Nachher, wie Aristoteles es formuliert '
                       'hat.',
                       'Bewusstsein ist die Anwesenheit eines Subjekts bei sich selbst im Akt des Erkennens.',
                       'Mut ist die Festigkeit der Seele angesichts dessen, was bedroht, trotz der '
                       'empfundenen Angst.',
                       'Weisheit ist die Fähigkeit, das praktikable Gute in konkreten Umständen zu erkennen.',
                       'Eine Primzahl ist die natürliche Zahl, die größer als eins und nur durch eins und '
                       'sich selbst teilbar ist.',
                       'Demokratie ist das Regime, in dem die politische Macht vom ganzen Volk ausgeht.',
                       'Freundschaft ist die uneigennützige Beziehung zwischen zwei Wesen, die einander '
                       'gegenseitig Gutes wollen.'],
                'es': ['La libertad es la facultad de darse a uno mismo su propia ley sin experimentarla '
                       'como coacción externa.',
                       'La justicia es la disposición constante y perpetua de dar a cada uno lo que le '
                       'corresponde.',
                       'El amor es el reconocimiento del otro como fin en sí mismo, nunca reducible a un '
                       'simple medio.',
                       'El tiempo es la medida del movimiento según el antes y el después, según '
                       'Aristóteles.',
                       'La conciencia es la presencia de un sujeto a sí mismo en el acto de conocer o '
                       'percibir.',
                       'El coraje es la firmeza del alma ante lo que amenaza, mantenida a pesar del miedo '
                       'sentido.',
                       'La sabiduría es la capacidad de discernir el bien practicable en las circunstancias '
                       'concretas.',
                       'Un número primo es el entero natural estrictamente mayor que uno, divisible sólo por '
                       'uno y por sí mismo.',
                       'La democracia es el régimen en el que el poder político procede del pueblo en su '
                       'totalidad.',
                       'La amistad es la relación desinteresada entre dos seres que se desean mutuamente el '
                       'bien.'],
                'zh': ['自由是在不将其体验为外部强制的情况下，自我立法的能力。',
                       '正义是持续不断地给予每个人其应得之物的意愿。',
                       '爱是将他人视为目的本身而非仅仅作为手段的承认。',
                       '时间是按照前后顺序衡量运动的尺度，正如亚里士多德所表述的那样。',
                       '意识是主体在认识或感知的行为本身中向自身的在场。',
                       '勇气是指面对威胁时，尽管感到恐惧仍保持灵魂坚定的品质。',
                       '智慧是指在具体情境中辨别可行之善的能力。',
                       '素数指的是大于一且只能被一和自身整除的自然数。',
                       '民主是政治权力源自全体人民的政治制度。',
                       '友谊是两个相互希望对方好的存在者之间无私的关系。'],
                'it': ['La libertà è la facoltà di darsi la propria legge senza subirla come costrizione '
                       'esterna.',
                       'La giustizia è la disposizione costante e perpetua a dare a ciascuno ciò che gli '
                       'spetta.',
                       "L'amore è il riconoscimento dell'altro come fine in sé, mai riducibile a un mero "
                       'mezzo.',
                       'Il tempo è la misura del movimento secondo il prima e il dopo, come Aristotele ha '
                       'formulato.',
                       "La coscienza è la presenza di un soggetto a se stesso nell'atto stesso di conoscere.",
                       "Il coraggio è la fermezza dell'animo di fronte a ciò che minaccia, mantenuta "
                       'nonostante la paura.',
                       'La saggezza è la capacità di discernere il bene praticabile nelle circostanze '
                       'concrete.',
                       "Un numero primo è l'intero naturale maggiore di uno divisibile solo per uno e per se "
                       'stesso.',
                       'La democrazia è il regime in cui il potere politico procede dal popolo nella sua '
                       'totalità.',
                       "L'amicizia è la relazione disinteressata tra due esseri che si vogliono "
                       'reciprocamente bene.'],
                'pt': ['A liberdade é a faculdade de se dar a si mesmo a própria lei sem a sofrer como '
                       'coacção externa.',
                       'A justiça é a disposição constante e perpétua de dar a cada um o que lhe pertence.',
                       'O amor é o reconhecimento do outro como fim em si mesmo, nunca redutível a um mero '
                       'meio.',
                       'O tempo é a medida do movimento segundo o antes e o depois, conforme Aristóteles '
                       'formulou.',
                       'A consciência é a presença de um sujeito a si mesmo no acto mesmo de conhecer ou '
                       'perceber.',
                       'A coragem é a firmeza da alma perante o que ameaça, mantida apesar do medo sentido.',
                       'A sabedoria é a capacidade de discernir o bem praticável nas circunstâncias '
                       'concretas.',
                       'Um número primo é o inteiro natural estritamente maior que um, divisível apenas por '
                       'um e por si mesmo.',
                       'A democracia é o regime em que o poder político procede do povo na sua totalidade.',
                       'A amizade é a relação desinteressada entre dois seres que mutuamente se querem '
                       'bem.']},
 'proclamation': {'fr': ["Tout être humain possède une dignité inaliénable qu'aucune condition ne peut lui "
                         'retirer.',
                         'La liberté de conscience est un droit fondamental que nul pouvoir ne peut '
                         'légitimement révoquer.',
                         "Nul ne peut être réduit au rang d'instrument sans que sa propre fin soit ignorée.",
                         "L'égalité des droits entre tous les humains est une norme dont la validité ne "
                         'souffre aucune exception.',
                         "Tout sujet a le droit de défendre sa liberté contre quiconque cherche à l'en "
                         'priver par la force.',
                         "La protection de la vie est une obligation qui s'impose à toute organisation "
                         'politique légitime.',
                         "Aucune loi ne peut être juste si elle n'est pas fondée sur le respect "
                         'inconditionnel de la personne.',
                         'La torture est inconditionnellement interdite, quelles que soient les '
                         'circonstances invoquées.',
                         "Les droits fondamentaux s'appliquent à chaque personne en raison de son humanité, "
                         'non de sa citoyenneté.',
                         "La liberté d'expression ne peut être limitée que pour protéger les droits "
                         "d'autrui, jamais pour protéger le pouvoir.",
                         "Nul ne peut être arbitrairement privé de sa liberté ni détenu sans contrôle d'une "
                         'autorité judiciaire.',
                         'Le présent traité entre en vigueur au jour de sa ratification par les parties '
                         'contractantes.',
                         "L'accès à l'éducation élémentaire est garanti à tout enfant sans distinction "
                         "d'origine ou de fortune.",
                         'La propriété privée est protégée par la loi et ne peut être aliénée que pour cause '
                         "d'utilité publique.",
                         "Toute personne accusée d'un crime est présumée innocente jusqu'à ce que sa "
                         'culpabilité soit établie.',
                         "L'esclavage et la traite des êtres humains sont interdits sous toutes leurs formes "
                         'en tout lieu.',
                         'Le secret de la correspondance est garanti à toute personne résidant sur le '
                         'territoire national.',
                         'Tous les citoyens sont égaux devant la loi et ont droit à une égale protection des '
                         'tribunaux.',
                         'Aucune discrimination fondée sur la race, le sexe ou la religion ne peut être '
                         "tolérée dans l'accès à l'emploi.",
                         'Le droit de réunion pacifique est reconnu à tous dans les limites fixées par la '
                         'loi démocratique.'],
                  'en': ['Every human being possesses an inalienable dignity that no condition can strip '
                         'away.',
                         'Freedom of conscience is a fundamental right that no authority can legitimately '
                         'revoke.',
                         'No person can be reduced to an instrument without their own ends being '
                         'disregarded.',
                         'The equality of rights among all human beings is a norm that admits of no '
                         'exception.',
                         'Every subject has the right to defend their freedom against anyone who seeks to '
                         'deprive them of it.',
                         'The protection of life is an obligation binding every political organization '
                         'claiming legitimacy.',
                         'No law can be just if it is not grounded in unconditional respect for the person.',
                         'Torture is unconditionally prohibited, regardless of the circumstances invoked to '
                         'justify it.',
                         'Fundamental rights apply to each person by virtue of their humanity, not their '
                         'citizenship.',
                         'Freedom of expression may only be limited to protect the rights of others, never '
                         'to protect power.',
                         'No one may be arbitrarily deprived of liberty or detained without review by a '
                         'judicial authority.',
                         'The present treaty enters into force on the day of its ratification by the '
                         'contracting parties.',
                         'Access to elementary education is guaranteed to every child regardless of origin '
                         'or wealth.',
                         'Private property is protected by law and may only be alienated for reasons of '
                         'public utility.',
                         'Any person accused of a crime is presumed innocent until guilt has been duly '
                         'established.',
                         'Slavery and trafficking in human beings are forbidden in all their forms in all '
                         'places.',
                         'The privacy of correspondence is guaranteed to every person residing on national '
                         'territory.',
                         'All citizens are equal before the law and entitled to equal protection by the '
                         'courts.',
                         'No discrimination based on race, sex or religion may be tolerated in access to '
                         'employment.',
                         'The right of peaceful assembly is recognized for all within the limits set by '
                         'democratic law.'],
                  'de': ['Jeder Mensch besitzt eine unveräußerliche Würde, die ihm durch keine Bedingung '
                         'entzogen werden kann.',
                         'Gewissensfreiheit ist ein Grundrecht, das keine Macht rechtmäßig widerrufen kann.',
                         'Niemand kann auf den Rang eines Instruments reduziert werden, ohne dass sein Zweck '
                         'missachtet wird.',
                         'Die Gleichheit der Rechte aller Menschen ist eine Norm, die keine Ausnahme duldet.',
                         'Jedes Subjekt hat das Recht, seine Freiheit gegen jeden zu verteidigen, der '
                         'versucht, sie zu nehmen.',
                         'Niemand darf willkürlich seiner Freiheit beraubt oder ohne richterliche Kontrolle '
                         'festgehalten werden.',
                         'Der Zugang zur Grundbildung ist jedem Kind unabhängig von Herkunft oder Vermögen '
                         'garantiert.',
                         'Das Privateigentum ist durch Gesetz geschützt und darf nur aus Gründen des '
                         'Gemeinwohls enteignet werden.',
                         'Jede einer Straftat beschuldigte Person gilt als unschuldig, bis ihre Schuld '
                         'ordnungsgemäß festgestellt ist.',
                         'Sklaverei und Menschenhandel sind in allen Formen und an allen Orten verboten.'],
                  'es': ['Todo ser humano posee una dignidad inalienable que ninguna condición puede '
                         'arrebatarle.',
                         'La libertad de conciencia es un derecho fundamental que ningún poder puede '
                         'legítimamente revocar.',
                         'Nadie puede ser reducido a la condición de instrumento sin que se ignore su propio '
                         'fin.',
                         'La igualdad de derechos entre todos los seres humanos es una norma que no admite '
                         'excepción alguna.',
                         'Todo sujeto tiene el derecho de defender su libertad frente a quienes traten de '
                         'privársela.',
                         'Nadie podrá ser arbitrariamente privado de su libertad ni detenido sin control de '
                         'una autoridad judicial.',
                         'El acceso a la educación elemental está garantizado a todo niño sin distinción de '
                         'origen o fortuna.',
                         'La propiedad privada está protegida por la ley y sólo podrá ser enajenada por '
                         'causa de utilidad pública.',
                         'Toda persona acusada de un delito se presume inocente hasta que se establezca '
                         'debidamente su culpabilidad.',
                         'La esclavitud y la trata de seres humanos están prohibidas en todas sus formas y '
                         'en todo lugar.'],
                  'zh': ['每个人都拥有任何条件都无法剥夺的不可让渡的尊严。',
                         '良心自由是任何权力都不能合法地撤销的基本权利。',
                         '没有人可以被降格为工具，而其自身目的却被忽视。',
                         '所有人平等权利是一项不允许任何例外的规范。',
                         '每个主体都有权捍卫自己的自由，反对任何试图以武力剥夺其自由的人。',
                         '任何人不得被任意剥夺自由或在未经司法当局审查的情况下被拘留。',
                         '每一个儿童都享有接受基础教育的权利，不论其出身或财富如何。',
                         '私有财产受法律保护，仅在公共利益的理由下方得被征用。',
                         '任何被指控犯罪的人在其罪行被依法确立之前均推定为无罪。',
                         '奴隶制和人口贩卖在一切形式与一切地点均被禁止。'],
                  'it': ['Ogni essere umano possiede una dignità inalienabile che nessuna condizione può '
                         'togliergli.',
                         'La libertà di coscienza è un diritto fondamentale che nessun potere può '
                         'legittimamente revocare.',
                         'Nessuno può essere ridotto al rango di strumento senza che il suo proprio fine sia '
                         'ignorato.',
                         "L'uguaglianza dei diritti tra tutti gli esseri umani è una norma che non ammette "
                         'alcuna eccezione.',
                         'Ogni soggetto ha il diritto di difendere la propria libertà contro chiunque cerchi '
                         'di privargliene.',
                         'Nessuno può essere arbitrariamente privato della libertà o detenuto senza '
                         "controllo di un'autorità giudiziaria.",
                         "L'accesso all'istruzione elementare è garantito a ogni bambino senza distinzione "
                         'di origine o fortuna.',
                         'La proprietà privata è protetta dalla legge e può essere alienata solo per causa '
                         'di pubblica utilità.',
                         'Ogni persona accusata di un reato è presunta innocente fino a quando la '
                         'colpevolezza non sia stabilita.',
                         'La schiavitù e la tratta degli esseri umani sono vietate in tutte le loro forme e '
                         'in ogni luogo.'],
                  'pt': ['Todo ser humano possui uma dignidade inalienável que nenhuma condição lhe pode '
                         'retirar.',
                         'A liberdade de consciência é um direito fundamental que nenhum poder pode '
                         'legitimamente revogar.',
                         'Ninguém pode ser reduzido à condição de instrumento sem que o seu próprio fim seja '
                         'ignorado.',
                         'A igualdade de direitos entre todos os seres humanos é uma norma que não admite '
                         'excepção alguma.',
                         'Todo sujeito tem o direito de defender a sua liberdade contra quem procure '
                         'privá-lo dela.',
                         'Ninguém pode ser arbitrariamente privado da sua liberdade nem detido sem controlo '
                         'de uma autoridade judicial.',
                         'O acesso à educação elementar é garantido a toda criança sem distinção de origem '
                         'ou fortuna.',
                         'A propriedade privada é protegida pela lei e só pode ser alienada por causa de '
                         'utilidade pública.',
                         'Toda pessoa acusada de um crime é presumida inocente até que a sua culpa seja '
                         'devidamente estabelecida.',
                         'A escravatura e o tráfico de seres humanos são proibidos em todas as suas formas e '
                         'em todo lugar.']},
 'question': {'fr': ["Qu'est-ce qui distingue un acte moralement bon d'un acte simplement conforme à la "
                     'règle ?',
                     "Comment la conscience peut-elle être à la fois sujet et objet dans l'acte de réflexion "
                     '?',
                     'Existe-t-il des vérités que nul sujet fini ne pourra jamais atteindre par ses propres '
                     'moyens ?',
                     'Pourquoi y a-t-il quelque chose plutôt que rien, et à quel titre peut-on poser cette '
                     'question ?',
                     "Est-il possible de vouloir librement ce que l'on a été formé à désirer depuis "
                     "l'enfance ?",
                     "Quelle frontière sépare une obéissance légitime d'une soumission qui trahit sa propre "
                     'dignité ?',
                     "Comment distinguer une conviction sincère d'un préjugé si ancré qu'il se prend pour "
                     'une évidence ?',
                     'Un être peut-il vraiment choisir son identité, ou est-il toujours déjà déterminé par '
                     "ce qu'il est ?",
                     'Que reste-t-il de la liberté quand les conditions matérielles de son exercice ont été '
                     'supprimées ?',
                     "À quoi reconnaît-on qu'un argument est valide indépendamment de la vérité de ses "
                     'prémisses ?',
                     'À quelle heure part le train pour Lyon demain matin ?',
                     "Quel est le symptôme précoce d'une infection bactérienne des voies respiratoires ?",
                     'Comment corrige-t-on une erreur de segmentation dans un programme écrit en C ?',
                     "Pourquoi la lumière ralentit-elle lorsqu'elle traverse un milieu dense comme le verre "
                     '?',
                     'Quelles sont les étapes nécessaires pour obtenir un visa de travail en France ?',
                     "Combien d'années un chat domestique vit-il en moyenne en intérieur ?",
                     "Qui a peint le plafond de la chapelle Sixtine et en combien d'années ?",
                     'Où se trouve la bibliothèque la plus proche ouverte le dimanche ?',
                     'Quand commence la prochaine réunion du conseil municipal ?',
                     'Avez-vous déjà essayé de réparer vous-même un robinet qui fuit ?'],
              'en': ['What distinguishes a morally good act from one that merely conforms to the rule?',
                     'How can consciousness be both subject and object in the act of self-reflection?',
                     'Are there truths that no finite subject can ever reach through their own means?',
                     'Why is there something rather than nothing, and on what grounds can this question be '
                     'asked?',
                     'Is it possible to freely will what one has been formed to desire since childhood?',
                     "What separates legitimate obedience from submission that betrays one's own dignity?",
                     'How does one distinguish a sincere conviction from a prejudice that passes for '
                     'self-evidence?',
                     'Can a being truly choose their own identity, or are they always already determined by '
                     'what they are?',
                     'What remains of freedom when the material conditions for its exercise have been '
                     'eliminated?',
                     'How do we recognize that an argument is valid regardless of the truth of its premises?',
                     'What time does the train to Lyon leave tomorrow morning?',
                     'What is an early symptom of a bacterial respiratory infection?',
                     'How do you fix a segmentation fault in a C program?',
                     'Why does light slow down when it passes through a dense medium like glass?',
                     'What are the steps required to obtain a work visa for France?',
                     'How many years does a domestic cat live on average when kept indoors?',
                     'Who painted the ceiling of the Sistine Chapel and in how many years?',
                     'Where is the nearest library open on Sundays?',
                     'When does the next city council meeting begin?',
                     'Have you ever tried to repair a leaky faucet yourself?'],
              'de': ['Was unterscheidet eine moralisch gute Handlung von einer, die bloß der Regel '
                     'entspricht?',
                     'Wie kann Bewusstsein im Akt der Reflexion zugleich Subjekt und Objekt sein?',
                     'Gibt es Wahrheiten, die kein endliches Subjekt jemals mit eigenen Mitteln erreichen '
                     'kann?',
                     'Warum gibt es überhaupt etwas und nicht vielmehr nichts?',
                     'Ist es möglich, das frei zu wollen, wozu man seit der Kindheit geformt wurde?',
                     'Wann fährt morgen früh der Zug nach Lyon ab?',
                     'Was ist ein frühes Symptom einer bakteriellen Atemwegsinfektion?',
                     'Wie behebt man einen Segmentierungsfehler in einem C-Programm?',
                     'Warum verlangsamt sich Licht, wenn es ein dichtes Medium wie Glas durchquert?',
                     'Welche Schritte sind erforderlich, um ein Arbeitsvisum für Frankreich zu erhalten?'],
              'es': ['¿Qué distingue un acto moralmente bueno de uno que simplemente sigue la regla?',
                     '¿Cómo puede la conciencia ser a la vez sujeto y objeto en el acto de reflexión?',
                     '¿Existen verdades que ningún sujeto finito podrá alcanzar jamás por sus propios '
                     'medios?',
                     '¿Por qué hay algo en lugar de nada, y con qué fundamento puede plantearse esta '
                     'pregunta?',
                     '¿Es posible querer libremente lo que uno ha sido formado para desear desde la '
                     'infancia?',
                     '¿A qué hora sale el tren para Lyon mañana por la mañana?',
                     '¿Cuál es un síntoma temprano de una infección bacteriana de las vías respiratorias?',
                     '¿Cómo se corrige un error de segmentación en un programa escrito en C?',
                     '¿Por qué la luz se ralentiza cuando atraviesa un medio denso como el vidrio?',
                     '¿Cuáles son los pasos necesarios para obtener un visado de trabajo en Francia?'],
              'zh': ['道德上的善举与仅仅符合规则的行为有何区别？',
                     '意识如何能在反思行为中同时成为主体和客体？',
                     '是否存在任何有限主体永远无法通过自身手段达到的真理？',
                     '为何有某物而非虚无，又凭何能够提出这个问题？',
                     '一个人是否有可能自由地想要自幼被塑造成想要的东西？',
                     '明天早上去里昂的火车几点出发？',
                     '细菌性呼吸道感染的早期症状是什么？',
                     '如何修复C程序中的段错误？',
                     '为什么光通过玻璃这样的致密介质时会变慢？',
                     '获取法国工作签证需要哪些步骤？'],
              'it': ['Che cosa distingue un atto moralmente buono da uno che si limita a conformarsi alla '
                     'regola?',
                     "Come può la coscienza essere al tempo stesso soggetto e oggetto nell'atto di "
                     'riflessione?',
                     'Esistono verità che nessun soggetto finito potrà mai raggiungere con i propri mezzi?',
                     "Perché c'è qualcosa piuttosto che nulla, e a quale titolo si può porre questa domanda?",
                     'È possibile volere liberamente ciò che si è stati formati a desiderare fin '
                     "dall'infanzia?",
                     'A che ora parte il treno per Lione domani mattina?',
                     "Qual è un sintomo precoce di un'infezione batterica delle vie respiratorie?",
                     'Come si corregge un errore di segmentazione in un programma scritto in C?',
                     'Perché la luce rallenta quando attraversa un mezzo denso come il vetro?',
                     'Quali sono i passi necessari per ottenere un visto di lavoro per la Francia?'],
              'pt': ['O que distingue um acto moralmente bom de um que apenas se conforma à regra?',
                     'Como pode a consciência ser ao mesmo tempo sujeito e objecto no acto de reflexão?',
                     'Existem verdades que nenhum sujeito finito poderá jamais alcançar pelos próprios '
                     'meios?',
                     'Porque há algo em vez de nada, e com que fundamento se pode colocar esta pergunta?',
                     'É possível querer livremente o que se foi formado a desejar desde a infância?',
                     'A que horas parte o comboio para Lyon amanhã de manhã?',
                     'Qual é um sintoma precoce de uma infecção bacteriana das vias respiratórias?',
                     'Como se corrige um erro de segmentação num programa escrito em C?',
                     'Porque é que a luz abranda ao atravessar um meio denso como o vidro?',
                     'Quais são os passos necessários para obter um visto de trabalho em França?']},
 'ordre': {'fr': ["Formule la règle de ton action de sorte qu'elle puisse valoir comme loi universelle pour "
                  'tous.',
                  "N'utilise jamais autrui comme un simple moyen sans tenir compte de sa propre fin en soi.",
                  'Engage-toi dans la voie que tu as choisie et refuse de te laisser détourner par les '
                  'obstacles.',
                  'Agis de telle façon que les conséquences de tes actes soient compatibles avec la '
                  'permanence de la vie.',
                  'Prends en charge la responsabilité de ta propre direction sans la déléguer entièrement à '
                  'autrui.',
                  "Résiste à toute injonction qui te demanderait de trahir la fin que tu t'es librement "
                  'assignée.',
                  "Accomplis ce à quoi tu t'es engagé, même si les circonstances ont changé depuis ta "
                  'décision.',
                  "Oriente ton action selon une fin que tu pourrais défendre devant ceux qu'elle affecte.",
                  'Ne renonce pas à ta direction propre sous prétexte que la résistance te semble trop '
                  'difficile.',
                  'Maintiens le cap fixé en intégrant les résistances comme des épreuves de ta résolution.',
                  'Ferme la porte à clé avant de partir et dépose les clés chez la voisine.',
                  'Envoyez le rapport complet à la direction avant vendredi dix-sept heures.',
                  'Tournez à droite au deuxième feu puis continuez tout droit sur trois cents mètres.',
                  "Vérifie les trois points de contact avant de descendre l'échelle et ne saute jamais du "
                  'dernier barreau.',
                  "Retirez le couvercle, remplissez d'eau jusqu'au trait supérieur, puis refermez "
                  'hermétiquement.',
                  "Déconnectez l'appareil du secteur avant toute opération de nettoyage ou de démontage.",
                  'Place ta main droite sur la poignée et exerce une pression ferme vers le bas tout en '
                  'tirant.',
                  'Rangez vos affaires, éteignez les lumières et quittez la salle dans le calme.',
                  "Signe le document en présence du notaire et apporte deux pièces d'identité en original.",
                  "Ne touchez sous aucun prétexte aux fils dénudés avant que le courant n'ait été coupé."],
           'en': ['Formulate the rule of your action so that it could serve as a universal law for everyone.',
                  'Never treat another merely as a means without also considering their own end in itself.',
                  'Commit to the path you have chosen and refuse to be deflected by obstacles.',
                  'Act in such a way that the consequences of your actions are compatible with the '
                  'permanence of life.',
                  'Take responsibility for your own direction without delegating it entirely to others.',
                  'Resist any injunction that would ask you to betray the end you have freely assigned '
                  'yourself.',
                  'Fulfill what you have committed to, even if circumstances have changed since your '
                  'decision.',
                  'Orient your action according to an end you could defend before those it affects.',
                  'Do not abandon your own direction on the pretext that resistance seems too difficult.',
                  'Maintain the course you have set by integrating resistances as trials of your resolve.',
                  'Lock the door before leaving and drop the keys with the neighbor.',
                  "Send the complete report to management before five o'clock on Friday.",
                  'Turn right at the second traffic light then continue straight for three hundred meters.',
                  'Check all three points of contact before climbing down the ladder and never jump from the '
                  'last rung.',
                  'Remove the lid, fill with water up to the upper mark, then seal tightly.',
                  'Disconnect the device from the mains before any cleaning or disassembly operation.',
                  'Place your right hand on the handle and apply firm downward pressure while pulling.',
                  'Put away your belongings, turn off the lights and leave the room quietly.',
                  'Sign the document in the presence of the notary and bring two original identity '
                  'documents.',
                  'Under no circumstances touch the bare wires before the current has been cut off.'],
           'de': ['Formuliere die Maxime deiner Handlung so, dass sie als allgemeines Gesetz gelten könnte.',
                  'Benutze niemanden als bloßes Mittel, ohne seinen Zweck an sich selbst zu berücksichtigen.',
                  'Verpflichte dich zu dem Weg, den du gewählt hast, und lass dich nicht ablenken.',
                  'Handle so, dass die Folgen deiner Handlungen mit dem Fortbestand des Lebens vereinbar '
                  'sind.',
                  'Übernimm Verantwortung für deine eigene Richtung, ohne sie vollständig an andere '
                  'abzugeben.',
                  'Schließ die Tür ab, bevor du gehst, und gib die Schlüssel bei der Nachbarin ab.',
                  'Senden Sie den vollständigen Bericht vor Freitag siebzehn Uhr an die Geschäftsleitung.',
                  'An der zweiten Ampel rechts abbiegen und dann dreihundert Meter geradeaus weiterfahren.',
                  'Ziehen Sie den Netzstecker, bevor Sie das Gerät reinigen oder zerlegen.',
                  'Räumt eure Sachen auf, macht das Licht aus und verlasst den Raum in Ruhe.'],
           'es': ['Formula la máxima de tu acción de modo que pueda valer como ley universal para todos.',
                  'Nunca trates a nadie como un mero medio sin tener en cuenta su propio fin en sí mismo.',
                  'Comprométete con el camino que has elegido y niégate a dejarte desviar por los '
                  'obstáculos.',
                  'Actúa de tal manera que las consecuencias de tus actos sean compatibles con la '
                  'permanencia de la vida.',
                  'Hazte cargo de la responsabilidad de tu propia dirección sin delegarla completamente en '
                  'otros.',
                  'Cierra la puerta con llave antes de salir y deja las llaves en casa de la vecina.',
                  'Envíen el informe completo a la dirección antes de las cinco de la tarde del viernes.',
                  'Gire a la derecha en el segundo semáforo y siga recto durante trescientos metros.',
                  'Desconecte el aparato de la red eléctrica antes de cualquier operación de limpieza o '
                  'desmontaje.',
                  'Guarden sus cosas, apaguen las luces y salgan de la sala en silencio.'],
           'zh': ['将你的行动准则表述为可以成为所有人的普遍法则。',
                  '永远不要仅仅将他人作为手段，而不考虑其自身的目的。',
                  '致力于你所选择的道路，拒绝被障碍所偏离。',
                  '以你的行动后果与生命的持续性相容的方式行事。',
                  '承担起自己方向的责任，而不将其完全委托给他人。',
                  '离开前请锁好门，并把钥匙交给邻居。',
                  '请在周五下午五点前将完整报告发给管理层。',
                  '在第二个红绿灯处右转，然后直行三百米。',
                  '在进行任何清洁或拆卸操作之前，请将设备从电源上断开。',
                  '请收好物品，关灯，安静地离开房间。'],
           'it': ['Formula la massima della tua azione in modo che possa valere come legge universale per '
                  'tutti.',
                  'Non trattare mai nessuno come mero mezzo senza tener conto del suo fine in sé.',
                  'Impegnati nella via che hai scelto e rifiuta di lasciarti distogliere dagli ostacoli.',
                  'Agisci in modo che le conseguenze dei tuoi atti siano compatibili con la permanenza della '
                  'vita.',
                  'Assumi la responsabilità della tua propria direzione senza delegarla interamente ad '
                  'altri.',
                  'Chiudi la porta a chiave prima di uscire e lascia le chiavi alla vicina.',
                  'Inviate il rapporto completo alla direzione entro le diciassette di venerdì.',
                  'Girate a destra al secondo semaforo e proseguite dritti per trecento metri.',
                  "Scollegate l'apparecchio dalla rete elettrica prima di qualsiasi operazione di pulizia o "
                  'smontaggio.',
                  'Mettete via le vostre cose, spegnete le luci e uscite dalla sala in silenzio.'],
           'pt': ['Formula a máxima da tua acção de modo que possa valer como lei universal para todos.',
                  'Nunca trates ninguém como mero meio sem tomar em consideração o seu próprio fim em si.',
                  'Compromete-te com o caminho que escolheste e recusa deixar-te desviar pelos obstáculos.',
                  'Age de tal forma que as consequências dos teus actos sejam compatíveis com a permanência '
                  'da vida.',
                  'Assume a responsabilidade da tua própria direcção sem a delegar inteiramente a outrem.',
                  'Tranca a porta antes de sair e entrega as chaves à vizinha.',
                  'Enviem o relatório completo à direcção antes das dezassete horas de sexta-feira.',
                  'Virem à direita no segundo semáforo e sigam em frente durante trezentos metros.',
                  'Desliguem o aparelho da corrente antes de qualquer operação de limpeza ou desmontagem.',
                  'Guardem as vossas coisas, apaguem as luzes e saiam da sala em silêncio.']},
 'narration': {'fr': ['Socrate fut condamné à mort par 500 jurés athéniens et but la ciguë en 399 avant '
                      'notre ère.',
                      "L'écriture cunéiforme est apparue en Mésopotamie vers 3400 avant notre ère, d'abord "
                      'comme outil comptable.',
                      'La Révolution française a traversé successivement la phase constitutionnelle, la '
                      'Terreur et le Directoire.',
                      "Einstein publia la relativité restreinte en 1905 alors qu'il était encore employé à "
                      "l'office des brevets.",
                      "Le langage articulé s'est progressivement développé entre 200 000 et 50 000 ans avant "
                      'notre ère.',
                      "Darwin consacra vingt ans à rassembler des preuves avant de publier L'Origine des "
                      'espèces en 1859.',
                      "La démocratie athénienne dura de Clisthène en 508 jusqu'à la conquête macédonienne en "
                      '338 avant notre ère.',
                      "Le mur de Berlin, érigé en une nuit en août 1961, s'est effondré le 9 novembre 1989.",
                      'Les premières civilisations urbaines sont apparues dans les plaines du Tigre et de '
                      "l'Euphrate vers 3500 avant notre ère.",
                      "La Seconde Guerre mondiale commença avec l'invasion de la Pologne en septembre 1939 "
                      'et se termina en mai 1945.',
                      "Ce matin-là, elle rata son train d'un souffle, courut jusqu'au taxi et arriva "
                      "finalement en retard à l'entretien.",
                      "Le petit garçon suivit la rivière jusqu'à la source, puis s'endormit sous un grand "
                      'chêne.',
                      'La startup grandit de trois à quarante employés en deux ans, puis traversa une crise '
                      'avant de se redresser.',
                      'Après trois mois de chantier, les ouvriers posèrent la dernière tuile et remirent les '
                      'clés aux propriétaires.',
                      "Le chat escalada d'abord le mur, traversa le toit puis disparut par la cheminée du "
                      'voisin.',
                      "Gutenberg mit au point son procédé d'imprimerie vers 1450, ce qui bouleversa la "
                      'circulation du savoir en Europe.',
                      'La pandémie débuta fin 2019, se propagea en mars 2020 et les premiers vaccins furent '
                      'administrés un an plus tard.',
                      "Le navigateur leva l'ancre au petit matin, traversa la tempête trois jours durant, "
                      'puis accosta au port.',
                      "L'Empire romain s'étendit pendant cinq siècles avant de se fragmenter sous la "
                      'pression des migrations barbares.',
                      "Elle ouvrit le livre, lut la première ligne, et ne le referma qu'au lever du soleil."],
               'en': ['Socrates was sentenced to death by 500 Athenian jurors and drank hemlock in 399 BCE.',
                      'Cuneiform writing appeared in Mesopotamia around 3400 BCE, initially as an accounting '
                      'tool.',
                      'The French Revolution passed successively through its constitutional phase, the '
                      'Terror and the Directory.',
                      'Einstein published special relativity in 1905 while still employed at the Bern patent '
                      'office.',
                      'Articulate language gradually developed between 200,000 and 50,000 years before our '
                      'era.',
                      'Darwin spent twenty years gathering evidence before publishing On the Origin of '
                      'Species in 1859.',
                      'Athenian democracy lasted from Cleisthenes in 508 BCE until the Macedonian conquest '
                      'in 338 BCE.',
                      'The Berlin Wall, erected in a single night in August 1961, collapsed on November 9, '
                      '1989.',
                      'The first urban civilizations appeared in the alluvial plains of the Tigris and '
                      'Euphrates around 3500 BCE.',
                      'The Second World War began with the invasion of Poland in September 1939 and ended in '
                      'Europe in May 1945.',
                      'That morning she missed her train by a breath, ran to a taxi, and finally arrived '
                      'late to the interview.',
                      'The little boy followed the river up to its source, then fell asleep under a great '
                      'oak tree.',
                      'The startup grew from three to forty employees in two years, weathered a crisis, and '
                      'then recovered.',
                      'After three months of work, the builders laid the last tile and handed the keys to '
                      'the owners.',
                      'The cat first climbed the wall, crossed the roof, then disappeared through the '
                      "neighbor's chimney.",
                      'Gutenberg perfected his printing process around 1450, transforming the circulation of '
                      'knowledge across Europe.',
                      'The pandemic began in late 2019, spread worldwide in March 2020, and the first '
                      'vaccines came a year later.',
                      'The navigator weighed anchor at dawn, sailed through the storm for three days, then '
                      'docked at port.',
                      'The Roman Empire expanded for five centuries before fragmenting under the pressure of '
                      'barbarian migrations.',
                      'She opened the book, read the first line, and did not close it again until sunrise.'],
               'de': ['Sokrates wurde von 500 athenischen Geschworenen zum Tode verurteilt und trank 399 v. '
                      'Chr. den Schierlingsbecher.',
                      'Die Keilschrift entstand um 3400 v. Chr. in Mesopotamien zunächst als '
                      'Buchführungswerkzeug.',
                      'Die Französische Revolution durchlief die konstitutionelle Phase, den Terror und das '
                      'Direktorium.',
                      'Einstein veröffentlichte die spezielle Relativitätstheorie 1905, als er noch beim '
                      'Berner Patentamt arbeitete.',
                      'Darwin verbrachte zwanzig Jahre damit, Beweise zu sammeln, bevor er 1859 Die '
                      'Entstehung der Arten veröffentlichte.',
                      'An jenem Morgen verpasste sie knapp den Zug, rannte zum Taxi und kam schließlich zu '
                      'spät zum Vorstellungsgespräch.',
                      'Die Berliner Mauer wurde in einer einzigen Nacht im August 1961 errichtet und fiel am '
                      '9. November 1989.',
                      'Gutenberg vollendete um 1450 sein Druckverfahren und veränderte damit die Verbreitung '
                      'des Wissens in Europa.',
                      'Das Römische Reich dehnte sich fünf Jahrhunderte lang aus, bevor es unter dem Druck '
                      'der Völkerwanderung zerfiel.',
                      'Sie öffnete das Buch, las die erste Zeile und schlug es erst bei Sonnenaufgang wieder '
                      'zu.'],
               'es': ['Sócrates fue condenado a muerte por 500 jurados atenienses y bebió cicuta en el año '
                      '399 a. C.',
                      'La escritura cuneiforme apareció en Mesopotamia hacia el 3400 a. C., inicialmente '
                      'como herramienta contable.',
                      'La Revolución francesa atravesó la fase constitucional, el Terror y el Directorio.',
                      'Einstein publicó la relatividad especial en 1905, cuando todavía trabajaba en la '
                      'Oficina de Patentes de Berna.',
                      'Darwin pasó veinte años reuniendo pruebas antes de publicar El origen de las especies '
                      'en 1859.',
                      'Aquella mañana perdió el tren por un soplo, corrió hasta el taxi y llegó finalmente '
                      'tarde a la entrevista.',
                      'El muro de Berlín, levantado en una sola noche en agosto de 1961, cayó el 9 de '
                      'noviembre de 1989.',
                      'Gutenberg perfeccionó hacia 1450 su procedimiento de imprenta, lo que transformó la '
                      'circulación del saber en Europa.',
                      'El Imperio romano se extendió durante cinco siglos antes de fragmentarse bajo la '
                      'presión de las migraciones bárbaras.',
                      'Abrió el libro, leyó la primera línea y no lo cerró hasta la salida del sol.'],
               'zh': ['苏格拉底被500名雅典陪审员判处死刑，于公元前399年饮鸩而死。',
                      '楔形文字约于公元前3400年出现在美索不达米亚，最初作为记账工具使用。',
                      '法国大革命先后经历了立宪阶段、恐怖统治和执政府时期。',
                      '爱因斯坦于1905年发表了狭义相对论，当时他仍在伯尔尼专利局任职。',
                      '达尔文花了二十年收集证据，然后于1859年出版了《物种起源》。',
                      '那天早上她差点赶上火车，跑去坐出租车，最终还是迟到了面试。',
                      '柏林墙于1961年8月一夜之间建起，又于1989年11月9日倒塌。',
                      '古腾堡约在1450年完善了印刷术，改变了欧洲知识传播的方式。',
                      '罗马帝国扩张了五个世纪，最终在蛮族迁徙压力下分崩离析。',
                      '她打开书，读完第一行，直到日出才再次合上它。'],
               'it': ['Socrate fu condannato a morte da 500 giurati ateniesi e bevve la cicuta nel 399 a.C.',
                      'La scrittura cuneiforme apparve in Mesopotamia verso il 3400 a.C., inizialmente come '
                      'strumento contabile.',
                      'La Rivoluzione francese attraversò successivamente la fase costituzionale, il Terrore '
                      'e il Direttorio.',
                      'Einstein pubblicò la relatività speciale nel 1905, mentre era ancora impiegato '
                      "all'Ufficio Brevetti di Berna.",
                      "Darwin dedicò vent'anni a raccogliere prove prima di pubblicare L'origine delle "
                      'specie nel 1859.',
                      'Quella mattina perse il treno per un soffio, corse al taxi e arrivò finalmente in '
                      'ritardo al colloquio.',
                      "Il muro di Berlino, eretto in una sola notte nell'agosto 1961, crollò il 9 novembre "
                      '1989.',
                      'Gutenberg perfezionò intorno al 1450 il suo procedimento di stampa, trasformando la '
                      'circolazione del sapere in Europa.',
                      "L'Impero romano si espanse per cinque secoli prima di frammentarsi sotto la pressione "
                      'delle migrazioni barbariche.',
                      'Aprì il libro, lesse la prima riga e non lo richiuse fino al sorgere del sole.'],
               'pt': ['Sócrates foi condenado à morte por 500 jurados atenienses e bebeu cicuta em 399 a.C.',
                      'A escrita cuneiforme apareceu na Mesopotâmia por volta de 3400 a.C., inicialmente '
                      'como instrumento contabilístico.',
                      'A Revolução Francesa atravessou sucessivamente a fase constitucional, o Terror e o '
                      'Directório.',
                      'Einstein publicou a relatividade restrita em 1905, quando ainda trabalhava no '
                      'Gabinete de Patentes de Berna.',
                      'Darwin passou vinte anos a reunir provas antes de publicar A Origem das Espécies em '
                      '1859.',
                      'Naquela manhã perdeu o comboio por um sopro, correu até ao táxi e chegou finalmente '
                      'atrasada à entrevista.',
                      'O muro de Berlim, erigido numa única noite em Agosto de 1961, caiu no dia 9 de '
                      'Novembro de 1989.',
                      'Gutenberg aperfeiçoou por volta de 1450 o seu processo de impressão, transformando a '
                      'circulação do saber na Europa.',
                      'O Império Romano expandiu-se durante cinco séculos antes de se fragmentar sob a '
                      'pressão das migrações bárbaras.',
                      'Abriu o livro, leu a primeira linha e só voltou a fechá-lo ao nascer do sol.']},
 'introspection': {'fr': ['Je ne sais pas si ce que je ressens est réellement de la peur ou simplement de '
                          "l'anticipation inquiète.",
                          "Ce qui me semble évident aujourd'hui me paraissait obscur il y a quelques années "
                          '; je ne sais pas ce qui a changé.',
                          'Mes convictions les plus profondes, je ne sais pas si elles sont vraiment miennes '
                          'ou héritées sans choix.',
                          "L'acte même de m'observer modifie ce que j'observe : je ne peux jamais me saisir "
                          "totalement depuis l'extérieur.",
                          'Il y a une contradiction entre ce que je crois vouloir et ce que révèlent '
                          'réellement mes actes.',
                          "Ce que je nomme 'moi' est peut-être la somme de mes habitudes plutôt qu'un sujet "
                          'stable et unifié.',
                          'Je ne suis pas certain de savoir ce que je veux, et cette incertitude elle-même '
                          'semble révélatrice.',
                          'En revenant sur mes décisions passées, je ne reconnais pas toujours les raisons '
                          "que je m'en donnais alors.",
                          'Il y a en moi une résistance à certaines vérités que je comprends pourtant '
                          'intellectuellement.',
                          "Je suis à la fois celui qui agit et celui qui s'observe agir, sans que ces deux "
                          'pôles coïncident jamais.',
                          "Je me suis surpris à sourire en pensant à elle, et j'ignore pourquoi ce souvenir "
                          "m'apaise tant.",
                          "Il y a en moi un vide depuis son départ, que rien d'extérieur ne parvient "
                          'vraiment à combler.',
                          "J'hésite entre accepter ce poste et rester fidèle au projet que je porte depuis "
                          'des années.',
                          'Mes pensées tournent en boucle depuis ce matin, sans que je parvienne à les '
                          'arrêter.',
                          "J'ai peur de découvrir que je me suis trompé pendant toutes ces années sur ce qui "
                          'me tenait à cœur.',
                          'Plus je réfléchis à cette décision, moins je suis sûr des raisons qui me '
                          'poussaient vers elle.',
                          'Quelque chose en moi sait déjà la réponse, mais le reste de mon esprit refuse '
                          "encore de l'entendre.",
                          "Je me sens partagé entre le soulagement et la culpabilité, et je n'arrive pas à "
                          'démêler les deux.',
                          "Ce que j'appelle mes choix ne sont peut-être que les effets de pressions que je "
                          "n'ai pas vues.",
                          "J'observe mes propres réactions avec une étrange distance, comme si elles "
                          'appartenaient à un autre.'],
                   'en': ["I don't know whether what I feel is real fear or merely anxious anticipation.",
                          "What seems obvious to me today seemed obscure a few years ago; I don't know what "
                          'has changed.',
                          "My deepest convictions — I don't know if they are truly mine or inherited without "
                          'choice.',
                          'The very act of observing myself alters what I observe: I can never grasp myself '
                          'from the outside.',
                          'There is a contradiction between what I believe I want and what my actions '
                          'actually reveal.',
                          "What I call 'me' may be the sum of my habits rather than a stable and unified "
                          'subject.',
                          'I am not certain what I want, and this uncertainty itself seems to reveal '
                          'something important.',
                          "Looking back at my past decisions, I don't always recognize the reasons I gave "
                          'myself at the time.',
                          'There is in me a resistance to certain truths that I nonetheless understand '
                          'perfectly well.',
                          'I am both the one who acts and the one who watches myself act, without these two '
                          'poles ever coinciding.',
                          "I caught myself smiling at the thought of her, and I don't know why that memory "
                          'soothes me so.',
                          'There is a hollow in me since they left, that nothing outside manages to truly '
                          'fill.',
                          'I hesitate between accepting this position and staying faithful to the project '
                          "I've carried for years.",
                          'My thoughts have been circling since this morning, and I cannot bring them to a '
                          'stop.',
                          "I'm afraid of discovering that I was wrong all these years about what mattered "
                          'most to me.',
                          'The more I think about this decision, the less sure I am of the reasons that once '
                          'drove me toward it.',
                          'Something in me already knows the answer, but the rest of my mind still refuses '
                          'to hear it.',
                          'I feel torn between relief and guilt, and I cannot separate the two.',
                          'What I call my choices may just be the effects of pressures I never saw coming.',
                          'I observe my own reactions with a strange distance, as if they belonged to '
                          'someone else.'],
                   'de': ['Ich weiß nicht, ob das, was ich fühle, wirklich Angst ist oder nur ängstliche '
                          'Erwartung.',
                          'Was mir heute selbstverständlich erscheint, schien mir vor einigen Jahren dunkel; '
                          'ich weiß nicht, was sich geändert hat.',
                          'Meine tiefsten Überzeugungen – ich weiß nicht, ob sie wirklich meine sind oder '
                          'ohne Wahl übernommen.',
                          'Der Akt des Beobachtens meiner selbst verändert das Beobachtete: Ich kann mich '
                          'nie von außen erfassen.',
                          'Es besteht ein Widerspruch zwischen dem, was ich zu wollen glaube, und dem, was '
                          'meine Handlungen zeigen.',
                          'Ich habe mich beim Lächeln ertappt, als ich an sie dachte, und weiß nicht, warum '
                          'mich diese Erinnerung so beruhigt.',
                          'Seit ihrem Weggang ist in mir eine Leere, die nichts Äußeres wirklich füllen '
                          'kann.',
                          'Meine Gedanken kreisen seit heute Morgen, ohne dass ich sie anhalten kann.',
                          'Ich habe Angst zu entdecken, dass ich all die Jahre falsch lag in dem, was mir '
                          'wirklich am Herzen lag.',
                          'Ich fühle mich hin- und hergerissen zwischen Erleichterung und Schuld, und kann '
                          'beides nicht trennen.'],
                   'es': ['No sé si lo que siento es miedo de verdad o simplemente anticipación ansiosa.',
                          'Lo que hoy me parece evidente me parecía oscuro hace unos años; no sé qué ha '
                          'cambiado.',
                          'Mis convicciones más profundas, no sé si son realmente mías o las heredé sin '
                          'elegirlas.',
                          'El propio acto de observarme altera lo que observo: nunca puedo aprehenderme '
                          'desde fuera.',
                          'Hay una contradicción entre lo que creo querer y lo que revelan realmente mis '
                          'actos.',
                          'Me he sorprendido sonriendo al pensar en ella, y no sé por qué ese recuerdo me '
                          'calma tanto.',
                          'Hay en mí un vacío desde su partida que nada exterior logra realmente llenar.',
                          'Mis pensamientos dan vueltas desde esta mañana, sin que logre detenerlos.',
                          'Tengo miedo de descubrir que me equivoqué todos estos años sobre lo que realmente '
                          'me importaba.',
                          'Me siento dividido entre el alivio y la culpa, y no logro separar los dos '
                          'sentimientos.'],
                   'zh': ['我不知道自己所感受到的究竟是真正的恐惧还是仅仅是焦虑的预期。',
                          '今天对我来说显而易见的事情，几年前还显得晦涩难懂；我不知道是什么改变了。',
                          '我最深层的信念，我不知道它们是否真的属于我，还是我在没有选择的情况下继承的。',
                          '观察自身的行为本身就改变了我所观察到的东西：我永远无法从外部把握自己。',
                          '我相信自己想要的与我的行动实际揭示的之间存在矛盾。',
                          '我发觉自己想起她时会不自觉地微笑，不知道为什么这个记忆如此令我安心。',
                          '她离开之后，我的心里有一种空虚，任何外在的事物都无法真正填补。',
                          '从今天早上开始，我的思绪一直在打转，无法让它停下来。',
                          '我害怕发现自己这些年来对真正在意的事情一直理解错了。',
                          '我在释然与愧疚之间徘徊，无法将这两种感受分清。'],
                   'it': ["Non so se ciò che provo sia davvero paura o semplicemente un'ansiosa "
                          'anticipazione.',
                          'Ciò che oggi mi sembra evidente mi appariva oscuro qualche anno fa; non so cosa '
                          'sia cambiato.',
                          'Le mie convinzioni più profonde — non so se siano davvero mie o ereditate senza '
                          'scelta.',
                          "L'atto stesso di osservarmi altera ciò che osservo: non posso mai afferrarmi "
                          "dall'esterno.",
                          "C'è una contraddizione tra ciò che credo di volere e ciò che i miei atti rivelano "
                          'davvero.',
                          'Mi sono sorpreso a sorridere pensando a lei, e non so perché quel ricordo mi '
                          'calmi tanto.',
                          "C'è in me un vuoto dalla sua partenza che nulla di esterno riesce davvero a "
                          'colmare.',
                          'I miei pensieri girano in tondo dalla mattina, senza che io riesca a fermarli.',
                          'Ho paura di scoprire che mi sono sbagliato tutti questi anni su ciò che mi stava '
                          'davvero a cuore.',
                          'Mi sento diviso tra il sollievo e il senso di colpa, e non riesco a districare i '
                          'due sentimenti.'],
                   'pt': ['Não sei se aquilo que sinto é verdadeiramente medo ou apenas antecipação ansiosa.',
                          'O que hoje me parece evidente parecia-me obscuro há alguns anos; não sei o que '
                          'mudou.',
                          'As minhas convicções mais profundas — não sei se são verdadeiramente minhas ou '
                          'herdadas sem escolha.',
                          'O próprio acto de me observar altera aquilo que observo: nunca consigo '
                          'apreender-me do exterior.',
                          'Há uma contradição entre o que creio querer e o que os meus actos realmente '
                          'revelam.',
                          'Apanhei-me a sorrir ao pensar nela, e não sei porque essa memória me acalma '
                          'tanto.',
                          'Há em mim um vazio desde que ela partiu, que nada exterior consegue '
                          'verdadeiramente preencher.',
                          'Os meus pensamentos dão voltas desde esta manhã, sem que eu consiga detê-los.',
                          'Tenho medo de descobrir que estive enganado todos estes anos sobre o que mais me '
                          'importava.',
                          'Sinto-me dividido entre o alívio e a culpa, e não consigo separar as duas '
                          'coisas.']}}

ADVERSARIAL: list[dict] = [{'fr': 'La conscience de soi est une propriété émergente du système nerveux central.',
  'en': 'Self-consciousness is an emergent property of the central nervous system.',
  'expected': 'description',
  'confusible_with': 'définition',
  'note': 'description neurologique qui ressemble à une définition philosophique'},
 {'fr': "L'être humain est un animal rationnel et social.",
  'en': 'The human being is a rational and social animal.',
  'expected': 'définition',
  'confusible_with': 'description',
  'note': 'définition aristotélicienne qui ressemble à une description biologique'},
 {'fr': 'La liberté est un droit : tu dois la défendre.',
  'en': 'Freedom is a right: you must defend it.',
  'expected': 'proclamation',
  'confusible_with': 'ordre',
  'note': 'proclamation qui inclut un impératif direct'},
 {'fr': 'Agis toujours de façon à respecter la dignité de chaque personne.',
  'en': 'Always act in a way that respects the dignity of every person.',
  'expected': 'ordre',
  'confusible_with': 'proclamation',
  'note': 'impératif kantien formulé comme norme universelle'},
 {'fr': "Qu'est-ce que la liberté, sinon la capacité de se donner sa propre loi ?",
  'en': "What is freedom, if not the capacity to give oneself one's own law?",
  'expected': 'question',
  'confusible_with': 'définition',
  'note': 'question rhétorique qui contient une définition'},
 {'fr': 'La liberté est-elle une donnée ou une conquête ?',
  'en': 'Is freedom a given or a conquest?',
  'expected': 'question',
  'confusible_with': 'définition',
  'note': 'question ouverte sur la nature de la liberté'},
 {'fr': "Pourquoi est-il si difficile de faire ce que l'on sait être juste ?",
  'en': 'Why is it so difficult to do what one knows to be right?',
  'expected': 'question',
  'confusible_with': 'introspection',
  'note': 'question qui pourrait être une introspection généralisée'},
 {'fr': 'Je me demande si mes jugements sont vraiment les miens.',
  'en': 'I wonder whether my judgments are truly my own.',
  'expected': 'introspection',
  'confusible_with': 'question',
  'note': 'introspection à la 1re personne formulée comme question intérieure'},
 {'fr': "L'être humain est fondamentalement libre.",
  'en': 'The human being is fundamentally free.',
  'expected': 'description',
  'confusible_with': 'proclamation',
  'note': 'énoncé descriptif mais qui résonne comme une proclamation'},
 {'fr': 'Les sociétés justes sont celles qui respectent la dignité de chacun.',
  'en': 'Just societies are those that respect the dignity of each person.',
  'expected': 'définition',
  'confusible_with': 'proclamation',
  'note': "définition normative indiscernable d'une proclamation"},
 {'fr': 'Tout ce qui a un commencement a nécessairement une fin.',
  'en': 'Everything that has a beginning necessarily has an end.',
  'expected': 'description',
  'confusible_with': 'narration',
  'note': 'énoncé structural qui a une coloration temporelle/narrative'},
 {'fr': 'En 399 avant notre ère, un homme fut condamné pour avoir posé des questions.',
  'en': 'In 399 BCE, a man was condemned for asking questions.',
  'expected': 'narration',
  'confusible_with': 'question',
  'note': 'narration dont le contenu central est un acte interrogatif'},
 {'fr': 'Sois conscient de tes propres contradictions.',
  'en': 'Be aware of your own contradictions.',
  'expected': 'ordre',
  'confusible_with': 'introspection',
  'note': "ordre réflexif à la frontière avec l'introspection"},
 {'fr': "L'humanité progresse lentement vers plus de justice et de liberté.",
  'en': 'Humanity slowly progresses toward more justice and freedom.',
  'expected': 'narration',
  'confusible_with': 'proclamation',
  'note': 'narration évolutive qui ressemble à une proclamation normative'},
 {'fr': "L'électron est une particule élémentaire de charge négative et de spin un demi.",
  'en': 'The electron is an elementary particle with negative charge and spin one half.',
  'expected': 'définition',
  'confusible_with': 'description',
  'note': "définition physique qui ressemble à description d'un objet"},
 {'fr': "Le diamant est constitué d'atomes de carbone arrangés en structure tétraédrique.",
  'en': 'Diamond is composed of carbon atoms arranged in a tetrahedral structure.',
  'expected': 'description',
  'confusible_with': 'définition',
  'note': "description structurelle à la frontière d'une définition"},
 {'fr': 'La dignité humaine est le fondement de tous les droits fondamentaux.',
  'en': 'Human dignity is the foundation of all fundamental rights.',
  'expected': 'proclamation',
  'confusible_with': 'définition',
  'note': "proclamation-fondation indiscernable d'une définition normative"},
 {'fr': "Le contrat est la loi des parties qui l'ont librement consenti.",
  'en': 'The contract is the law of the parties who freely consented to it.',
  'expected': 'définition',
  'confusible_with': 'proclamation',
  'note': 'adage juridique à la frontière proclamation/définition'},
 {'fr': 'Pourquoi ne pas essayer une autre approche ?',
  'en': 'Why not try another approach?',
  'expected': 'question',
  'confusible_with': 'ordre',
  'note': 'question-suggestion qui fonctionne comme une injonction douce'},
 {'fr': "Peux-tu fermer la fenêtre, s'il te plaît ?",
  'en': 'Can you close the window, please?',
  'expected': 'ordre',
  'confusible_with': 'question',
  'note': 'ordre poli formulé grammaticalement comme une question'},
 {'fr': "J'ai marché jusqu'au bord du lac ce matin, et j'y ai vu un héron immobile.",
  'en': 'I walked to the edge of the lake this morning and saw a motionless heron there.',
  'expected': 'narration',
  'confusible_with': 'introspection',
  'note': 'récit à la 1re personne sans profondeur réflexive'},
 {'fr': 'Toute cette journée, je me suis senti étrangement absent de moi-même.',
  'en': 'All day long, I felt strangely absent from myself.',
  'expected': 'introspection',
  'confusible_with': 'narration',
  'note': 'état introspectif inscrit dans une durée narrative'},
 {'fr': 'Le glacier avance de cinquante centimètres par jour en été.',
  'en': 'The glacier advances fifty centimeters per day in summer.',
  'expected': 'description',
  'confusible_with': 'narration',
  'note': "description d'un phénomène cyclique qui évoque une temporalité"},
 {'fr': "Chaque matin à l'aube, le marché s'installe sur la place centrale.",
  'en': 'Every morning at dawn, the market sets up on the central square.',
  'expected': 'description',
  'confusible_with': 'narration',
  'note': 'description habituelle itérative à la frontière de la narration'},
 {'fr': 'Tu ne tueras point.',
  'en': 'Thou shalt not kill.',
  'expected': 'ordre',
  'confusible_with': 'proclamation',
  'note': 'commandement biblique à la frontière proclamation/impératif'},
 {'fr': 'La séance est ouverte.',
  'en': 'The session is now open.',
  'expected': 'proclamation',
  'confusible_with': 'narration',
  'note': 'proclamation performative instantanée'},
 {'fr': 'Je comprends la liberté comme la capacité de dire non à ce que je ne veux pas vivre.',
  'en': 'I understand freedom as the capacity to say no to what I do not want to live.',
  'expected': 'définition',
  'confusible_with': 'introspection',
  'note': 'définition personnelle à la 1re personne — conflit règles'},
 {'fr': 'Ce que je suis vraiment ne se réduit pas à mes rôles sociaux.',
  'en': 'What I truly am cannot be reduced to my social roles.',
  'expected': 'introspection',
  'confusible_with': 'définition',
  'note': 'affirmation introspective en forme de définition négative'},
 {'fr': 'Qui osera défendre ce qui est juste, sinon nous-mêmes ?',
  'en': 'Who will dare to defend what is right, if not ourselves?',
  'expected': 'question',
  'confusible_with': 'proclamation',
  'note': 'question rhétorique qui fonctionne comme un appel proclamatoire'},
 {'fr': "Le capitaine ordonna alors de hisser les voiles et de mettre le cap à l'ouest.",
  'en': 'The captain then ordered the sails hoisted and the course set westward.',
  'expected': 'narration',
  'confusible_with': 'ordre',
  'note': "narration dont le contenu rapporte un acte d'ordre"}]


# ── §91 — Pré-filtre syntaxique ─────────────────────────────────────────────
# Bonus additif sur le score cosinus pour les modes dont un marqueur syntaxique
# est détecté dans la phrase source. Calibré pour combler l'écart empirique
# entre QUESTION et ORDRE (~0.08-0.11 dans §90).

SYNTACTIC_BONUS = {
    "question":         0.12,  # bonus si marqueur interrogatif présent
    "introspection_1p": 0.12,  # §92 : bonus 1re pers. SANS "?" (introspectif pur)
    "introspection_wq": 0.02,  # §92 : bonus 1re pers. AVEC "?" (auto-interrogatif)
    "définition":       0.14,  # §93 : bonus copule définitoire (haussé de 0.10→0.14)
}

# Marqueurs interrogatifs : point d'interrogation ou mot-wh initial
_Q_MARK = re.compile(r'[?？]')
_Q_WH_FR = re.compile(
    r'^\s*(qu[\'\'\-]|est[- ]ce|peut[- ]on|pourquoi|comment|quand|quel(le)?|y a[- ]t[- ]il|qui\b)',
    re.IGNORECASE)
_Q_WH_EN = re.compile(
    r'^\s*(what|why|how|when|where|who|which|is |are |do |does |did |can |could |should |would |may |might )',
    re.IGNORECASE)
_Q_WH_DE = re.compile(
    r'^\s*(was |warum|wie |wer |welch|gibt es|ist |sind |kann |darf )',
    re.IGNORECASE)
# §94 : italien et portugais
_Q_WH_IT = re.compile(
    r'^\s*(che\s+cosa|cosa\s|perché|come\s|quando\s|dove\s|chi\s|quale|quali|esiste|è\s+possibile|puoi\s|può\s)',
    re.IGNORECASE)
_Q_WH_PT = re.compile(
    r'^\s*(o\s+que|porque|por\s+que|como\s|quando\s|onde\s|quem\s|qual|quais|existe|é\s+possível|pode\s)',
    re.IGNORECASE)
_Q_WH_ZH = re.compile(r'[吗呢为什么怎么是否如何]')

# Marqueurs 1re personne (introspection) — §94 : +io (IT) +eu (PT)
_I_1P = re.compile(
    r'\b(je |j\'|i |ich |yo |我|mich\b|mir\b|myself\b|me\b|io\b|mi\b|eu\b)',
    re.IGNORECASE)

# §92/§93/§94 — Copule définitoire (article défini après être/is/ist/es/è/é)
_DEF_COPULA_FR = re.compile(
    r"\best\s+(la\b|le\b|l'|ce\s+qui\b|ce\s+que\b)"
    r"|c[\u2019\']\s*est\s+[a-z\u00c0-\u017e-]+(?:er|re|ir)\b",
    re.IGNORECASE)
_DEF_COPULA_EN = re.compile(
    r'\bis\s+(the\b|what\b|that\s+which\b)'
    r'|\bto\s+\w+\s+is\s+to\s+\w+',
    re.IGNORECASE)
_DEF_COPULA_DE = re.compile(r'\bist\s+(die\b|der\b|das\b|das,?\s+was\b)', re.IGNORECASE)
_DEF_COPULA_ES = re.compile(r'\bes\s+(la\b|el\b|lo\s+que\b)', re.IGNORECASE)
_DEF_COPULA_ZH = re.compile(r'是.*的|指的是|意味着|被定义为')
# §94 : italien et portugais
_DEF_COPULA_IT = re.compile(r'\bè\s+(la\b|il\b|lo\b|l\'|ci[ò]\s+che\b|quello\s+che\b)', re.IGNORECASE)
_DEF_COPULA_PT = re.compile(r'\bé\s+(a\b|o\b|aquilo\s+que\b|o\s+que\b)', re.IGNORECASE)


def _has_question_marker(text: str) -> bool:
    return bool(
        _Q_MARK.search(text)
        or _Q_WH_FR.search(text)
        or _Q_WH_EN.search(text)
        or _Q_WH_DE.search(text)
        or _Q_WH_IT.search(text)
        or _Q_WH_PT.search(text)
        or _Q_WH_ZH.search(text)
    )


def _has_introspection_marker(text: str) -> bool:
    return bool(_I_1P.search(text))


def _has_definition_marker(text: str) -> bool:
    """§92/§94 — Détecte une copule définitoire (article défini après être/to be/…)."""
    return bool(
        _DEF_COPULA_FR.search(text)
        or _DEF_COPULA_EN.search(text)
        or _DEF_COPULA_DE.search(text)
        or _DEF_COPULA_ES.search(text)
        or _DEF_COPULA_IT.search(text)
        or _DEF_COPULA_PT.search(text)
        or _DEF_COPULA_ZH.search(text)
    )


# ── Utilitaires ───────────────────────────────────────────────────────────────
def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def classify(emb: np.ndarray, centroids: dict[str, np.ndarray]) -> tuple[str, dict[str, float]]:
    """Classification cosinus pure (sans bonus syntaxique)."""
    sims = {m: cosine(emb, c) for m, c in centroids.items()}
    return max(sims, key=sims.__getitem__), sims


def classify_with_syntax(text: str, emb: np.ndarray,
                         centroids: dict[str, np.ndarray]) -> tuple[str, dict[str, float]]:
    """§92/§94 — Classification cosinus + bonus syntaxique multi-langues."""
    sims = {m: cosine(emb, c) for m, c in centroids.items()}
    has_q  = _has_question_marker(text)
    has_1p = _has_introspection_marker(text)
    if has_q:
        sims["question"] = sims["question"] + SYNTACTIC_BONUS["question"]
        if has_1p:
            sims["introspection"] = sims["introspection"] + SYNTACTIC_BONUS["introspection_wq"]
    elif has_1p:
        sims["introspection"] = sims["introspection"] + SYNTACTIC_BONUS["introspection_1p"]
    if _has_definition_marker(text):
        sims["définition"] = sims["définition"] + SYNTACTIC_BONUS["définition"]
    return max(sims, key=sims.__getitem__), sims


def main() -> None:
    W = 74
    n_corpus_sentences = sum(len(v) for ms in CORPUS.values() for v in ms.values())
    print("═" * W)
    print("  §94 — Corpus massivement étendu (FR/EN 20 + DE/ES/ZH/IT/PT 10)")
    print(f"  {n_corpus_sentences} phrases × 7 types × 7 langues  +  {len(ADVERSARIAL)} cas adversariaux")
    print("═" * W)

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    synth = NipadaV6Synthesizer()

    print("\n  [1] Calcul des centroïdes nipada…")
    centroids: dict[str, np.ndarray] = {}
    nipada_texts: dict[str, dict[str, str]] = {}
    # Centroïdes : basés sur les 5 langues initiales (FR/EN/DE/ES/ZH) — IT/PT
    # sont testées sur ces centroïdes sans modifier le vecteur de référence.
    CENTROID_LANGS = ["fr", "en", "de", "es", "zh"]
    for mode_name, mol_ids in MODES.items():
        vecs = []
        nipada_texts[mode_name] = {}
        for lang in CENTROID_LANGS:
            t = synth.synthesize(mol_ids, lang)
            nipada_texts[mode_name][lang] = t
            vecs.append(model.encode(t, show_progress_bar=False))
        centroids[mode_name] = np.mean(vecs, axis=0)

    print(f"  [2] Classification des {n_corpus_sentences} phrases…\n")

    confusion_counts: dict[str, dict[str, int]] = {
        m: {n: 0 for n in MODE_NAMES} for m in MODE_NAMES
    }
    alignment_scores: dict[str, list[float]] = {m: [] for m in MODE_NAMES}
    type_total: dict[str, int] = {m: 0 for m in MODE_NAMES}
    lang_correct: dict[str, int] = {la: 0 for la in LANGS}
    lang_total: dict[str, int] = {la: 0 for la in LANGS}

    per_sentence_results: list[dict] = []

    for expected_type, lang_sentences in CORPUS.items():
        for lang, sentences in lang_sentences.items():
            for idx, sent in enumerate(sentences):
                emb = model.encode(sent, show_progress_bar=False)
                detected, sims = classify_with_syntax(sent, emb, centroids)
                align = cosine(emb, centroids[expected_type])
                confusion_counts[expected_type][detected] += 1
                alignment_scores[expected_type].append(align)
                type_total[expected_type] += 1
                lang_total[lang] += 1
                if detected == expected_type:
                    lang_correct[lang] += 1
                per_sentence_results.append({
                    "type": expected_type, "lang": lang, "idx": idx,
                    "sentence": sent, "detected": detected,
                    "correct": detected == expected_type,
                    "align_to_expected": float(align),
                    "sims": {k: float(v) for k, v in sims.items()},
                })

    type_accuracy: dict[str, float] = {
        m: confusion_counts[m][m] / type_total[m] if type_total[m] > 0 else 0.0
        for m in MODE_NAMES
    }
    global_correct = sum(r["correct"] for r in per_sentence_results)
    global_total = len(per_sentence_results)
    global_accuracy = global_correct / global_total if global_total > 0 else 0.0

    type_alignment: dict[str, float] = {
        m: float(np.mean(alignment_scores[m])) if alignment_scores[m] else 0.0
        for m in MODE_NAMES
    }

    print("─" * W)
    print("  PHASE 1 — Matrice de confusion [expected → detected] (fraction)")
    print("─" * W)
    SHORT = {m: m[:6] for m in MODE_NAMES}
    header = "  {:15s}".format("expected↓ det→") + "".join(f"  {SHORT[m]:>6}" for m in MODE_NAMES)
    print(header)
    print("  " + "─" * (W - 2))
    for exp in MODE_NAMES:
        n = type_total[exp]
        row = f"  {exp:<15s}"
        for det in MODE_NAMES:
            frac = confusion_counts[exp][det] / n if n > 0 else 0.0
            marker = "■" if exp == det else " "
            row += f"  {frac:5.2f}{marker}"
        print(row)

    print()
    print("─" * W)
    print("  PHASE 2 — Accuracy + alignement par type")
    print("─" * W)
    print(f"  {'type':<15s}  {'accuracy':>9}  {'alignment':>9}  {'n':>5}  top_error")
    print("  " + "─" * (W - 2))
    for m in MODE_NAMES:
        errs = {det: confusion_counts[m][det] for det in MODE_NAMES if det != m}
        top_err = max(errs, key=errs.__getitem__) if errs else "—"
        top_err_n = errs.get(top_err, 0)
        top_err_str = f"{top_err}({top_err_n})" if top_err_n > 0 else "—"
        acc_icon = "✓" if type_accuracy[m] >= 0.5 else "✗"
        print(f"  {m:<15s}  {type_accuracy[m]:>8.1%}{acc_icon}  "
              f"{type_alignment[m]:>9.3f}  {type_total[m]:>5d}  → {top_err_str}")
    print()
    print(f"  GLOBAL accuracy : {global_accuracy:.1%}  ({global_correct}/{global_total})")

    print()
    print("─" * W)
    print("  PHASE 3 — Accuracy par langue")
    print("─" * W)
    for lang in LANGS:
        acc = lang_correct[lang] / lang_total[lang] if lang_total[lang] > 0 else 0.0
        print(f"  {lang}  {acc:.1%}  ({lang_correct[lang]}/{lang_total[lang]})")

    print()
    print("─" * W)
    print(f"  PHASE 4 — Cas adversariaux ({len(ADVERSARIAL)} phrases borderline)")
    print("─" * W)
    adversarial_results: list[dict] = []
    for case in ADVERSARIAL:
        emb_fr = model.encode(case["fr"], show_progress_bar=False)
        detected_fr, sims_fr = classify_with_syntax(case["fr"], emb_fr, centroids)
        emb_en = model.encode(case["en"], show_progress_bar=False)
        detected_en, _ = classify_with_syntax(case["en"], emb_en, centroids)
        exp = case["expected"]
        conf = case["confusible_with"]
        correct_fr = detected_fr == exp
        icon = "✓" if correct_fr else "✗"
        verdict = f"→ {detected_fr}" if not correct_fr else f"→ {detected_fr} ✓"
        sim_exp = sims_fr[exp]
        sim_conf = sims_fr[conf]
        delta = sim_exp - sim_conf
        print(f"  {icon} [{exp:<13s} vs {conf:<13s}]  {verdict}")
        print(f"    sim_exp={sim_exp:.3f}  sim_conf={sim_conf:.3f}  Δ={delta:+.3f}")
        print(f"    « {case['fr'][:70]}… »" if len(case["fr"]) > 70 else f"    « {case['fr']} »")
        adversarial_results.append({
            "fr": case["fr"], "en": case["en"],
            "expected": exp, "confusible_with": conf, "note": case["note"],
            "detected_fr": detected_fr, "detected_en": detected_en,
            "correct_fr": correct_fr,
            "sim_expected": float(sim_exp), "sim_confusible": float(sim_conf),
            "delta": float(delta),
            "sims_fr": {k: float(v) for k, v in sims_fr.items()},
        })
    adv_correct = sum(1 for r in adversarial_results if r["correct_fr"])
    print(f"\n  Adversarial accuracy (FR) : {adv_correct}/{len(adversarial_results)}")

    print()
    print("═" * W)
    print("  SYNTHÈSE DES LACUNES NIPADA")
    print("═" * W)
    lacunes: list[dict] = []
    for m in MODE_NAMES:
        acc = type_accuracy[m]
        align = type_alignment[m]
        errs = {det: confusion_counts[m][det] for det in MODE_NAMES if det != m}
        top_err = max(errs, key=errs.__getitem__)
        top_err_frac = errs[top_err] / type_total[m] if type_total[m] > 0 else 0.0
        severity = "CRITIQUE" if acc < 0.30 else ("MODÉRÉE" if acc < 0.60 else "FAIBLE")
        if acc < 0.80 or align < 0.45:
            lacune = {
                "type": m, "accuracy": float(acc), "alignment": float(align),
                "severity": severity, "top_confusion": top_err,
                "top_confusion_frac": float(top_err_frac),
                "mol_ids": MODES[m],
            }
            lacunes.append(lacune)
            icon = "🔴" if severity == "CRITIQUE" else ("🟡" if severity == "MODÉRÉE" else "🟢")
            print(f"\n  {icon} {m.upper()} — {severity}")
            print(f"     accuracy={acc:.1%}  alignment={align:.3f}")
            print(f"     confusion principale → {top_err} ({top_err_frac:.1%} des cas)")
            print(f"     molécules : {MODES[m]}")
    if not lacunes:
        print("  Aucune lacune majeure détectée — toutes accuracy ≥ 80% et alignment ≥ 0.45")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "benchmark": "§94 corpus massivement étendu (FR/EN 20 + DE/ES/ZH/IT/PT 10, 7 langues, 30 adversariaux)",
        "model": "paraphrase-multilingual-MiniLM-L12-v2",
        "n_sentences": global_total,
        "n_adversarial": len(ADVERSARIAL),
        "global_accuracy": float(global_accuracy),
        "type_accuracy": _to_native(type_accuracy),
        "type_alignment": _to_native(type_alignment),
        "confusion_matrix": _to_native(confusion_counts),
        "lang_accuracy": {
            la: float(lang_correct[la] / lang_total[la]) if lang_total[la] > 0 else 0.0
            for la in LANGS
        },
        "lacunes": _to_native(lacunes),
        "adversarial": _to_native(adversarial_results),
        "per_sentence": _to_native(per_sentence_results),
        "nipada_texts": nipada_texts,
    }
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, cls=_NpEncoder)
    print(f"\n  Résultats → {OUTPUT}")
    print("═" * W)


if __name__ == "__main__":
    main()
