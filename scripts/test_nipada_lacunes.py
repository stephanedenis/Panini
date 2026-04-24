#!/usr/bin/env python3
"""
§86/§90/§92 — Lacunes nipada : corpus étendu multi-genre + matrice de confusion
===========================================================================
Version §90 : utilise NipadaV6Synthesizer (6 atomes : +TEMPS(13)) et MODES_V6
  §87 — narration : [13, 78, 273]  TEMPS+DEVENIR+SUCCESSION (vs §86 [462,1155])
  §88 — question  : [143, 165, 11] INTERROGATION(11×13)+JUGEMENT+SUJET
  §89 — introspection : [2310, 22, 26] +ÉVOLUTION(2×13)
  §91 — pré-filtre syntaxique QUESTION(?/wh) +0.12 + INTROSPECTION(1re pers.) +0.06
  §92 — copule définitoire (est la/le/l'/ce qui) → DÉFINITION +0.10
         introspection 1p sans "?" → +0.12 (vs +0.06 §91) ; avec "?" → +0.02

Corpus : 10 phrases × 7 types × FR/EN  +  5 phrases × 7 types × DE/ES/ZH
         = 245 phrases de test
       + 14 cas adversariaux (borderline entre paires confusibles)

Output → research/nipada/falsification/nipada_lacunes_report.json
"""

from __future__ import annotations

import json
import itertools
import re
import sys
from collections import defaultdict
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

# ── Modes V6 (§87/§88/§89) ────────────────────────────────────────────────────
MODES = MODES_V6   # §90 : utilise MODES_V6 de nipada_v6
MODE_NAMES = list(MODES.keys())
LANGS = ["fr", "en", "de", "es", "zh"]

# ── Corpus 10 phrases (FR/EN) + 5 phrases (DE/ES/ZH) par type ────────────────
CORPUS: dict[str, dict[str, list[str]]] = {

    # ── description [2,5,3] = ÊTRE×RAPPORT×DIFFÉRENCE — structurel/scientifique
    "description": {
        "fr": [
            "L'eau est une molécule composée de deux atomes d'hydrogène liés à un atome d'oxygène.",
            "Un arbre se distingue d'un arbuste par un tronc unique qui s'élève à plus d'un mètre.",
            "La lumière visible est un rayonnement électromagnétique de longueur d'onde entre 380 et 780 nm.",
            "Un prédateur est un organisme qui capture et ingère d'autres organismes pour se nourrir.",
            "Le cerveau humain est un organe d'environ 1,3 kg constitué d'environ 86 milliards de neurones.",
            "Un triangle équilatéral possède trois côtés égaux et trois angles de 60 degrés chacun.",
            "L'ADN est une macromolécule en double hélice dont les brins portent les instructions génétiques.",
            "Paris est traversée par la Seine et divisée en vingt arrondissements numérotés en spirale.",
            "Un algorithme est une séquence finie d'opérations élémentaires résolvant un problème donné.",
            "La gravitation attire les masses l'une vers l'autre en proportion de leur produit.",
        ],
        "en": [
            "Water is a molecule composed of two hydrogen atoms covalently bonded to one oxygen atom.",
            "A tree differs from a shrub by having a single trunk rising more than one meter above ground.",
            "Visible light is electromagnetic radiation with wavelengths ranging from 380 to 780 nanometers.",
            "A predator is an organism that captures and consumes other organisms for sustenance.",
            "The human brain weighs about 1.3 kg and contains approximately 86 billion neurons.",
            "An equilateral triangle has three equal sides and three angles of 60 degrees each.",
            "DNA is a double-helix macromolecule whose strands carry the genetic instructions for living organisms.",
            "Paris is divided into twenty arrondissements arranged in a spiral pattern.",
            "An algorithm is a finite sequence of elementary operations designed to solve a specific problem.",
            "Gravity attracts masses toward each other in proportion to their product.",
        ],
        "de": [
            "Wasser ist ein Molekül aus zwei Wasserstoffatomen, die kovalent an ein Sauerstoffatom gebunden sind.",
            "Ein Baum unterscheidet sich von einem Strauch durch einen Stamm, der mehr als einen Meter aufragt.",
            "Sichtbares Licht ist elektromagnetische Strahlung mit Wellenlängen zwischen 380 und 780 Nanometern.",
            "Ein Raubtier ist ein Organismus, der andere Organismen einfängt und frisst, um sich zu ernähren.",
            "Das menschliche Gehirn ist ein Organ von etwa 1,3 kg mit rund 86 Milliarden Neuronen.",
        ],
        "es": [
            "El agua es una molécula formada por dos átomos de hidrógeno enlazados a un átomo de oxígeno.",
            "Un árbol se distingue de un arbusto por poseer un tronco único que se eleva más de un metro.",
            "La luz visible es una radiación electromagnética con longitudes de onda entre 380 y 780 nm.",
            "Un depredador es un organismo que captura y consume a otros organismos para alimentarse.",
            "El cerebro humano pesa unos 1,3 kg y está formado por aproximadamente 86 000 millones de neuronas.",
        ],
        "zh": [
            "水是由两个氢原子与一个氧原子通过共价键连接而成的分子。",
            "乔木与灌木的区别在于前者拥有一根高于一米的单一主干。",
            "可见光是波长在380至780纳米之间的电磁辐射。",
            "捕食者是捕获并消费其他生物以维持生存的生物体。",
            "人类大脑约重1.3公斤，由约860亿个神经元组成。",
        ],
    },

    # ── définition [385,66] = SENS×IDENTITÉ — philosophique/sémantique
    "définition": {
        "fr": [
            "La liberté est la faculté de se donner sa propre loi sans la subir comme une contrainte extérieure.",
            "La justice est la disposition constante et perpétuelle à rendre à chacun ce qui lui revient.",
            "L'amour est la reconnaissance de l'autre comme une fin en soi, jamais réductible à un moyen.",
            "Le temps est la mesure du mouvement selon l'avant et l'après, selon la formulation d'Aristote.",
            "La conscience est la présence d'un sujet à lui-même dans l'acte même de connaître ou de percevoir.",
            "Une hypothèse est une proposition provisoire posée pour rendre compte de faits observés.",
            "La beauté est ce qui provoque un plaisir immédiat, universel et désintéressé dans la contemplation.",
            "Le droit est l'ensemble des règles qui organisent la vie en société, garanties par la contrainte publique.",
            "L'identité personnelle est ce qui fait qu'un être reste lui-même à travers le changement du temps.",
            "La vérité est l'adéquation entre ce qu'un énoncé affirme et l'état de fait qu'il prétend décrire.",
        ],
        "en": [
            "Freedom is the capacity to give oneself one's own law without experiencing it as external constraint.",
            "Justice is the constant and perpetual disposition to give each person what is due to them.",
            "Love is the recognition of another as an end in themselves, never reducible to a mere means.",
            "Time is the measure of movement according to before and after, as Aristotle formulated it.",
            "Consciousness is the presence of a subject to itself in the very act of knowing or perceiving.",
            "A hypothesis is a provisional proposition advanced to account for observed facts.",
            "Beauty is what provokes an immediate, universal and disinterested pleasure in contemplation.",
            "Law is the ensemble of rules organizing social life, guaranteed by public coercion.",
            "Personal identity is what makes a being remain itself through the changes of time.",
            "Truth is the correspondence between what a proposition asserts and the state of affairs it describes.",
        ],
        "de": [
            "Freiheit ist die Fähigkeit, sich selbst ein Gesetz zu geben, ohne es als äußeren Zwang zu erleben.",
            "Gerechtigkeit ist die beständige Bereitschaft, jedem das zu geben, was ihm zusteht.",
            "Liebe ist die Anerkennung des anderen als Zweck an sich selbst, nie als bloßes Mittel.",
            "Zeit ist das Maß der Bewegung nach Vorher und Nachher, wie Aristoteles es formuliert hat.",
            "Bewusstsein ist die Anwesenheit eines Subjekts bei sich selbst im Akt des Erkennens.",
        ],
        "es": [
            "La libertad es la facultad de darse a uno mismo su propia ley sin experimentarla como coacción externa.",
            "La justicia es la disposición constante y perpetua de dar a cada uno lo que le corresponde.",
            "El amor es el reconocimiento del otro como fin en sí mismo, nunca reducible a un simple medio.",
            "El tiempo es la medida del movimiento según el antes y el después, según Aristóteles.",
            "La conciencia es la presencia de un sujeto a sí mismo en el acto de conocer o percibir.",
        ],
        "zh": [
            "自由是在不将其体验为外部强制的情况下，自我立法的能力。",
            "正义是持续不断地给予每个人其应得之物的意愿。",
            "爱是将他人视为目的本身而非仅仅作为手段的承认。",
            "时间是按照前后顺序衡量运动的尺度，正如亚里士多德所表述的那样。",
            "意识是主体在认识或感知的行为本身中向自身的在场。",
        ],
    },

    # ── proclamation [33,55,77] = NORME×DROIT×LIBERTÉ — déclaratoire/normatif
    "proclamation": {
        "fr": [
            "Tout être humain possède une dignité inaliénable qu'aucune condition ne peut lui retirer.",
            "La liberté de conscience est un droit fondamental que nul pouvoir ne peut légitimement révoquer.",
            "Nul ne peut être réduit au rang d'instrument sans que sa propre fin soit ignorée.",
            "L'égalité des droits entre tous les humains est une norme dont la validité ne souffre aucune exception.",
            "Tout sujet a le droit de défendre sa liberté contre quiconque cherche à l'en priver par la force.",
            "La protection de la vie est une obligation qui s'impose à toute organisation politique légitime.",
            "Aucune loi ne peut être juste si elle n'est pas fondée sur le respect inconditionnel de la personne.",
            "La torture est inconditionnellement interdite, quelles que soient les circonstances invoquées.",
            "Les droits fondamentaux s'appliquent à chaque personne en raison de son humanité, non de sa citoyenneté.",
            "La liberté d'expression ne peut être limitée que pour protéger les droits d'autrui, jamais pour protéger le pouvoir.",
        ],
        "en": [
            "Every human being possesses an inalienable dignity that no condition can strip away.",
            "Freedom of conscience is a fundamental right that no authority can legitimately revoke.",
            "No person can be reduced to an instrument without their own ends being disregarded.",
            "The equality of rights among all human beings is a norm that admits of no exception.",
            "Every subject has the right to defend their freedom against anyone who seeks to deprive them of it.",
            "The protection of life is an obligation binding every political organization claiming legitimacy.",
            "No law can be just if it is not grounded in unconditional respect for the person.",
            "Torture is unconditionally prohibited, regardless of the circumstances invoked to justify it.",
            "Fundamental rights apply to each person by virtue of their humanity, not their citizenship.",
            "Freedom of expression may only be limited to protect the rights of others, never to protect power.",
        ],
        "de": [
            "Jeder Mensch besitzt eine unveräußerliche Würde, die ihm durch keine Bedingung entzogen werden kann.",
            "Gewissensfreiheit ist ein Grundrecht, das keine Macht rechtmäßig widerrufen kann.",
            "Niemand kann auf den Rang eines Instruments reduziert werden, ohne dass sein Zweck missachtet wird.",
            "Die Gleichheit der Rechte aller Menschen ist eine Norm, die keine Ausnahme duldet.",
            "Jedes Subjekt hat das Recht, seine Freiheit gegen jeden zu verteidigen, der versucht, sie zu nehmen.",
        ],
        "es": [
            "Todo ser humano posee una dignidad inalienable que ninguna condición puede arrebatarle.",
            "La libertad de conciencia es un derecho fundamental que ningún poder puede legítimamente revocar.",
            "Nadie puede ser reducido a la condición de instrumento sin que se ignore su propio fin.",
            "La igualdad de derechos entre todos los seres humanos es una norma que no admite excepción alguna.",
            "Todo sujeto tiene el derecho de defender su libertad frente a quienes traten de privársela.",
        ],
        "zh": [
            "每个人都拥有任何条件都无法剥夺的不可让渡的尊严。",
            "良心自由是任何权力都不能合法地撤销的基本权利。",
            "没有人可以被降格为工具，而其自身目的却被忽视。",
            "所有人平等权利是一项不允许任何例外的规范。",
            "每个主体都有权捍卫自己的自由，反对任何试图以武力剥夺其自由的人。",
        ],
    },

    # ── question [165,11] = JUGEMENT×SUJET — interrogatif/évaluatif
    "question": {
        "fr": [
            "Qu'est-ce qui distingue un acte moralement bon d'un acte simplement conforme à la règle ?",
            "Comment la conscience peut-elle être à la fois sujet et objet dans l'acte de réflexion ?",
            "Existe-t-il des vérités que nul sujet fini ne pourra jamais atteindre par ses propres moyens ?",
            "Pourquoi y a-t-il quelque chose plutôt que rien, et à quel titre peut-on poser cette question ?",
            "Est-il possible de vouloir librement ce que l'on a été formé à désirer depuis l'enfance ?",
            "Quelle frontière sépare une obéissance légitime d'une soumission qui trahit sa propre dignité ?",
            "Comment distinguer une conviction sincère d'un préjugé si ancré qu'il se prend pour une évidence ?",
            "Un être peut-il vraiment choisir son identité, ou est-il toujours déjà déterminé par ce qu'il est ?",
            "Que reste-t-il de la liberté quand les conditions matérielles de son exercice ont été supprimées ?",
            "À quoi reconnaît-on qu'un argument est valide indépendamment de la vérité de ses prémisses ?",
        ],
        "en": [
            "What distinguishes a morally good act from one that merely conforms to the rule?",
            "How can consciousness be both subject and object in the act of self-reflection?",
            "Are there truths that no finite subject can ever reach through their own means?",
            "Why is there something rather than nothing, and on what grounds can this question be asked?",
            "Is it possible to freely will what one has been formed to desire since childhood?",
            "What separates legitimate obedience from submission that betrays one's own dignity?",
            "How does one distinguish a sincere conviction from a prejudice that passes for self-evidence?",
            "Can a being truly choose their own identity, or are they always already determined by what they are?",
            "What remains of freedom when the material conditions for its exercise have been eliminated?",
            "How do we recognize that an argument is valid regardless of the truth of its premises?",
        ],
        "de": [
            "Was unterscheidet eine moralisch gute Handlung von einer, die bloß der Regel entspricht?",
            "Wie kann Bewusstsein im Akt der Reflexion zugleich Subjekt und Objekt sein?",
            "Gibt es Wahrheiten, die kein endliches Subjekt jemals mit eigenen Mitteln erreichen kann?",
            "Warum gibt es überhaupt etwas und nicht vielmehr nichts?",
            "Ist es möglich, das frei zu wollen, wozu man seit der Kindheit geformt wurde?",
        ],
        "es": [
            "¿Qué distingue un acto moralmente bueno de uno que simplemente sigue la regla?",
            "¿Cómo puede la conciencia ser a la vez sujeto y objeto en el acto de reflexión?",
            "¿Existen verdades que ningún sujeto finito podrá alcanzar jamás por sus propios medios?",
            "¿Por qué hay algo en lugar de nada, y con qué fundamento puede plantearse esta pregunta?",
            "¿Es posible querer libremente lo que uno ha sido formado para desear desde la infancia?",
        ],
        "zh": [
            "道德上的善举与仅仅符合规则的行为有何区别？",
            "意识如何能在反思行为中同时成为主体和客体？",
            "是否存在任何有限主体永远无法通过自身手段达到的真理？",
            "为何有某物而非虚无，又凭何能够提出这个问题？",
            "一个人是否有可能自由地想要自幼被塑造成想要的东西？",
        ],
    },

    # ── ordre [154,231] = PROJET×RÉSISTANCE — directif/impératif
    "ordre": {
        "fr": [
            "Formule la règle de ton action de sorte qu'elle puisse valoir comme loi universelle pour tous.",
            "N'utilise jamais autrui comme un simple moyen sans tenir compte de sa propre fin en soi.",
            "Engage-toi dans la voie que tu as choisie et refuse de te laisser détourner par les obstacles.",
            "Agis de telle façon que les conséquences de tes actes soient compatibles avec la permanence de la vie.",
            "Prends en charge la responsabilité de ta propre direction sans la déléguer entièrement à autrui.",
            "Résiste à toute injonction qui te demanderait de trahir la fin que tu t'es librement assignée.",
            "Accomplis ce à quoi tu t'es engagé, même si les circonstances ont changé depuis ta décision.",
            "Oriente ton action selon une fin que tu pourrais défendre devant ceux qu'elle affecte.",
            "Ne renonce pas à ta direction propre sous prétexte que la résistance te semble trop difficile.",
            "Maintiens le cap fixé en intégrant les résistances comme des épreuves de ta résolution.",
        ],
        "en": [
            "Formulate the rule of your action so that it could serve as a universal law for everyone.",
            "Never treat another merely as a means without also considering their own end in itself.",
            "Commit to the path you have chosen and refuse to be deflected by obstacles.",
            "Act in such a way that the consequences of your actions are compatible with the permanence of life.",
            "Take responsibility for your own direction without delegating it entirely to others.",
            "Resist any injunction that would ask you to betray the end you have freely assigned yourself.",
            "Fulfill what you have committed to, even if circumstances have changed since your decision.",
            "Orient your action according to an end you could defend before those it affects.",
            "Do not abandon your own direction on the pretext that resistance seems too difficult.",
            "Maintain the course you have set by integrating resistances as trials of your resolve.",
        ],
        "de": [
            "Formuliere die Maxime deiner Handlung so, dass sie als allgemeines Gesetz gelten könnte.",
            "Benutze niemanden als bloßes Mittel, ohne seinen Zweck an sich selbst zu berücksichtigen.",
            "Verpflichte dich zu dem Weg, den du gewählt hast, und lass dich nicht ablenken.",
            "Handle so, dass die Folgen deiner Handlungen mit dem Fortbestand des Lebens vereinbar sind.",
            "Übernimm Verantwortung für deine eigene Richtung, ohne sie vollständig an andere abzugeben.",
        ],
        "es": [
            "Formula la máxima de tu acción de modo que pueda valer como ley universal para todos.",
            "Nunca trates a nadie como un mero medio sin tener en cuenta su propio fin en sí mismo.",
            "Comprométete con el camino que has elegido y niégate a dejarte desviar por los obstáculos.",
            "Actúa de tal manera que las consecuencias de tus actos sean compatibles con la permanencia de la vida.",
            "Hazte cargo de la responsabilidad de tu propia dirección sin delegarla completamente en otros.",
        ],
        "zh": [
            "将你的行动准则表述为可以成为所有人的普遍法则。",
            "永远不要仅仅将他人作为手段，而不考虑其自身的目的。",
            "致力于你所选择的道路，拒绝被障碍所偏离。",
            "以你的行动后果与生命的持续性相容的方式行事。",
            "承担起自己方向的责任，而不将其完全委托给他人。",
        ],
    },

    # ── narration [462,1155] = RÉCIT×MÉMOIRE — temporel/séquentiel
    "narration": {
        "fr": [
            "Socrate fut condamné à mort par 500 jurés athéniens et but la ciguë en 399 avant notre ère.",
            "L'écriture cunéiforme est apparue en Mésopotamie vers 3400 avant notre ère, d'abord comme outil comptable.",
            "La Révolution française a traversé successivement la phase constitutionnelle, la Terreur et le Directoire.",
            "Einstein publia la relativité restreinte en 1905 alors qu'il était encore employé à l'office des brevets.",
            "Le langage articulé s'est progressivement développé entre 200 000 et 50 000 ans avant notre ère.",
            "Darwin consacra vingt ans à rassembler des preuves avant de publier L'Origine des espèces en 1859.",
            "La démocratie athénienne dura de Clisthène en 508 jusqu'à la conquête macédonienne en 338 avant notre ère.",
            "Le mur de Berlin, érigé en une nuit en août 1961, s'est effondré le 9 novembre 1989.",
            "Les premières civilisations urbaines sont apparues dans les plaines du Tigre et de l'Euphrate vers 3500 avant notre ère.",
            "La Seconde Guerre mondiale commença avec l'invasion de la Pologne en septembre 1939 et se termina en mai 1945.",
        ],
        "en": [
            "Socrates was sentenced to death by 500 Athenian jurors and drank hemlock in 399 BCE.",
            "Cuneiform writing appeared in Mesopotamia around 3400 BCE, initially as an accounting tool.",
            "The French Revolution passed successively through its constitutional phase, the Terror and the Directory.",
            "Einstein published special relativity in 1905 while still employed at the Bern patent office.",
            "Articulate language gradually developed between 200,000 and 50,000 years before our era.",
            "Darwin spent twenty years gathering evidence before publishing On the Origin of Species in 1859.",
            "Athenian democracy lasted from Cleisthenes in 508 BCE until the Macedonian conquest in 338 BCE.",
            "The Berlin Wall, erected in a single night in August 1961, collapsed on November 9, 1989.",
            "The first urban civilizations appeared in the alluvial plains of the Tigris and Euphrates around 3500 BCE.",
            "The Second World War began with the invasion of Poland in September 1939 and ended in Europe in May 1945.",
        ],
        "de": [
            "Sokrates wurde von 500 athenischen Geschworenen zum Tode verurteilt und trank 399 v. Chr. den Schierlingsbecher.",
            "Die Keilschrift entstand um 3400 v. Chr. in Mesopotamien zunächst als Buchführungswerkzeug.",
            "Die Französische Revolution durchlief die konstitutionelle Phase, den Terror und das Direktorium.",
            "Einstein veröffentlichte die spezielle Relativitätstheorie 1905, als er noch beim Berner Patentamt arbeitete.",
            "Darwin verbrachte zwanzig Jahre damit, Beweise zu sammeln, bevor er 1859 Die Entstehung der Arten veröffentlichte.",
        ],
        "es": [
            "Sócrates fue condenado a muerte por 500 jurados atenienses y bebió cicuta en el año 399 a. C.",
            "La escritura cuneiforme apareció en Mesopotamia hacia el 3400 a. C., inicialmente como herramienta contable.",
            "La Revolución francesa atravesó la fase constitucional, el Terror y el Directorio.",
            "Einstein publicó la relatividad especial en 1905, cuando todavía trabajaba en la Oficina de Patentes de Berna.",
            "Darwin pasó veinte años reuniendo pruebas antes de publicar El origen de las especies en 1859.",
        ],
        "zh": [
            "苏格拉底被500名雅典陪审员判处死刑，于公元前399年饮鸩而死。",
            "楔形文字约于公元前3400年出现在美索不达米亚，最初作为记账工具使用。",
            "法国大革命先后经历了立宪阶段、恐怖统治和执政府时期。",
            "爱因斯坦于1905年发表了狭义相对论，当时他仍在伯尔尼专利局任职。",
            "达尔文花了二十年收集证据，然后于1859年出版了《物种起源》。",
        ],
    },

    # ── introspection [2310,22] = CONSCIENCE×IDENTITÉ_SUJET — réflexif/auto-référentiel
    "introspection": {
        "fr": [
            "Je ne sais pas si ce que je ressens est réellement de la peur ou simplement de l'anticipation inquiète.",
            "Ce qui me semble évident aujourd'hui me paraissait obscur il y a quelques années ; je ne sais pas ce qui a changé.",
            "Mes convictions les plus profondes, je ne sais pas si elles sont vraiment miennes ou héritées sans choix.",
            "L'acte même de m'observer modifie ce que j'observe : je ne peux jamais me saisir totalement depuis l'extérieur.",
            "Il y a une contradiction entre ce que je crois vouloir et ce que révèlent réellement mes actes.",
            "Ce que je nomme 'moi' est peut-être la somme de mes habitudes plutôt qu'un sujet stable et unifié.",
            "Je ne suis pas certain de savoir ce que je veux, et cette incertitude elle-même semble révélatrice.",
            "En revenant sur mes décisions passées, je ne reconnais pas toujours les raisons que je m'en donnais alors.",
            "Il y a en moi une résistance à certaines vérités que je comprends pourtant intellectuellement.",
            "Je suis à la fois celui qui agit et celui qui s'observe agir, sans que ces deux pôles coïncident jamais.",
        ],
        "en": [
            "I don't know whether what I feel is real fear or merely anxious anticipation.",
            "What seems obvious to me today seemed obscure a few years ago; I don't know what has changed.",
            "My deepest convictions — I don't know if they are truly mine or inherited without choice.",
            "The very act of observing myself alters what I observe: I can never grasp myself from the outside.",
            "There is a contradiction between what I believe I want and what my actions actually reveal.",
            "What I call 'me' may be the sum of my habits rather than a stable and unified subject.",
            "I am not certain what I want, and this uncertainty itself seems to reveal something important.",
            "Looking back at my past decisions, I don't always recognize the reasons I gave myself at the time.",
            "There is in me a resistance to certain truths that I nonetheless understand perfectly well.",
            "I am both the one who acts and the one who watches myself act, without these two poles ever coinciding.",
        ],
        "de": [
            "Ich weiß nicht, ob das, was ich fühle, wirklich Angst ist oder nur ängstliche Erwartung.",
            "Was mir heute selbstverständlich erscheint, schien mir vor einigen Jahren dunkel; ich weiß nicht, was sich geändert hat.",
            "Meine tiefsten Überzeugungen – ich weiß nicht, ob sie wirklich meine sind oder ohne Wahl übernommen.",
            "Der Akt des Beobachtens meiner selbst verändert das Beobachtete: Ich kann mich nie von außen erfassen.",
            "Es besteht ein Widerspruch zwischen dem, was ich zu wollen glaube, und dem, was meine Handlungen zeigen.",
        ],
        "es": [
            "No sé si lo que siento es miedo de verdad o simplemente anticipación ansiosa.",
            "Lo que hoy me parece evidente me parecía oscuro hace unos años; no sé qué ha cambiado.",
            "Mis convicciones más profundas, no sé si son realmente mías o las heredé sin elegirlas.",
            "El propio acto de observarme altera lo que observo: nunca puedo aprehenderme desde fuera.",
            "Hay una contradicción entre lo que creo querer y lo que revelan realmente mis actos.",
        ],
        "zh": [
            "我不知道自己所感受到的究竟是真正的恐惧还是仅仅是焦虑的预期。",
            "今天对我来说显而易见的事情，几年前还显得晦涩难懂；我不知道是什么改变了。",
            "我最深层的信念，我不知道它们是否真的属于我，还是我在没有选择的情况下继承的。",
            "观察自身的行为本身就改变了我所观察到的东西：我永远无法从外部把握自己。",
            "我相信自己想要的与我的行动实际揭示的之间存在矛盾。",
        ],
    },
}

# ── 14 cas adversariaux (borderline entre paires confusibles) ─────────────────
ADVERSARIAL: list[dict] = [
    # description ↔ définition
    {
        "fr": "La conscience de soi est une propriété émergente du système nerveux central.",
        "en": "Self-consciousness is an emergent property of the central nervous system.",
        "expected": "description", "confusible_with": "définition",
        "note": "description neurologique qui ressemble à une définition philosophique",
    },
    {
        "fr": "L'être humain est un animal rationnel et social.",
        "en": "The human being is a rational and social animal.",
        "expected": "définition", "confusible_with": "description",
        "note": "définition aristotélicienne qui ressemble à une description biologique",
    },
    # proclamation ↔ ordre
    {
        "fr": "La liberté est un droit : tu dois la défendre.",
        "en": "Freedom is a right: you must defend it.",
        "expected": "proclamation", "confusible_with": "ordre",
        "note": "proclamation qui inclut un impératif direct",
    },
    {
        "fr": "Agis toujours de façon à respecter la dignité de chaque personne.",
        "en": "Always act in a way that respects the dignity of every person.",
        "expected": "ordre", "confusible_with": "proclamation",
        "note": "impératif kantien formulé comme norme universelle",
    },
    # question ↔ définition
    {
        "fr": "Qu'est-ce que la liberté, sinon la capacité de se donner sa propre loi ?",
        "en": "What is freedom, if not the capacity to give oneself one's own law?",
        "expected": "question", "confusible_with": "définition",
        "note": "question rhétorique qui contient une définition",
    },
    {
        "fr": "La liberté est-elle une donnée ou une conquête ?",
        "en": "Is freedom a given or a conquest?",
        "expected": "question", "confusible_with": "définition",
        "note": "question ouverte sur la nature de la liberté",
    },
    # question ↔ introspection
    {
        "fr": "Pourquoi est-il si difficile de faire ce que l'on sait être juste ?",
        "en": "Why is it so difficult to do what one knows to be right?",
        "expected": "question", "confusible_with": "introspection",
        "note": "question qui pourrait être une introspection généralisée",
    },
    {
        "fr": "Je me demande si mes jugements sont vraiment les miens.",
        "en": "I wonder whether my judgments are truly my own.",
        "expected": "introspection", "confusible_with": "question",
        "note": "introspection à la première personne formulée comme une question intérieure",
    },
    # description ↔ proclamation
    {
        "fr": "L'être humain est fondamentalement libre.",
        "en": "The human being is fundamentally free.",
        "expected": "description", "confusible_with": "proclamation",
        "note": "énoncé descriptif mais qui résonne comme une proclamation",
    },
    {
        "fr": "Les sociétés justes sont celles qui respectent la dignité de chacun.",
        "en": "Just societies are those that respect the dignity of each person.",
        "expected": "définition", "confusible_with": "proclamation",
        "note": "définition normative indiscernable d'une proclamation",
    },
    # narration ↔ description
    {
        "fr": "Tout ce qui a un commencement a nécessairement une fin.",
        "en": "Everything that has a beginning necessarily has an end.",
        "expected": "description", "confusible_with": "narration",
        "note": "énoncé structural qui a une coloration temporelle/narrative",
    },
    {
        "fr": "En 399 avant notre ère, un homme fut condamné pour avoir posé des questions.",
        "en": "In 399 BCE, a man was condemned for asking questions.",
        "expected": "narration", "confusible_with": "question",
        "note": "narration dont le contenu central est un acte interrogatif",
    },
    # introspection ↔ description
    {
        "fr": "Sois conscient de tes propres contradictions.",
        "en": "Be aware of your own contradictions.",
        "expected": "ordre", "confusible_with": "introspection",
        "note": "ordre réflexif à la frontière avec l'introspection",
    },
    {
        "fr": "L'humanité progresse lentement vers plus de justice et de liberté.",
        "en": "Humanity slowly progresses toward more justice and freedom.",
        "expected": "narration", "confusible_with": "proclamation",
        "note": "narration évolutive qui ressemble à une proclamation normative",
    },
]


# ── §91 — Pré-filtre syntaxique ─────────────────────────────────────────────
# Bonus additif sur le score cosinus pour les modes dont un marqueur syntaxique
# est détecté dans la phrase source. Calibré pour combler l'écart empirique
# entre QUESTION et ORDRE (~0.08-0.11 dans §90).

SYNTACTIC_BONUS = {
    "question":         0.12,  # bonus si marqueur interrogatif présent
    "introspection_1p": 0.12,  # §92 : bonus 1re pers. SANS "?" (introspectif pur)
    "introspection_wq": 0.02,  # §92 : bonus 1re pers. AVEC "?" (auto-interrogatif)
    "définition":       0.10,  # §92 : bonus si copule définitoire (est la/le/l'/ce qui)
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
_Q_WH_ZH = re.compile(r'[吗呢为什么怎么是否如何]')

# Marqueurs 1re personne (introspection)
_I_1P = re.compile(
    r'\b(je |j\'|i |ich |yo |我|mich\b|mir\b|myself\b|me\b)',
    re.IGNORECASE)

# §92 — Copule définitoire (article défini après est/is/ist/es)
# Distingue les définitions ("est la faculté", "is the capacity")
# des descriptions ("est une molécule") et proclamations ("est garanti")
_DEF_COPULA_FR = re.compile(r"\best\s+(la\b|le\b|l'|ce\s+qui\b|ce\s+que\b)", re.IGNORECASE)
_DEF_COPULA_EN = re.compile(r'\bis\s+(the\b|what\b|that\s+which\b)', re.IGNORECASE)
_DEF_COPULA_DE = re.compile(r'\bist\s+(die\b|der\b|das\b|das,?\s+was\b)', re.IGNORECASE)
_DEF_COPULA_ES = re.compile(r'\bes\s+(la\b|el\b|lo\s+que\b)', re.IGNORECASE)
_DEF_COPULA_ZH = re.compile(r'是.*的|指的是|意味着|被定义为')


def _has_question_marker(text: str) -> bool:
    return bool(
        _Q_MARK.search(text)
        or _Q_WH_FR.search(text)
        or _Q_WH_EN.search(text)
        or _Q_WH_DE.search(text)
        or _Q_WH_ZH.search(text)
    )


def _has_introspection_marker(text: str) -> bool:
    return bool(_I_1P.search(text))


def _has_definition_marker(text: str) -> bool:
    """§92 — Détecte une copule définitoire (article défini après être/to be)."""
    return bool(
        _DEF_COPULA_FR.search(text)
        or _DEF_COPULA_EN.search(text)
        or _DEF_COPULA_DE.search(text)
        or _DEF_COPULA_ES.search(text)
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
    """§92 — Classification cosinus + bonus syntaxique (définition + introspection affinée).

    §91 : question +0.12 si "?" / mot-wh initial
    §92 : introspection +0.12 si 1re pers. SANS "?"  (introspectif pur)
                        +0.02 si 1re pers. AVEC "?"  (auto-interrogatif → laisser gagner question)
          définition   +0.10 si copule définitoire (est la/le/l'/ce qui — article défini)
    """
    sims = {m: cosine(emb, c) for m, c in centroids.items()}
    has_q  = _has_question_marker(text)
    has_1p = _has_introspection_marker(text)
    if has_q:
        sims["question"] = sims["question"] + SYNTACTIC_BONUS["question"]
        if has_1p:
            # 1re pers. + "?" : auto-interrogatif → petit bonus introspection
            sims["introspection"] = sims["introspection"] + SYNTACTIC_BONUS["introspection_wq"]
    elif has_1p:
        # 1re pers. sans "?" : introspectif pur → bonus fort
        sims["introspection"] = sims["introspection"] + SYNTACTIC_BONUS["introspection_1p"]
    if _has_definition_marker(text):
        sims["définition"] = sims["définition"] + SYNTACTIC_BONUS["définition"]
    return max(sims, key=sims.__getitem__), sims


def main() -> None:
    W = 74
    print("═" * W)
    print("  §92 — Copule définitoire (DÉFINITION) + introspection 1p/wq affinée")
    print(f"  245 phrases × 7 types × 5 langues  +  14 cas adversariaux")
    print("═" * W)

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    synth = NipadaV6Synthesizer()   # §90 : V6

    # ── 1. Centroïdes nipada par mode ─────────────────────────────────────────
    print("\n  [1] Calcul des centroïdes nipada…")
    centroids: dict[str, np.ndarray] = {}
    nipada_texts: dict[str, dict[str, str]] = {}
    for mode_name, mol_ids in MODES.items():
        vecs = []
        nipada_texts[mode_name] = {}
        for lang in LANGS:
            t = synth.synthesize(mol_ids, lang)
            nipada_texts[mode_name][lang] = t
            vecs.append(model.encode(t, show_progress_bar=False))
        centroids[mode_name] = np.mean(vecs, axis=0)

    # ── 2. Classification du corpus ───────────────────────────────────────────
    print("  [2] Classification des 245 phrases…\n")

    # confusion_counts[expected][detected] = count
    confusion_counts: dict[str, dict[str, int]] = {
        m: {n: 0 for n in MODE_NAMES} for m in MODE_NAMES
    }
    # alignment_scores[expected] = list of cosine(sentence, centroid_of_expected)
    alignment_scores: dict[str, list[float]] = {m: [] for m in MODE_NAMES}
    # total sentences per type
    type_total: dict[str, int] = {m: 0 for m in MODE_NAMES}
    # per_lang accuracy
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
                    "type": expected_type,
                    "lang": lang,
                    "idx": idx,
                    "sentence": sent,
                    "detected": detected,
                    "correct": detected == expected_type,
                    "align_to_expected": float(align),
                    "sims": {k: float(v) for k, v in sims.items()},
                })

    # ── 3. Métriques agrégées ─────────────────────────────────────────────────
    # Per-type accuracy
    type_accuracy: dict[str, float] = {
        m: confusion_counts[m][m] / type_total[m] if type_total[m] > 0 else 0.0
        for m in MODE_NAMES
    }
    global_correct = sum(r["correct"] for r in per_sentence_results)
    global_total = len(per_sentence_results)
    global_accuracy = global_correct / global_total if global_total > 0 else 0.0

    # Per-type alignment
    type_alignment: dict[str, float] = {
        m: float(np.mean(alignment_scores[m])) if alignment_scores[m] else 0.0
        for m in MODE_NAMES
    }

    # ── 4. Affichage matrice de confusion ─────────────────────────────────────
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

    # ── 5. Accuracy + alignment par type ─────────────────────────────────────
    print()
    print("─" * W)
    print("  PHASE 2 — Accuracy + alignement par type")
    print("─" * W)
    print(f"  {'type':<15s}  {'accuracy':>9}  {'alignment':>9}  {'n':>5}  top_error")
    print("  " + "─" * (W - 2))
    for m in MODE_NAMES:
        # top confusion target (other than self)
        errs = {det: confusion_counts[m][det] for det in MODE_NAMES if det != m}
        top_err = max(errs, key=errs.__getitem__) if errs else "—"
        top_err_n = errs.get(top_err, 0)
        top_err_str = f"{top_err}({top_err_n})" if top_err_n > 0 else "—"
        acc_icon = "✓" if type_accuracy[m] >= 0.5 else "✗"
        print(f"  {m:<15s}  {type_accuracy[m]:>8.1%}{acc_icon}  "
              f"{type_alignment[m]:>9.3f}  {type_total[m]:>5d}  → {top_err_str}")

    print()
    print(f"  GLOBAL accuracy : {global_accuracy:.1%}  ({global_correct}/{global_total})")

    # ── 6. Accuracy par langue ────────────────────────────────────────────────
    print()
    print("─" * W)
    print("  PHASE 3 — Accuracy par langue")
    print("─" * W)
    for lang in LANGS:
        acc = lang_correct[lang] / lang_total[lang] if lang_total[lang] > 0 else 0.0
        print(f"  {lang}  {acc:.1%}  ({lang_correct[lang]}/{lang_total[lang]})")

    # ── 7. Cas adversariaux ───────────────────────────────────────────────────
    print()
    print("─" * W)
    print("  PHASE 4 — Cas adversariaux (14 phrases borderline)")
    print("─" * W)
    adversarial_results: list[dict] = []
    for case in ADVERSARIAL:
        # Test FR (primary)
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

    # ── 8. Synthèse des lacunes ───────────────────────────────────────────────
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

    # ── 9. Sauvegarde JSON ────────────────────────────────────────────────────
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "benchmark": "§92 copule définitoire + introspection 1p/wq — DÉFINITION +0.10, INTROSPECTION 1p +0.12",
        "model": "paraphrase-multilingual-MiniLM-L12-v2",
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
