# Créé par BRAS Arthur, le 31/03/2026 en Python 3.7
# Créé par BRAS Arthur, le 30/03/2026 en Python 3.7
# Créé par BRAS Arthur, le 30/03/2026 en Python 3.7
"""
LA COURSE DU PETIT-DEJEUNER - VERSION ENDLESS
Mode infini style Subway Surfers : plus le temps passe, plus c'est rapide !
Chaque aliment est dessine en illustration 2D reconnaissable.

Controles: FLECHES GAUCHE/DROITE ou A/D
Sources : ANSES, Sante Publique France, PNNS
"""

import pygame
import random
import math
import sys

pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

LARGEUR, HAUTEUR = 1200, 800
FPS = 60

BLANC      = (255, 255, 255)
NOIR       = (0, 0, 0)
BLEU_CIEL  = (135, 206, 250)
BLEU_FONCE = (25, 25, 112)
VERT       = (46, 204, 113)
VERT_FLUO  = (0, 255, 0)
ROUGE      = (231, 76, 60)
ROUGE_FLUO = (255, 0, 0)
OR         = (255, 215, 0)
JAUNE      = (255, 235, 59)
ORANGE     = (255, 152, 0)
VIOLET     = (155, 89, 182)
GRIS       = (189, 195, 199)
ROSE_PASS  = (255,  60, 200)
BLEU_PASS  = ( 40, 120, 255)
VIOLET_PASS= (120,  40, 220)

# =============================================================================
# PASS ROYAL - 20 paliers
# =============================================================================
PASS_TIERS = [
    {"tier":  1, "xp_cumul":     0, "free": ("pieces",  50),            "premium": ("pieces",  150)},
    {"tier":  2, "xp_cumul":   250, "free": ("boite", "boite_normale"), "premium": ("pieces",  200)},
    {"tier":  3, "xp_cumul":   600, "free": ("pieces", 100),            "premium": ("skin", "cosmos")},
    {"tier":  4, "xp_cumul":  1050, "free": ("pieces", 125),            "premium": ("boite", "grande_boite")},
    {"tier":  5, "xp_cumul":  1600, "free": ("skin", "cosmos"),         "premium": ("pieces",  400)},
    {"tier":  6, "xp_cumul":  2250, "free": ("boite", "boite_normale"), "premium": ("pieces",  450)},
    {"tier":  7, "xp_cumul":  3000, "free": ("pieces", 175),            "premium": ("boite", "grande_boite")},
    {"tier":  8, "xp_cumul":  3850, "free": ("pieces", 200),            "premium": ("skin", "plasma")},
    {"tier":  9, "xp_cumul":  4800, "free": ("boite", "grande_boite"),  "premium": ("pieces",  600)},
    {"tier": 10, "xp_cumul":  5900, "free": ("pieces", 250),            "premium": ("boite", "mega_boite")},
    {"tier": 11, "xp_cumul":  7100, "free": ("boite", "boite_normale"), "premium": ("pieces",  750)},
    {"tier": 12, "xp_cumul":  8400, "free": ("pieces", 300),            "premium": ("boite", "grande_boite")},
    {"tier": 13, "xp_cumul":  9800, "free": ("pieces", 325),            "premium": ("skin", "lava")},
    {"tier": 14, "xp_cumul": 11300, "free": ("boite", "grande_boite"),  "premium": ("pieces",  900)},
    {"tier": 15, "xp_cumul": 12900, "free": ("pieces", 375),            "premium": ("boite", "mega_boite")},
    {"tier": 16, "xp_cumul": 14600, "free": ("boite", "boite_normale"), "premium": ("pieces", 1000)},
    {"tier": 17, "xp_cumul": 16400, "free": ("pieces", 425),            "premium": ("boite", "mega_boite")},
    {"tier": 18, "xp_cumul": 18300, "free": ("boite", "grande_boite"),  "premium": ("pieces", 1100)},
    {"tier": 19, "xp_cumul": 20300, "free": ("pieces", 500),            "premium": ("boite", "mega_boite")},
    {"tier": 20, "xp_cumul": 22500, "free": ("boite", "mega_boite"),    "premium": ("skin", "roi")},
]
PASS_PRIX_PREMIUM = 1200   # coût en pièces pour débloquer la voie royale
XP_MAX_TOTAL = 22500       # XP pour finir le pass

# =============================================================================
# STICKERS - Catalogue de stickers personnalisables pour le bol
# =============================================================================
STICKERS_CATALOGUE = [
    {"id": "etoile",    "nom": "Etoile",     "prix": 0,   "desc": "Classique"},
    {"id": "coeur",     "nom": "Coeur",      "prix": 80,  "desc": "Plein d'amour"},
    {"id": "flamme",    "nom": "Flamme",     "prix": 120, "desc": "On fire !"},
    {"id": "eclair",    "nom": "Eclair",     "prix": 100, "desc": "Super rapide"},
    {"id": "couronne",  "nom": "Couronne",   "prix": 200, "desc": "Sois le roi"},
    {"id": "flocon",    "nom": "Flocon",     "prix": 150, "desc": "Givre et glace"},
    {"id": "diamant",   "nom": "Diamant",    "prix": 250, "desc": "Precieux"},
    {"id": "lune",      "nom": "Lune",       "prix": 130, "desc": "Nuit etoilee"},
    {"id": "arc",       "nom": "Arc-en-ciel","prix": 180, "desc": "Couleurs !"},
    {"id": "nuage",     "nom": "Nuage",      "prix": 90,  "desc": "Planer"},
]
MAX_SLOTS_STICKERS = 3   # nombre d'emplacements sur le bol

# =============================================================================
# BOITES DE RECOMPENSES - Système style Brawl Stars
# =============================================================================
# Chaque entrée de contenu : (type, valeur, poids)
#   type    : "pieces" | "xp" | "sticker" | "bol"
#   valeur  : nombre pour pieces/xp, None pour sticker/bol (tirage aléatoire)
#   poids   : poids relatif de probabilité
BOITES_CATALOGUE = [
    {
        "id":      "boite_normale",
        "nom":     "Boite",
        "emoji":   "[N]",
        "couleur": (60, 130, 220),          # bleu
        "bord":    (120, 180, 255),
        "prix":    80,
        "desc":    "Recompenses de base",
        "contenu": [
            ("pieces",  50,  35),
            ("pieces", 100,  25),
            ("pieces", 150,  15),
            ("xp",      25,  15),
            ("xp",      50,   7),
            ("sticker", None, 3),
        ],
    },
    {
        "id":      "grande_boite",
        "nom":     "Grande Boite",
        "emoji":   "[G]",
        "couleur": (130, 60, 200),          # violet
        "bord":    (200, 140, 255),
        "prix":    220,
        "desc":    "Meilleures chances !",
        "contenu": [
            ("pieces", 150,  25),
            ("pieces", 300,  20),
            ("pieces", 500,  10),
            ("xp",      75,  18),
            ("xp",     150,  12),
            ("sticker", None,10),
            ("bol",    None,  5),
        ],
    },
    {
        "id":      "mega_boite",
        "nom":     "Mega Boite",
        "emoji":   "[M]",
        "couleur": (200, 155, 0),           # or
        "bord":    (255, 220, 60),
        "prix":    600,
        "desc":    "Le maximum !",
        "contenu": [
            ("pieces", 400,  20),
            ("pieces", 700,  15),
            ("pieces",1000,  10),
            ("xp",     200,  18),
            ("xp",     400,  12),
            ("sticker", None,12),
            ("bol",    None, 13),
        ],
    },
]


def _nom_recompense(reward):
    """Retourne le texte lisible d'une récompense de pass."""
    if reward[0] == "pieces":
        return f"{reward[1]} pieces"
    if reward[0] == "boite":
        noms = {"boite_normale": "Boite", "grande_boite": "Grande Boite", "mega_boite": "Mega Boite"}
        return noms.get(reward[1], reward[1])
    skins_noms = {"cosmos": "Bol Cosmos", "plasma": "Bol Plasma",
                  "lava": "Bol Lava", "roi": "Bol Royal"}
    return skins_noms.get(reward[1], reward[1])


# =============================================================================


# -----------------------------------------------------------------------------
# Fonctions d'illustration 2D pour chaque aliment
# -----------------------------------------------------------------------------

def dessiner_oeuf(ecran, x, y, taille=40):
    """Oeuf au plat - rendu cartoon realiste"""
    import math as _math
    t = taille

    # Ombre portee
    pygame.draw.ellipse(ecran, (180, 180, 170),
                        (x - t + 8, y + t // 2 - 2, (t - 6) * 2, 10))

    # Blanc d'oeuf - forme irreguliere via polygone arrondi
    nb = 60
    pts_blanc = []
    for i in range(nb):
        angle = _math.pi * 2 * i / nb
        # forme elliptique de base avec quelques bosses irregulieres
        rx = (t - 4) * (1 + 0.12 * _math.cos(angle * 3 + 0.5))
        ry = (t // 2 - 2) * (1 + 0.08 * _math.sin(angle * 2 + 1.0))
        px = x + _math.cos(angle) * rx
        py = (y + 6) + _math.sin(angle) * ry
        pts_blanc.append((px, py))

    pygame.draw.polygon(ecran, (255, 255, 248), pts_blanc)
    pygame.draw.polygon(ecran, (210, 210, 200), pts_blanc, 2)

    # Jaune d'oeuf (cercle bombe avec degrade simule)
    pygame.draw.circle(ecran, (200, 130, 0), (x, y - 2), t // 3 + 2)  # ombre
    pygame.draw.circle(ecran, (255, 195, 0), (x, y - 2), t // 3)
    pygame.draw.circle(ecran, (255, 215, 30), (x, y - 2), t // 3 - 3)
    pygame.draw.circle(ecran, (255, 230, 60), (x - 2, y - 4), t // 4)
    pygame.draw.circle(ecran, (255, 140, 0), (x, y - 2), t // 3, 2)

    # Reflets sur le jaune
    pygame.draw.circle(ecran, (255, 252, 180), (x - 5, y - 7), 5)
    pygame.draw.circle(ecran, (255, 255, 220), (x - 4, y - 6), 2)

def dessiner_yaourt(ecran, x, y, taille=40):
    """Pot de yaourt - style cartoon soigne"""
    t = taille

    # Ombre portee
    pygame.draw.ellipse(ecran, (160, 160, 180),
                        (x - t + 14, y + t // 2 + 2, (t - 10) * 2, 10))

    # Corps du pot (trapeze arrondi, blanc nacre)
    pts = [
        (x - t + 10, y + t // 2),
        (x + t - 10, y + t // 2),
        (x + t - 18, y - t // 2 + 4),
        (x - t + 18, y - t // 2 + 4),
    ]
    pygame.draw.polygon(ecran, (240, 242, 248), pts)
    # Cote gauche (volume)
    pygame.draw.polygon(ecran, (210, 215, 230), [
        pts[3], pts[0],
        (pts[0][0] + 6, pts[0][1]),
        (pts[3][0] + 6, pts[3][1]),
    ])
    pygame.draw.polygon(ecran, (170, 175, 200), pts, 3)

    # Couvercle aluminium (avec reflets)
    lid_rect = (x - t + 14, y - t // 2 - 7, (t - 14) * 2, 12)
    pygame.draw.rect(ecran, (195, 200, 220), lid_rect, border_radius=4)
    pygame.draw.rect(ecran, (230, 235, 250), (lid_rect[0] + 4, lid_rect[1] + 2, lid_rect[2] - 8, 4), border_radius=2)
    pygame.draw.rect(ecran, (140, 145, 170), lid_rect, 2, border_radius=4)

    # Etiquette coloree (bleu ciel degrade)
    etiq_rect = (x - t + 20, y - t // 4 + 2, (t - 18) * 2, t // 2 - 2)
    pygame.draw.rect(ecran, (80, 165, 245), etiq_rect, border_radius=4)
    pygame.draw.rect(ecran, (120, 195, 255), (etiq_rect[0] + 3, etiq_rect[1] + 3, etiq_rect[2] - 6, etiq_rect[3] // 3), border_radius=3)
    pygame.draw.rect(ecran, (40, 120, 200), etiq_rect, 2, border_radius=4)

    # Texte "YAO" bien centre
    f = pygame.font.Font(None, 20)
    t_txt = f.render("YAO", True, BLANC)
    ecran.blit(t_txt, (x - t_txt.get_width() // 2, y - t // 8 + 2))

def dessiner_pomme(ecran, x, y, taille=40):
    """Pomme rouge - cercle simple avec queue et feuille"""
    r = taille - 4

    # Ombre portee
    pygame.draw.ellipse(ecran, (140, 15, 15),
                        (x - r + 4, y + r - 8, (r - 2) * 2, 12))

    # Corps : cercle rouge
    pygame.draw.circle(ecran, (200, 30, 30), (x, y), r)
    pygame.draw.circle(ecran, (230, 50, 50), (x, y), r - 4)

    # Reflet
    pygame.draw.ellipse(ecran, (255, 130, 130),
                        (x - r // 2, y - r // 2, r // 2, r // 3))

    # Contour
    pygame.draw.circle(ecran, (120, 0, 0), (x, y), r, 3)

    # Tige
    pygame.draw.line(ecran, (100, 55, 10), (x + 2, y - r + 4), (x + 5, y - r - 12), 4)
    pygame.draw.line(ecran, (140, 80, 20), (x + 2, y - r + 4), (x + 5, y - r - 12), 2)

    # Feuille
    fx, fy = x + 5, y - r - 10
    feuille = [
        (fx,      fy),
        (fx + 8,  fy - 8),
        (fx + 18, fy - 9),
        (fx + 14, fy + 2),
        (fx + 4,  fy + 5),
    ]
    pygame.draw.polygon(ecran, (50, 155, 35), feuille)
    pygame.draw.polygon(ecran, (25, 100, 15), feuille, 2)
    pygame.draw.line(ecran, (35, 120, 20), (fx, fy), (fx + 14, fy + 2), 1)

def dessiner_pain_complet(ecran, x, y, taille=40):
    """Pain complet style cartoon - forme de miche ovale avec entailles"""
    t = taille
    # Ombre portee
    pygame.draw.ellipse(ecran, (160, 100, 30),
                        (x - t + 6, y - t//2 + 8, t*2 - 4, t - 4))
    # Corps principal du pain (ovale allonge)
    pygame.draw.ellipse(ecran, (220, 155, 70),
                        (x - t + 2, y - t//2, t*2 - 4, t))
    # Dessus plus clair (volume)
    pygame.draw.ellipse(ecran, (240, 185, 100),
                        (x - t + 10, y - t//2 + 4, t*2 - 20, t//2 - 2))
    # Contour marron fonce
    pygame.draw.ellipse(ecran, (140, 80, 25),
                        (x - t + 2, y - t//2, t*2 - 4, t), 3)

    # Entailles caracteristiques du pain (3 coups de lame)
    for i, (ex, ey, ew, eh, ang) in enumerate([
        (-16,  -t//2+18, 14, 8, -25),
        (  0,  -t//2+16, 14, 8, -20),
        ( 16,  -t//2+18, 14, 8, -25),
    ]):
        surf = pygame.Surface((ew+4, eh+4), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (170, 110, 45), (0, 0, ew, eh))
        pygame.draw.ellipse(surf, (120, 70, 20), (0, 0, ew, eh), 2)
        rot = pygame.transform.rotate(surf, ang)
        ecran.blit(rot, (x + ex - rot.get_width()//2,
                         y + ey - rot.get_height()//2))

def dessiner_amandes(ecran, x, y, taille=40):
    """Amandes style image - 3 grosses amandes brunes avec stries"""
    t = taille

    def amande(ax, ay, larg, haut, angle_deg, avec_chair=False):
        surf = pygame.Surface((larg+8, haut+8), pygame.SRCALPHA)
        # Corps
        couleur = (200, 130, 60) if not avec_chair else (235, 215, 175)
        pygame.draw.ellipse(surf, couleur, (4, 4, larg, haut))
        if not avec_chair:
            # stries de texture
            for k in range(4):
                sy = 4 + haut//5 + k * haut//5
                pygame.draw.line(surf, (160, 95, 35),
                                 (6, sy), (larg+2, sy), 1)
            # reflet
            pygame.draw.ellipse(surf, (230, 165, 90),
                                (8, 6, larg//2, haut//3))
        pygame.draw.ellipse(surf, (120, 65, 20), (4, 4, larg, haut), 2)
        rot = pygame.transform.rotate(surf, angle_deg)
        ecran.blit(rot, (ax - rot.get_width()//2, ay - rot.get_height()//2))

    # Amande arriere gauche
    amande(x - 14, y - 10, 38, 22, 15)
    # Amande arriere droite
    amande(x + 14, y - 8,  38, 22, -10)
    # Amande cassee devant (chair visible)
    amande(x,      y + 10, 30, 18,  5, avec_chair=True)

def dessiner_kiwi(ecran, x, y, taille=40):
    """Demi-kiwi tranche - rendu detaille"""
    import math as _math
    r = taille // 2

    # Ombre portee
    pygame.draw.ellipse(ecran, (50, 35, 15),
                        (x - r - 2, y + r - 4, (r + 2) * 2, 10))

    # Peau exterieure (anneau brun epais)
    pygame.draw.circle(ecran, (95, 65, 30), (x, y), r + 5)
    pygame.draw.circle(ecran, (120, 85, 40), (x, y), r + 3)

    # Chair verte (remplissage principal)
    pygame.draw.circle(ecran, (85, 165, 50), (x, y), r)
    # Zone centrale plus claire
    pygame.draw.circle(ecran, (120, 195, 70), (x, y), int(r * 0.75))
    # Zone jaunatre autour du coeur
    pygame.draw.circle(ecran, (195, 215, 90), (x, y), int(r * 0.38))

    # Coeur blanc ivoire
    pygame.draw.circle(ecran, (245, 242, 215), (x, y), int(r * 0.22))
    pygame.draw.circle(ecran, (255, 252, 230), (x, y), int(r * 0.14))

    # Pepins noirs (8 triangles pointus vers le centre)
    for i in range(8):
        angle = i * _math.pi / 4 - _math.pi / 8
        dist = r * 0.55
        px = x + _math.cos(angle) * dist
        py = y + _math.sin(angle) * dist
        # Triangle pointu
        perp = angle + _math.pi / 2
        pts_graine = [
            (px + _math.cos(angle) * 6, py + _math.sin(angle) * 6),
            (px + _math.cos(perp) * 3.5, py + _math.sin(perp) * 3.5),
            (px - _math.cos(perp) * 3.5, py - _math.sin(perp) * 3.5),
        ]
        pygame.draw.polygon(ecran, (25, 20, 10), pts_graine)
        pygame.draw.polygon(ecran, (60, 50, 30), pts_graine, 1)

    # Lignes de chair (nervures radiales fines)
    for i in range(8):
        angle = i * _math.pi / 4
        pygame.draw.line(ecran, (70, 145, 40),
                         (int(x + _math.cos(angle) * r * 0.24),
                          int(y + _math.sin(angle) * r * 0.24)),
                         (int(x + _math.cos(angle) * r * 0.90),
                          int(y + _math.sin(angle) * r * 0.90)), 1)

    # Contour de la peau
    pygame.draw.circle(ecran, (60, 40, 15), (x, y), r + 5, 3)

def dessiner_bonbons(ecran, x, y, taille=40):
    """Bonbon emballe style 'candy wrapper' - rose/magenta reconnaissable"""
    import math as _math
    t = taille

    # Ombre portee
    pygame.draw.ellipse(ecran, (120, 0, 80),
                        (x - t + 10, y + t // 3, (t - 8) * 2, 12))

    # Corps central du bonbon (ellipse principale)
    cw, ch = int(t * 1.4), int(t * 1.0)
    # Degrade simule (plusieurs ellipses emboitees)
    degrande = [
        (0,       (180,  0, 120)),
        (4,       (210, 20, 150)),
        (8,       (240, 50, 180)),
        (13,      (255, 80, 200)),
        (17,      (255,110, 215)),
    ]
    for shrink, col in degrande:
        pygame.draw.ellipse(ecran, col,
                            (x - cw // 2 + shrink, y - ch // 2 + shrink,
                             cw - shrink * 2, ch - shrink * 2))

    # Reflet brillant (haut gauche)
    pygame.draw.ellipse(ecran, (255, 180, 230),
                        (x - cw // 2 + 10, y - ch // 2 + 8,
                         cw // 3, ch // 3))
    # Petit eclat blanc
    pygame.draw.ellipse(ecran, (255, 240, 250),
                        (x - cw // 2 + 12, y - ch // 2 + 10,
                         cw // 6, ch // 6))

    # Contour du corps
    pygame.draw.ellipse(ecran, (140, 0, 90),
                        (x - cw // 2, y - ch // 2, cw, ch), 3)

    # -- Torsades a gauche --------------------------------------------------
    # Fan de triangles magenta qui partent vers la gauche
    twist_x = x - cw // 2
    twist_y = y
    nb_rayons = 5
    ecart_angle = 22  # degres entre chaque rayon
    longueur = int(t * 0.55)
    largeur_base = 8
    for i in range(nb_rayons):
        angle_deg = -((nb_rayons - 1) / 2 * ecart_angle) + i * ecart_angle
        angle_rad = _math.radians(180 + angle_deg)
        tip_x = twist_x + _math.cos(angle_rad) * longueur
        tip_y = twist_y + _math.sin(angle_rad) * longueur
        perp_x = -_math.sin(angle_rad) * (largeur_base - i * 1.2)
        perp_y =  _math.cos(angle_rad) * (largeur_base - i * 1.2)
        tri = [
            (twist_x + perp_x, twist_y + perp_y),
            (twist_x - perp_x, twist_y - perp_y),
            (tip_x, tip_y),
        ]
        # Couleur alternee pour l'effet torsade
        col_t = (200, 0, 130) if i % 2 == 0 else (240, 60, 170)
        pygame.draw.polygon(ecran, col_t, tri)
        pygame.draw.polygon(ecran, (120, 0, 80), tri, 1)

    # -- Torsades a droite -------------------------------------------------
    twist_x2 = x + cw // 2
    for i in range(nb_rayons):
        angle_deg = -((nb_rayons - 1) / 2 * ecart_angle) + i * ecart_angle
        angle_rad = _math.radians(0 + angle_deg)
        tip_x = twist_x2 + _math.cos(angle_rad) * longueur
        tip_y = twist_y  + _math.sin(angle_rad) * longueur
        perp_x = -_math.sin(angle_rad) * (largeur_base - i * 1.2)
        perp_y  =  _math.cos(angle_rad) * (largeur_base - i * 1.2)
        tri = [
            (twist_x2 + perp_x, twist_y + perp_y),
            (twist_x2 - perp_x, twist_y - perp_y),
            (tip_x, tip_y),
        ]
        col_t = (200, 0, 130) if i % 2 == 0 else (240, 60, 170)
        pygame.draw.polygon(ecran, col_t, tri)
        pygame.draw.polygon(ecran, (120, 0, 80), tri, 1)

    # Lignes de texture sur le corps (stries diagonales)
    for k in range(3):
        sx = x - cw // 2 + 18 + k * 14
        pygame.draw.line(ecran, (255, 140, 210),
                         (sx, y - ch // 2 + 6),
                         (sx - 10, y + ch // 2 - 6), 2)

def dessiner_biscuit(ecran, x, y, taille=40):
    """Cookie aux pepites de chocolat - rendu cartoon realiste"""
    import math as _math
    t = taille
    r = t - 2

    # Ombre portee
    pygame.draw.ellipse(ecran, (120, 70, 20),
                        (x - r + 6, y + r - 6, (r - 4) * 2, 12))

    # Corps du cookie - polygone legerement irregulier (pas parfaitement rond)
    nb = 40
    pts = []
    for i in range(nb):
        angle = _math.pi * 2 * i / nb
        wobble = 1.0 + 0.07 * _math.sin(angle * 7 + 0.8) + 0.04 * _math.cos(angle * 3)
        px = x + _math.cos(angle) * r * wobble
        py = y + _math.sin(angle) * r * wobble
        pts.append((px, py))

    # Couches de couleur (bord dore fonce, centre beige dore)
    pygame.draw.polygon(ecran, (165, 105, 35), pts)  # bord
    # Corps interieur
    pts_inner = []
    for (px, py) in pts:
        dx, dy = px - x, py - y
        pts_inner.append((x + dx * 0.82, y + dy * 0.82))
    pygame.draw.polygon(ecran, (215, 158, 72), pts_inner)
    # Coeur plus clair
    pts_center = []
    for (px, py) in pts:
        dx, dy = px - x, py - y
        pts_center.append((x + dx * 0.60, y + dy * 0.60))
    pygame.draw.polygon(ecran, (235, 185, 100), pts_center)

    # Contour
    pygame.draw.polygon(ecran, (120, 75, 20), pts, 3)

    # Pepites de chocolat - reparties regulierement sur 2 anneaux
    # Anneau exterieur : 6 pepites
    for i in range(6):
        angle = math.pi * 2 * i / 6 + math.pi / 6
        dist = r * 0.62
        px = int(x + math.cos(angle) * dist)
        py = int(y + math.sin(angle) * dist)
        ang_rot = int(angle * 57) % 40 - 20
        pw, ph = 11, 7
        surf = pygame.Surface((pw + 4, ph + 4), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (55, 28, 8), (0, 0, pw, ph))
        pygame.draw.ellipse(surf, (35, 15, 3), (0, 0, pw, ph), 1)
        rot = pygame.transform.rotate(surf, ang_rot)
        ecran.blit(rot, (px - rot.get_width() // 2, py - rot.get_height() // 2))
    # Anneau interieur : 3 pepites
    for i in range(3):
        angle = math.pi * 2 * i / 3
        dist = r * 0.30
        px = int(x + math.cos(angle) * dist)
        py = int(y + math.sin(angle) * dist)
        ang_rot = int(angle * 57) % 30 - 15
        pw, ph = 10, 6
        surf = pygame.Surface((pw + 4, ph + 4), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (55, 28, 8), (0, 0, pw, ph))
        pygame.draw.ellipse(surf, (35, 15, 3), (0, 0, pw, ph), 1)
        rot = pygame.transform.rotate(surf, ang_rot)
        ecran.blit(rot, (px - rot.get_width() // 2, py - rot.get_height() // 2))

def dessiner_soda(ecran, x, y, taille=40):
    """Canette de soda - rendu cartoon brillant"""
    t = taille
    cw, ch = t - 4, t * 2

    # Ombre portee
    pygame.draw.ellipse(ecran, (160, 30, 30),
                        (x - cw // 2 + 6, y + ch // 2 + 2, cw - 4, 10))

    # Corps de la canette (rouge vif avec degrade simule)
    pygame.draw.rect(ecran, (190, 25, 25),
                     (x - cw // 2, y - ch // 2, cw, ch), border_radius=10)
    pygame.draw.rect(ecran, (230, 45, 45),
                     (x - cw // 2 + 3, y - ch // 2, cw - 6, ch), border_radius=10)
    # Bande centrale decorative (blanche)
    pygame.draw.rect(ecran, (255, 255, 255),
                     (x - cw // 2 + 4, y - 10, cw - 8, 20))
    pygame.draw.rect(ecran, (240, 50, 50),
                     (x - cw // 2 + 4, y - 6, cw - 8, 12))

    # Reflet vertical gauche (brillance)
    pygame.draw.rect(ecran, (255, 110, 110),
                     (x - cw // 2 + 5, y - ch // 2 + 12, 7, ch - 24),
                     border_radius=4)
    pygame.draw.rect(ecran, (255, 180, 180),
                     (x - cw // 2 + 6, y - ch // 2 + 14, 3, ch - 28),
                     border_radius=3)

    # Dessus de la canette (ellipse metallique)
    pygame.draw.ellipse(ecran, (160, 160, 175),
                        (x - cw // 2 - 2, y - ch // 2 - 8, cw + 4, 18))
    pygame.draw.ellipse(ecran, (210, 215, 225),
                        (x - cw // 2, y - ch // 2 - 6, cw, 14))
    pygame.draw.ellipse(ecran, (170, 175, 190),
                        (x - cw // 2, y - ch // 2 - 6, cw, 14), 2)

    # Bas de la canette
    pygame.draw.ellipse(ecran, (150, 25, 25),
                        (x - cw // 2, y + ch // 2 - 8, cw, 14))
    pygame.draw.ellipse(ecran, (170, 30, 30),
                        (x - cw // 2 + 2, y + ch // 2 - 6, cw - 4, 10))

    # Languette d'ouverture
    pygame.draw.ellipse(ecran, (130, 135, 150),
                        (x - 8, y - ch // 2 - 4, 16, 8))
    pygame.draw.line(ecran, (140, 145, 160),
                     (x, y - ch // 2 - 2), (x + 10, y - ch // 2 + 5), 3)
    pygame.draw.circle(ecran, (120, 125, 140), (x + 10, y - ch // 2 + 5), 4)
    pygame.draw.circle(ecran, (180, 185, 200), (x + 10, y - ch // 2 + 5), 4, 1)

    # Bulles deco
    for i, (bx, by, br) in enumerate([(-6, -22, 3), (6, -8, 4), (0, 10, 3)]):
        pygame.draw.circle(ecran, (255, 200, 200), (x + bx, y + by), br)
        pygame.draw.circle(ecran, (255, 255, 255), (x + bx - 1, y + by - 1), 1)

    # Texte "SODA"
    f = pygame.font.Font(None, 19)
    t_txt = f.render("SODA", True, BLANC)
    ecran.blit(t_txt, (x - t_txt.get_width() // 2, y - 8))

    # Contour general
    pygame.draw.rect(ecran, (120, 15, 15),
                     (x - cw // 2, y - ch // 2, cw, ch), 3, border_radius=10)


# Dictionnaire des fonctions de dessin par nom
DESSIN_ALIMENT = {
    "Oeuf":       dessiner_oeuf,
    "Yaourt":     dessiner_yaourt,
    "Pomme":      dessiner_pomme,
    "Pain complet": dessiner_pain_complet,
    "Amandes":    dessiner_amandes,
    "Kiwi":       dessiner_kiwi,
    "Bonbons":    dessiner_bonbons,
    "Biscuit":    dessiner_biscuit,
    "Soda":       dessiner_soda,
}


# -----------------------------------------------------------------------------
# Classe AlimentTombant - avec illustration 2D
# -----------------------------------------------------------------------------

class AlimentTombant:
    def __init__(self, nom, points_energie, points_sante, vitesse_base):
        self.nom = nom
        self.points_energie = points_energie
        self.points_sante   = points_sante
        self.taille = 40

        self.x = random.randint(80, LARGEUR - 80)
        self.y = -100
        self.vitesse = vitesse_base + random.uniform(-0.4, 0.4)
        self.angle_drift = random.uniform(0, 360)

        self.est_bon = points_energie > 0
        self.fn_dessin = DESSIN_ALIMENT.get(nom)

    def update(self):
        self.y += self.vitesse
        self.x += math.sin(self.y / 60) * 0.4

    def dessiner(self, ecran, fonte_nom):
        x, y = int(self.x), int(self.y)
        temps = pygame.time.get_ticks()

        # Halo clignotant - disque semi-transparent + anneaux epais
        allume = (temps // 180) % 2 == 0
        if allume:
            couleur_vive  = (0, 255, 0)   if self.est_bon else (255, 0, 0)
            couleur_douce = (60, 255, 60)  if self.est_bon else (255, 60, 60)
            r_halo = self.taille + 20
            # Disque teinte semi-transparent
            surf_halo = pygame.Surface((r_halo * 2 + 4, r_halo * 2 + 4), pygame.SRCALPHA)
            if self.est_bon:
                pygame.draw.circle(surf_halo, (0, 220, 0, 60),
                                   (r_halo + 2, r_halo + 2), r_halo)
            else:
                pygame.draw.circle(surf_halo, (255, 0, 0, 60),
                                   (r_halo + 2, r_halo + 2), r_halo)
            ecran.blit(surf_halo, (x - r_halo - 2, y - r_halo - 2))
            # Anneau epais exterieur
            pygame.draw.circle(ecran, couleur_vive,  (x, y), r_halo, 7)
            # Anneau interieur fin
            pygame.draw.circle(ecran, couleur_douce, (x, y), self.taille + 8, 3)

        # Illustration 2D
        if self.fn_dessin:
            self.fn_dessin(ecran, x, y, self.taille)
        else:
            pygame.draw.circle(ecran, GRIS, (x, y), self.taille//2)

        # Nom sous l'aliment
        couleur_fond_nom = (0, 130, 0) if self.est_bon else (170, 0, 0)
        couleur_bord_nom = VERT_FLUO if self.est_bon else ROUGE_FLUO
        txt = fonte_nom.render(self.nom, True, BLANC)
        rect = txt.get_rect(center=(x, y + self.taille + 18))
        fond = pygame.Rect(rect.x-8, rect.y-4, rect.width+16, rect.height+8)
        pygame.draw.rect(ecran, couleur_fond_nom, fond, border_radius=6)
        pygame.draw.rect(ecran, couleur_bord_nom, fond, 3, border_radius=6)
        ecran.blit(txt, rect)

    def est_hors_ecran(self):
        return self.y > HAUTEUR + 120




# -----------------------------------------------------------------------------
# Power-ups
# -----------------------------------------------------------------------------

class PowerUp:
    TYPES = {
        "bouclier": {"couleur": (80, 160, 255),  "label": "BOUCLIER",  "icone": "B"},
        "slowmo":   {"couleur": (180, 80, 255),  "label": "SLOW-MO",   "icone": "S"},
        "aimant":   {"couleur": (255, 215, 0),   "label": "AIMANT",    "icone": "A"},
    }

    def __init__(self, type_, vitesse):
        self.type_   = type_
        info         = self.TYPES[type_]
        self.couleur = info["couleur"]
        self.label   = info["label"]
        self.icone   = info["icone"]
        self.x       = random.randint(90, LARGEUR - 90)
        self.y       = -80
        self.vitesse = vitesse * 0.7   # plus lent que les aliments
        self.rayon   = 32
        self.angle   = 0

    def update(self):
        self.y     += self.vitesse
        self.angle += 3

    def est_hors_ecran(self):
        return self.y > HAUTEUR + 100

    def dessiner(self, ecran):
        x, y = int(self.x), int(self.y)
        t = pygame.time.get_ticks()

        # Halo pulsant
        pulse = 0.5 + 0.5 * math.sin(t / 200)
        r_halo = int(self.rayon + 10 + 6 * pulse)
        surf_h = pygame.Surface((r_halo*2+4, r_halo*2+4), pygame.SRCALPHA)
        pygame.draw.circle(surf_h, (*self.couleur, 70), (r_halo+2, r_halo+2), r_halo)
        ecran.blit(surf_h, (x - r_halo - 2, y - r_halo - 2))

        # Etoile a 6 branches tournante
        for i in range(6):
            a = math.radians(self.angle + i * 60)
            x2 = x + math.cos(a) * self.rayon
            y2 = y + math.sin(a) * self.rayon
            pygame.draw.line(ecran, self.couleur, (x, y), (int(x2), int(y2)), 4)

        # Cercle central
        pygame.draw.circle(ecran, BLANC,        (x, y), self.rayon - 6)
        pygame.draw.circle(ecran, self.couleur, (x, y), self.rayon - 6, 4)

        # Icone
        f = pygame.font.Font(None, 36)
        txt = f.render(self.icone, True, self.couleur)
        ecran.blit(txt, txt.get_rect(center=(x, y)))

        # Label
        f2  = pygame.font.Font(None, 22)
        lab = f2.render(self.label, True, BLANC)
        r   = lab.get_rect(center=(x, y + self.rayon + 16))
        fond = pygame.Rect(r.x-6, r.y-3, r.width+12, r.height+6)
        pygame.draw.rect(ecran, self.couleur, fond, border_radius=5)
        pygame.draw.rect(ecran, BLANC, fond, 2, border_radius=5)
        ecran.blit(lab, r)

# -----------------------------------------------------------------------------
# Bol du joueur
# -----------------------------------------------------------------------------

class Bol:
    SKINS = {
        # ---------- Bols stylises ----------
        "celeste":  {"couleur": ( 20,  70, 170), "nom": "Bol Celeste",   "prix": 0,   "forme": "classic",   "sticker": "celeste"},
        "jade":     {"couleur": ( 30, 130,  55), "nom": "Bol Jade",      "prix": 180, "forme": "classic",   "sticker": "jade"},
        "aztec":    {"couleur": (185,  30,  30), "nom": "Bol Azteque",   "prix": 320, "forme": "classic",   "sticker": "aztec"},
        "sakura":   {"couleur": (230, 218, 208), "nom": "Bol Sakura",    "prix": 480, "forme": "classic",   "sticker": "sakura"},
        "ocean":    {"couleur": ( 10,  90, 150), "nom": "Bol Ocean",     "prix": 250, "forme": "classic",   "sticker": "ocean"},
        "soleil":   {"couleur": (210, 140,   0), "nom": "Bol Soleil",    "prix": 400, "forme": "classic",   "sticker": "soleil"},
        "imperial": {"couleur": ( 80,  10, 120), "nom": "Bol Imperial",  "prix": 550, "forme": "classic",   "sticker": "imperial"},
        "dragon":   {"couleur": ( 15,  15,  40), "nom": "Bol Dragon",    "prix": 700, "forme": "classic",   "sticker": "dragon"},
        # ---------- Skins exclusifs PASS ROYAL ----------
        "cosmos":   {"couleur": ( 60,   0, 180), "nom": "Bol Cosmos",    "prix": 0,   "forme": "classic",   "sticker": "cosmos",  "pass_only": True},
        "plasma":   {"couleur": (180,   0, 220), "nom": "Bol Plasma",    "prix": 0,   "forme": "classic",   "sticker": "plasma",  "pass_only": True},
        "lava":     {"couleur": (220,  80,   0), "nom": "Bol Lava",      "prix": 0,   "forme": "classic",   "sticker": "lava",    "pass_only": True},
        "roi":      {"couleur": (180, 140,   0), "nom": "Bol Royal",     "prix": 0,   "forme": "classic",   "sticker": "roi",     "pass_only": True},
    }

    def __init__(self, couleur_skin="celeste", largeur_bonus=0, vitesse_bonus=0):
        self.x = LARGEUR // 2
        self.y = HAUTEUR - 130
        self.largeur = 160 + largeur_bonus
        self.hauteur = 80
        self.vitesse = 10 + vitesse_bonus
        self.oscillation = 0
        self.couleur_skin = couleur_skin
        self.stickers_slots = [None, None, None]  # 3 emplacements personnalisables
        self.custom_color = None          # (r,g,b) surcharge la couleur du skin si defini
        self.skip_skin_sticker = False    # True = pas de sticker decoratif du skin

    def deplacer_gauche(self):
        self.x = max(self.largeur//2 + 30, self.x - self.vitesse)

    def deplacer_droite(self):
        self.x = min(LARGEUR - self.largeur//2 - 30, self.x + self.vitesse)

    def update(self):
        self.oscillation += 0.1

    def _dessiner_sticker_custom(self, ecran, cx, cy, r, stk_id, now_ms):
        """Dessine un sticker personnalise (petit, sur le bol)."""
        import math as _m
        pulse = 0.85 + 0.15 * _m.sin(now_ms / 500.0)
        r = int(r * pulse)

        if stk_id == "etoile":
            pts = []
            for k in range(10):
                a = _m.radians(k * 36 - 90)
                rad = r if k % 2 == 0 else r // 2
                pts.append((int(cx + _m.cos(a) * rad), int(cy + _m.sin(a) * rad)))
            pygame.draw.polygon(ecran, (255, 230, 0), pts)
            pygame.draw.polygon(ecran, (200, 160, 0), pts, 1)

        elif stk_id == "coeur":
            # Deux demi-cercles + triangle
            for dx in (-r // 2, r // 2):
                pygame.draw.circle(ecran, (255, 50, 80), (cx + dx, cy - r // 4), r // 2)
            pts_h = [
                (cx - r, cy - r // 4),
                (cx, cy + r),
                (cx + r, cy - r // 4),
            ]
            pygame.draw.polygon(ecran, (255, 50, 80), pts_h)
            pygame.draw.circle(ecran, (255, 120, 140), (cx - r // 3, cy - r // 3), r // 4)

        elif stk_id == "flamme":
            pts_f = [
                (cx,       cy - r),
                (cx + r,   cy + r // 2),
                (cx + r // 3, cy),
                (cx,       cy + r),
                (cx - r // 3, cy),
                (cx - r,   cy + r // 2),
            ]
            pygame.draw.polygon(ecran, (255, 140, 0), pts_f)
            pts_i = [
                (cx,         cy - r // 2),
                (cx + r // 2, cy + r // 2),
                (cx,          cy + r // 3),
                (cx - r // 2, cy + r // 2),
            ]
            pygame.draw.polygon(ecran, (255, 230, 50), pts_i)

        elif stk_id == "eclair":
            pts_e = [
                (cx + r // 3, cy - r),
                (cx - r // 4, cy),
                (cx + r // 3, cy),
                (cx - r // 3, cy + r),
                (cx + r // 4, cy + r // 5),
                (cx - r // 3, cy + r // 5),
            ]
            pygame.draw.polygon(ecran, (255, 255, 0), pts_e)
            pygame.draw.polygon(ecran, (200, 200, 0), pts_e, 1)

        elif stk_id == "couronne":
            base_y = cy + r // 2
            pts_c = [
                (cx - r, base_y),
                (cx - r, cy - r // 3),
                (cx - r // 2, cy + r // 4),
                (cx, cy - r),
                (cx + r // 2, cy + r // 4),
                (cx + r, cy - r // 3),
                (cx + r, base_y),
            ]
            pygame.draw.polygon(ecran, (255, 210, 0), pts_c)
            pygame.draw.polygon(ecran, (200, 150, 0), pts_c, 2)
            for gem_x in (cx - r // 2, cx, cx + r // 2):
                pygame.draw.circle(ecran, (255, 80, 80), (gem_x, base_y - r // 4), r // 5)

        elif stk_id == "flocon":
            for angle in range(0, 360, 60):
                a = _m.radians(angle)
                ex = int(cx + _m.cos(a) * r)
                ey = int(cy + _m.sin(a) * r)
                pygame.draw.line(ecran, (180, 230, 255), (cx, cy), (ex, ey), 2)
                for ba in (-30, 30):
                    ba_r = _m.radians(angle + ba)
                    bx2 = int(cx + _m.cos(a) * r * 0.55 + _m.cos(ba_r) * r * 0.35)
                    by2 = int(cy + _m.sin(a) * r * 0.55 + _m.sin(ba_r) * r * 0.35)
                    pygame.draw.line(ecran, (220, 245, 255),
                                     (int(cx + _m.cos(a) * r * 0.55),
                                      int(cy + _m.sin(a) * r * 0.55)),
                                     (bx2, by2), 1)
            pygame.draw.circle(ecran, (240, 250, 255), (cx, cy), r // 4)

        elif stk_id == "diamant":
            pts_d = [
                (cx, cy - r),
                (cx + r, cy - r // 4),
                (cx + r * 2 // 3, cy + r),
                (cx - r * 2 // 3, cy + r),
                (cx - r, cy - r // 4),
            ]
            pygame.draw.polygon(ecran, (80, 200, 255), pts_d)
            pts_top = [pts_d[0], pts_d[1], (cx, cy - r // 4), pts_d[4]]
            pygame.draw.polygon(ecran, (160, 230, 255), pts_top)
            pygame.draw.polygon(ecran, (0, 120, 200), pts_d, 2)

        elif stk_id == "lune":
            pygame.draw.circle(ecran, (255, 240, 100), (cx, cy), r)
            pygame.draw.circle(ecran, (20, 40, 80), (cx + r // 3, cy - r // 4), int(r * 0.75))

        elif stk_id == "arc":
            couleurs_arc = [(255,50,50),(255,140,0),(255,230,0),(50,200,50),(50,100,255),(150,50,220)]
            for i, coul in enumerate(couleurs_arc):
                ep = r - i * (r // len(couleurs_arc))
                if ep < 2: break
                pygame.draw.arc(ecran, coul,
                                (cx - ep, cy - ep, ep * 2, ep * 2),
                                0, _m.pi, max(2, r // len(couleurs_arc)))

        elif stk_id == "nuage":
            for dx, dy, cr in [(-r//2, r//4, r//2), (0, 0, r*2//3), (r//2, r//4, r//2), (0, r//2, r//2)]:
                pygame.draw.circle(ecran, (230, 240, 255), (cx + dx, cy + dy), cr)
            pygame.draw.circle(ecran, (255, 255, 255), (cx, cy + r // 4), r // 2)

    def _dessiner_sticker(self, ecran, cx, cy, rx, ry, sticker, coul_base, now_ms):
        """Dessine les decorations sur le corps du bol - dessins nets et soignes."""
        import math as _m

        def clamp_in_bowl(px, py):
            """Verifie qu'un point est approximativement dans l'ellipse du bol."""
            dx = (px - cx) / max(1, rx - 6)
            dy = (py - cy - ry * 0.5) / max(1, ry * 0.55)
            return dx * dx + dy * dy < 1.0

        if sticker == "celeste":
            # ---- BOL CELESTE : ciel nocturne avec lune et etoiles a 5 branches ----
            # Lune croissante a gauche
            lx, ly = cx - rx // 2 + 8, cy + ry * 55 // 100
            pygame.draw.circle(ecran, (255, 235, 100), (lx, ly), 12)
            pygame.draw.circle(ecran, (20, 70, 170),   (lx + 7, ly - 4), 10)

            # Etoiles a 5 branches nettes, positions fixes dans le bol
            star_data = [
                (cx + rx * 35 // 100, cy + ry * 30 // 100, 7),
                (cx,                  cy + ry * 60 // 100, 6),
                (cx - rx * 20 // 100, cy + ry * 45 // 100, 5),
                (cx + rx * 50 // 100, cy + ry * 65 // 100, 5),
                (cx + rx * 15 // 100, cy + ry * 80 // 100, 4),
            ]
            pulse = _m.sin(now_ms / 400.0)
            for i, (sx, sy, sr) in enumerate(star_data):
                r_out = sr + int(1.5 * _m.sin(now_ms / 350.0 + i * 1.3))
                r_in  = max(2, r_out // 2)
                pts = []
                for k in range(10):
                    a = _m.radians(k * 36 - 90)
                    r = r_out if k % 2 == 0 else r_in
                    pts.append((int(sx + _m.cos(a) * r), int(sy + _m.sin(a) * r)))
                pygame.draw.polygon(ecran, (255, 245, 130), pts)
                pygame.draw.polygon(ecran, (220, 200,  60), pts, 1)

        elif sticker == "jade":
            # ---- BOL JADE : medaillon central + bande horizontale doree ----
            # Bande horizontale doree bien droite
            band_y = cy + ry * 35 // 100
            # Calcul exact de la demi-largeur a cette hauteur sur l'ellipse
            rel = (band_y - cy - ry) / ry  # entre -1 et 0
            demi = int(rx * _m.sqrt(max(0.0, 1.0 - rel * rel)))
            marge = 14
            if demi > marge + 4:
                pygame.draw.rect(ecran, (180, 140,  10),
                                 (cx - demi + marge,     band_y - 4, (demi - marge) * 2, 8))
                pygame.draw.rect(ecran, (240, 200,  50),
                                 (cx - demi + marge + 2, band_y - 2, (demi - marge) * 2 - 4, 4))
                pygame.draw.rect(ecran, (140, 100,   5),
                                 (cx - demi + marge,     band_y - 4, (demi - marge) * 2, 8), 1)

            # Medaillon central dore avec symbole yin/yang simplifie
            mx, my = cx, cy + ry * 72 // 100
            pygame.draw.circle(ecran, (160, 115,   5), (mx, my), 15)
            pygame.draw.circle(ecran, (210, 170,  20), (mx, my), 13)
            pygame.draw.circle(ecran, (240, 205,  55), (mx, my), 10)
            # Croix interieure en relief
            pygame.draw.line(ecran, (170, 125, 10), (mx - 7, my), (mx + 7, my), 2)
            pygame.draw.line(ecran, (170, 125, 10), (mx, my - 7), (mx, my + 7), 2)
            # Contour final
            pygame.draw.circle(ecran, (130,  90,   0), (mx, my), 15, 2)

        elif sticker == "aztec":
            # ---- BOL AZTEQUE : deux rangees de chevrons dores symetriques ----
            for row, frac_y in enumerate([0.30, 0.65]):
                band_y = cy + int(ry * frac_y)
                rel    = (band_y - cy - ry) / ry
                demi   = int(rx * _m.sqrt(max(0.0, 1.0 - rel * rel)))
                marge  = 12
                w_zone = (demi - marge) * 2
                if w_zone < 20:
                    continue
                nb_chev = 7
                step    = w_zone // nb_chev
                for k in range(nb_chev):
                    ox = cx - demi + marge + k * step + step // 2
                    h  = 9
                    pts_up = [(ox - step//3, band_y + h),
                              (ox,           band_y - h),
                              (ox + step//3, band_y + h)]
                    pygame.draw.polygon(ecran, (255, 210,  40), pts_up)
                    pygame.draw.polygon(ecran, (180, 130,   0), pts_up, 1)

            # Losanges sur la bande du milieu
            mid_y = cy + ry * 50 // 100
            rel_m = (mid_y - cy - ry) / ry
            demi_m = int(rx * _m.sqrt(max(0.0, 1.0 - rel_m * rel_m)))
            for k in range(4):
                lx = cx - demi_m + 18 + k * ((demi_m - 18) * 2 // 3)
                pts_l = [(lx, mid_y - 8), (lx + 7, mid_y),
                         (lx, mid_y + 8), (lx - 7, mid_y)]
                pygame.draw.polygon(ecran, (255, 215,  50), pts_l)
                pygame.draw.polygon(ecran, (160, 110,   0), pts_l, 1)

        elif sticker == "sakura":
            # ---- BOL SAKURA : fleurs de cerisier nettes avec tige et feuilles ----
            def fleur(fx, fy, taille):
                for i in range(5):
                    a  = _m.radians(i * 72 - 90)
                    px = int(fx + _m.cos(a) * taille)
                    py = int(fy + _m.sin(a) * taille)
                    pygame.draw.circle(ecran, (235, 130, 155), (px, py), taille - 1)
                    pygame.draw.circle(ecran, (255, 175, 190), (px, py), max(1, taille - 3))
                pygame.draw.circle(ecran, (255, 215,  70), (fx, fy), max(2, taille // 2 + 1))
                pygame.draw.circle(ecran, (200, 155,   0), (fx, fy), max(2, taille // 2 + 1), 1)

            fleur_data = [
                (cx - rx * 40 // 100, cy + ry * 35 // 100, 7),
                (cx + rx * 40 // 100, cy + ry * 40 // 100, 7),
                (cx,                  cy + ry * 70 // 100, 8),
                (cx - rx * 20 // 100, cy + ry * 75 // 100, 5),
                (cx + rx * 25 // 100, cy + ry * 75 // 100, 5),
            ]
            for (fx, fy, ts) in fleur_data:
                fleur(fx, fy, ts)

            # Petits traits de tige reliant les fleurs
            pygame.draw.line(ecran, (160, 100,  60),
                             (cx - rx * 40 // 100, cy + ry * 42 // 100),
                             (cx,                  cy + ry * 62 // 100), 1)
            pygame.draw.line(ecran, (160, 100,  60),
                             (cx + rx * 40 // 100, cy + ry * 47 // 100),
                             (cx,                  cy + ry * 62 // 100), 1)

        elif sticker == "ocean":
            # ---- BOL OCEAN : vagues blanches superposees ----
            for row, frac_y in enumerate([0.30, 0.55, 0.78]):
                wy    = cy + int(ry * frac_y)
                rel   = (wy - cy - ry) / ry
                demi  = int(rx * _m.sqrt(max(0.0, 1.0 - rel * rel)))
                marge = 10
                w_zone = (demi - marge) * 2
                if w_zone < 20:
                    continue
                nb_vagues = 4
                amp = 5 - row
                pts_vague = []
                steps = 60
                for s in range(steps + 1):
                    t  = s / steps
                    wx = cx - demi + marge + int(t * w_zone)
                    wy2 = wy + int(_m.sin(t * _m.pi * 2 * nb_vagues) * amp)
                    pts_vague.append((wx, wy2))
                if len(pts_vague) >= 2:
                    pygame.draw.lines(ecran, (200, 235, 255), False, pts_vague, 3)
                    pygame.draw.lines(ecran, (255, 255, 255), False, pts_vague, 1)

            # Bulles rondes nettes
            bulles = [
                (cx - rx * 30 // 100, cy + ry * 50 // 100, 5),
                (cx + rx * 35 // 100, cy + ry * 62 // 100, 4),
                (cx + rx * 10 // 100, cy + ry * 38 // 100, 3),
            ]
            for (bx, by, br) in bulles:
                pygame.draw.circle(ecran, (180, 220, 255), (bx, by), br)
                pygame.draw.circle(ecran, (220, 245, 255), (bx - 1, by - 1), max(1, br - 2))
                pygame.draw.circle(ecran, (100, 170, 220), (bx, by), br, 1)

        elif sticker == "soleil":
            # ---- BOL SOLEIL : soleil central avec rayons alternes ----
            sx, sy = cx, cy + ry * 58 // 100
            # Rayons alternes (longs / courts)
            nb_rayons = 12
            for k in range(nb_rayons):
                a    = _m.radians(k * 360 // nb_rayons - 90)
                long = 18 if k % 2 == 0 else 11
                x1   = int(sx + _m.cos(a) * 10)
                y1   = int(sy + _m.sin(a) * 10)
                x2   = int(sx + _m.cos(a) * long)
                y2   = int(sy + _m.sin(a) * long)
                pygame.draw.line(ecran, (255, 200,  20), (x1, y1), (x2, y2), 3)
                pygame.draw.line(ecran, (200, 145,   0), (x1, y1), (x2, y2), 1)
            # Corps du soleil
            pygame.draw.circle(ecran, (200, 140,   0), (sx, sy), 10)
            pygame.draw.circle(ecran, (255, 205,  30), (sx, sy),  9)
            pygame.draw.circle(ecran, (255, 235,  80), (sx, sy),  6)
            pygame.draw.circle(ecran, (255, 250, 140), (sx - 2, sy - 2), 3)

            # Motif de points dores sur le pourtour du bol (bande)
            band_y = cy + ry * 28 // 100
            rel    = (band_y - cy - ry) / ry
            demi   = int(rx * _m.sqrt(max(0.0, 1.0 - rel * rel)))
            for k in range(8):
                dot_x = cx - demi + 14 + k * ((demi - 14) * 2 // 7)
                pygame.draw.circle(ecran, (255, 210,  40), (dot_x, band_y), 4)
                pygame.draw.circle(ecran, (170, 120,   0), (dot_x, band_y), 4, 1)

        elif sticker == "imperial":
            # ---- BOL IMPERIAL : motifs imperiaux violets/or sur fond sombre ----
            # Bande or en haut
            band_y = cy + ry * 28 // 100
            rel    = (band_y - cy - ry) / ry
            demi   = int(rx * _m.sqrt(max(0.0, 1.0 - rel * rel)))
            marge  = 10
            if demi > marge + 4:
                pygame.draw.rect(ecran, (160, 120,  10),
                                 (cx - demi + marge,     band_y - 4, (demi - marge) * 2, 8))
                pygame.draw.rect(ecran, (215, 175,  50),
                                 (cx - demi + marge + 2, band_y - 2, (demi - marge) * 2 - 4, 4))

            # Fleur imperial a 8 petales au centre
            fx, fy = cx, cy + ry * 65 // 100
            for i in range(8):
                a  = _m.radians(i * 45)
                px = int(fx + _m.cos(a) * 14)
                py = int(fy + _m.sin(a) * 14)
                pygame.draw.circle(ecran, (170,  80, 210), (px, py), 7)
                pygame.draw.circle(ecran, (200, 130, 240), (px, py), 5)
            # Cercle dore central
            pygame.draw.circle(ecran, (160, 115,  10), (fx, fy), 8)
            pygame.draw.circle(ecran, (220, 180,  50), (fx, fy), 6)
            pygame.draw.circle(ecran, (240, 210,  80), (fx - 2, fy - 2), 3)

            # Petits carres dores aux quatre coins du bol
            corner_data = [
                (cx - rx * 42 // 100, cy + ry * 40 // 100),
                (cx + rx * 42 // 100, cy + ry * 40 // 100),
                (cx - rx * 35 // 100, cy + ry * 75 // 100),
                (cx + rx * 35 // 100, cy + ry * 75 // 100),
            ]
            for (qx, qy) in corner_data:
                pygame.draw.rect(ecran, (215, 170,  40), (qx - 4, qy - 4, 8, 8))
                pygame.draw.rect(ecran, (155, 110,   5), (qx - 4, qy - 4, 8, 8), 1)

        elif sticker == "dragon":
            # ---- BOL DRAGON : ecailles stylisees + yeux de dragon rouges ----
            # Ecailles (rangees d'arcs de cercle)
            for row in range(3):
                ey    = cy + ry * (25 + row * 22) // 100
                rel   = (ey - cy - ry) / ry
                demi  = int(rx * _m.sqrt(max(0.0, 1.0 - rel * rel)))
                marge = 8
                ecaille_w = 18
                nb_ec = max(1, (demi - marge) * 2 // ecaille_w)
                total_w = nb_ec * ecaille_w
                ox_start = cx - total_w // 2
                for k in range(nb_ec):
                    ex = ox_start + k * ecaille_w + ecaille_w // 2
                    # Decalage en quinconce
                    ey2 = ey + (ecaille_w // 4 if k % 2 == 0 else 0)
                    # Demi-cercle = ecaille
                    pygame.draw.arc(ecran, ( 50, 180, 100),
                                    (ex - 9, ey2 - 9, 18, 18),
                                    0, _m.pi, 3)
                    pygame.draw.arc(ecran, ( 20, 100,  55),
                                    (ex - 9, ey2 - 9, 18, 18),
                                    0, _m.pi, 1)

            # Yeux de dragon : deux cercles rouges avec pupille en fente
            for ex, ey in [(cx - rx * 28 // 100, cy + ry * 80 // 100),
                           (cx + rx * 28 // 100, cy + ry * 80 // 100)]:
                pygame.draw.circle(ecran, (200,  20,  20), (ex, ey), 7)
                pygame.draw.circle(ecran, (255,  60,  60), (ex, ey), 5)
                # Pupille en fente verticale
                pygame.draw.line(ecran, (10, 10, 10), (ex, ey - 4), (ex, ey + 4), 2)
                pygame.draw.circle(ecran, (255, 180, 180), (ex - 2, ey - 2), 2)

        elif sticker == "cosmos":
            # ---- BOL COSMOS : spirale galactique + étoiles colorées ----
            import math as _m
            # Spirale
            pts_spiral = []
            for k in range(120):
                a = k * 0.18
                r = k * 0.35
                sx2 = cx + int(_m.cos(a) * r)
                sy2 = cy + int(ry * 0.5 + _m.sin(a) * r * 0.5)
                if abs(sx2 - cx) < rx - 8 and abs(sy2 - (cy + ry * 0.5)) < ry * 0.55:
                    pts_spiral.append((sx2, sy2))
            if len(pts_spiral) >= 2:
                pygame.draw.lines(ecran, (140, 60, 255), False, pts_spiral, 2)
                pygame.draw.lines(ecran, (180, 100, 255), False, pts_spiral[:60], 1)
            # Étoiles colorées
            star_c = [
                (cx + rx*30//100, cy + ry*30//100, (255,200,100), 4),
                (cx - rx*35//100, cy + ry*50//100, (100,200,255), 3),
                (cx + rx*10//100, cy + ry*70//100, (200,100,255), 5),
                (cx - rx*15//100, cy + ry*25//100, (255,255,150), 3),
                (cx + rx*40//100, cy + ry*65//100, (100,255,200), 3),
            ]
            for (sx3, sy3, sc, sr) in star_c:
                pts_s = []
                for k in range(10):
                    a2 = _m.radians(k * 36 - 90)
                    rr = sr if k % 2 == 0 else sr // 2
                    pts_s.append((int(sx3 + _m.cos(a2) * rr), int(sy3 + _m.sin(a2) * rr)))
                pygame.draw.polygon(ecran, sc, pts_s)

        elif sticker == "plasma":
            # ---- BOL PLASMA : arcs électriques animés ----
            import math as _m
            t_ms = now_ms / 120.0
            for arc_i in range(5):
                pts_arc = []
                base_a = _m.radians(arc_i * 72 + t_ms * 40)
                x1 = cx + int(_m.cos(base_a) * rx * 0.5)
                y1 = cy + ry//2 + int(_m.sin(base_a) * ry * 0.35)
                x2 = cx + int(_m.cos(base_a + _m.pi) * rx * 0.4)
                y2 = cy + ry//2 + int(_m.sin(base_a + _m.pi) * ry * 0.3)
                steps = 12
                for s in range(steps + 1):
                    frac = s / steps
                    mx = int(x1 + (x2 - x1) * frac)
                    my = int(y1 + (y2 - y1) * frac)
                    zigzag = int(_m.sin(frac * _m.pi * 6 + t_ms + arc_i) * 8)
                    perp_x = int(-(y2 - y1) / max(1, abs(x2-x1)+abs(y2-y1)) * zigzag)
                    perp_y = int((x2 - x1) / max(1, abs(x2-x1)+abs(y2-y1)) * zigzag)
                    pts_arc.append((mx + perp_x, my + perp_y))
                if len(pts_arc) >= 2:
                    col_p = (220, 80, 255) if arc_i % 2 == 0 else (100, 160, 255)
                    pygame.draw.lines(ecran, col_p, False, pts_arc, 2)
            # Centre lumineux
            pygame.draw.circle(ecran, (200, 80, 255), (cx, cy + ry*65//100), 8)
            pygame.draw.circle(ecran, (240, 180, 255), (cx, cy + ry*65//100), 5)
            pygame.draw.circle(ecran, (255, 240, 255), (cx, cy + ry*65//100), 2)

        elif sticker == "lava":
            # ---- BOL LAVA : bulles de lave et fissures ----
            import math as _m
            # Fissures
            fissure_pts = [
                [(cx - 10, cy + ry*25//100), (cx,      cy + ry*45//100), (cx + 8, cy + ry*60//100)],
                [(cx + 20, cy + ry*30//100), (cx + 10, cy + ry*50//100), (cx + 5, cy + ry*70//100)],
                [(cx - 25, cy + ry*40//100), (cx - 15, cy + ry*60//100), (cx - 5, cy + ry*75//100)],
            ]
            for fp in fissure_pts:
                pygame.draw.lines(ecran, (255, 150, 0), False, fp, 3)
                pygame.draw.lines(ecran, (255, 220, 0), False, fp, 1)
            # Bulles de lave
            pulse_l = 0.5 + 0.5 * _m.sin(now_ms / 300)
            bulles_lv = [
                (cx - rx*30//100, cy + ry*45//100, 8),
                (cx + rx*25//100, cy + ry*55//100, 6),
                (cx,              cy + ry*72//100, 10),
                (cx - rx*10//100, cy + ry*30//100, 5),
            ]
            for (bx2, by2, br2) in bulles_lv:
                r_b = int(br2 + 2 * pulse_l)
                pygame.draw.circle(ecran, (255, 100, 0), (bx2, by2), r_b)
                pygame.draw.circle(ecran, (255, 200, 0), (bx2, by2), max(1, r_b - 3))
                pygame.draw.circle(ecran, (255, 255, 100), (bx2 - 2, by2 - 2), max(1, r_b // 3))
                pygame.draw.circle(ecran, (200, 60, 0), (bx2, by2), r_b, 2)

        elif sticker == "roi":
            # ---- BOL ROYAL : couronne dorée et joyaux ----
            import math as _m
            # Couronne (5 pointes)
            crown_cx, crown_cy = cx, cy + ry*45//100
            crown_w, crown_h = rx * 70 // 100, ry * 45 // 100
            base_y = crown_cy + crown_h // 2
            pointe_y = crown_cy - crown_h // 2
            nb_pointes = 5
            pts_crown = []
            # Base gauche
            pts_crown.append((crown_cx - crown_w // 2, base_y))
            for k in range(nb_pointes):
                frac = k / (nb_pointes - 1)
                x_tip = crown_cx - crown_w // 2 + int(frac * crown_w)
                # Hauteur alternée
                h_k = pointe_y if k % 2 == 0 else (pointe_y + crown_h // 2)
                pts_crown.append((x_tip, h_k))
            pts_crown.append((crown_cx + crown_w // 2, base_y))
            # Fermeture en bas
            pts_crown.append((crown_cx + crown_w // 2, base_y + 10))
            pts_crown.append((crown_cx - crown_w // 2, base_y + 10))
            pygame.draw.polygon(ecran, (180, 130, 0), pts_crown)
            pygame.draw.polygon(ecran, (240, 195, 40), pts_crown, 3)
            # Joyaux sur les pointes hautes
            joyaux_cols = [(255, 50, 50), (50, 200, 255), (50, 255, 100)]
            j = 0
            for k in range(nb_pointes):
                if k % 2 == 0:
                    frac = k / (nb_pointes - 1)
                    jx = crown_cx - crown_w // 2 + int(frac * crown_w)
                    jy = pointe_y
                    col_j = joyaux_cols[j % 3]
                    j += 1
                    pygame.draw.circle(ecran, col_j, (jx, jy), 6)
                    pygame.draw.circle(ecran, (255, 255, 255), (jx - 2, jy - 2), 2)
                    pygame.draw.circle(ecran, (0, 0, 0), (jx, jy), 6, 2)

    def dessiner(self, ecran):
        import math as _m
        offset_y = _m.sin(self.oscillation) * 4
        cx = int(self.x)
        cy = int(self.y + offset_y)
        W  = self.largeur
        H  = self.hauteur
        now_ms = pygame.time.get_ticks()

        # -- Palette + forme depuis le skin ------------------------------------------
        skin_info   = self.SKINS.get(self.couleur_skin, self.SKINS["celeste"])
        coul_base   = self.custom_color if self.custom_color else skin_info["couleur"]
        forme       = skin_info.get("forme", "classic")
        sticker     = skin_info.get("sticker", None)

        COUL_EXT    = coul_base
        COUL_FONCE  = tuple(max(0, int(c * 0.65)) for c in coul_base)
        COUL_CLAIR  = tuple(min(255, int(c * 1.25 + 20)) for c in coul_base)
        BLANC_INT   = (245, 245, 242)
        GRIS_INT    = (210, 208, 205)

        # Parametres de forme
        if forme == "large":
            rx = int(W * 0.65)   # plus large
            ry = int(H * 0.65)   # plus plat
        elif forme == "profond":
            rx = int(W * 0.42)   # plus etroit
            ry = int(H * 1.25)   # plus profond
        elif forme == "carre":
            rx = int(W * 0.52)
            ry = int(H * 0.90)
        elif forme == "hexagonal":
            rx = int(W * 0.50)
            ry = int(H * 0.95)
        else:
            rx = W // 2
            ry = H

        rim_ry = max(10, ry // 5)
        base_y = cy + ry

        # -- 1. Ombre au sol ---------------------------------------------------
        pygame.draw.ellipse(ecran, (20, 20, 20),
                            (cx - rx + 14, base_y + 4, (rx - 8) * 2, 10))

        # -- 2. Corps du bol ---------------------------------------------------
        if forme == "carre":
            # Bol rectangulaire avec coins arrondis en bas
            rect_pts = [
                (cx - rx, cy),
                (cx + rx, cy),
                (cx + rx, base_y - rx // 3),
                (cx + rx - rx // 3, base_y),
                (cx - rx + rx // 3, base_y),
                (cx - rx, base_y - rx // 3),
            ]
            pygame.draw.polygon(ecran, COUL_EXT, rect_pts)
            ombre_r = [rect_pts[1], rect_pts[2], rect_pts[3], (cx, base_y), (cx, cy)]
            if len(ombre_r) >= 3:
                pygame.draw.polygon(ecran, COUL_FONCE, ombre_r)
            pygame.draw.polygon(ecran, COUL_FONCE, rect_pts, 3)
            arc_pts = rect_pts  # pour la suite

        elif forme == "hexagonal":
            # Bol hexagonal - 6 cotes
            nb_hex = 6
            hex_pts = []
            for i in range(nb_hex + 1):
                angle = _m.pi * i / nb_hex
                px = cx + _m.cos(_m.pi - angle) * rx
                py = cy + rim_ry + _m.sin(angle) * (ry - rim_ry)
                # Arrondir en segments droits
                hex_pts.append((int(px), int(py)))
            corps_hex = [(cx - rx, cy)] + hex_pts + [(cx + rx, cy)]
            # Lisser avec des angles
            nb_seg = 80
            arc_pts = []
            for i in range(nb_seg + 1):
                angle = _m.pi * i / nb_seg
                px = cx + _m.cos(_m.pi - angle) * rx * (1.0 + 0.06 * _m.cos(angle * 6))
                py = cy + rim_ry + _m.sin(angle) * (ry - rim_ry)
                arc_pts.append((int(px), int(py)))
            corps_pts = [(cx - rx, cy)] + arc_pts + [(cx + rx, cy)]
            pygame.draw.polygon(ecran, COUL_EXT, corps_pts)
            # Facettes hexagonales
            for k in range(6):
                a1 = _m.pi * k / 6
                a2 = _m.pi * (k + 1) / 6
                f_pts = [
                    (int(cx + _m.cos(_m.pi - a1) * rx), int(cy + rim_ry + _m.sin(a1) * (ry - rim_ry))),
                    (int(cx + _m.cos(_m.pi - a2) * rx), int(cy + rim_ry + _m.sin(a2) * (ry - rim_ry))),
                ]
                if k % 2 == 0 and len(f_pts) >= 2:
                    pygame.draw.line(ecran, COUL_CLAIR, f_pts[0], f_pts[1], 3)
            pygame.draw.polygon(ecran, COUL_FONCE, corps_pts, 3)

        else:
            # Forme classique / large / profond : arc arrondi
            nb = 80
            arc_pts = []
            for i in range(nb + 1):
                angle = _m.pi * i / nb
                px = cx + _m.cos(_m.pi - angle) * rx
                py = cy + rim_ry + _m.sin(angle) * (ry - rim_ry)
                arc_pts.append((int(px), int(py)))

            corps_pts = [(cx - rx, cy)] + arc_pts + [(cx + rx, cy)]
            pygame.draw.polygon(ecran, COUL_EXT, corps_pts)
            ombre_pts = arc_pts[nb // 2:] + [(cx + rx, cy)]
            if len(ombre_pts) >= 3:
                pygame.draw.polygon(ecran, COUL_FONCE, ombre_pts)
            reflet_pts = [(cx - rx, cy), (cx - rx + 10, cy)] + arc_pts[:nb // 6]
            if len(reflet_pts) >= 3:
                pygame.draw.polygon(ecran, COUL_CLAIR, reflet_pts)
            pygame.draw.polygon(ecran, COUL_FONCE, corps_pts, 3)

        # -- 3. Stickers decoratifs -------------------------------------------
        if sticker and not getattr(self, "skip_skin_sticker", False):
            self._dessiner_sticker(ecran, cx, cy, rx, ry, sticker, coul_base, now_ms)

        # -- 3b. Stickers personnalises (slots) --------------------------------
        slots_config = getattr(self, "stickers_slots", [None, None, None])
        slot_positions = [
            (cx - rx * 45 // 100, cy + ry * 55 // 100),
            (cx,                  cy + ry * 70 // 100),
            (cx + rx * 45 // 100, cy + ry * 55 // 100),
        ]
        for slot_idx, stk_id in enumerate(slots_config):
            if stk_id:
                sx, sy = slot_positions[slot_idx]
                self._dessiner_sticker_custom(ecran, sx, sy, 16, stk_id, now_ms)

        # -- 4. Interieur du bol ----------------------------------------------
        int_rx = rx - 10
        int_ry = rim_ry + 2
        sw = max(4, int_rx * 2)
        sh = max(4, int_ry * 2)
        surf_int = pygame.Surface((sw, sh), pygame.SRCALPHA)
        masque   = pygame.Surface((sw, sh), pygame.SRCALPHA)
        pygame.draw.ellipse(masque, (255, 255, 255, 255), (0, 0, sw, sh))
        pygame.draw.ellipse(surf_int, GRIS_INT  + (255,), (0, 0, sw, sh))
        pygame.draw.ellipse(surf_int, BLANC_INT + (255,), (14, 4, sw - 28, sh - 8))
        surf_int.blit(masque, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        ecran.blit(surf_int, (cx - int_rx, cy - int_ry))

        # -- 5. Rebord elliptique (moitie superieure seulement) ---------------
        old_clip = ecran.get_clip()
        ecran.set_clip(pygame.Rect(cx - rx - 4, cy - rim_ry - 4, rx * 2 + 8, rim_ry + 4))
        pygame.draw.ellipse(ecran, COUL_EXT,
                            (cx - rx, cy - rim_ry, rx * 2, rim_ry * 2), 10)
        pygame.draw.ellipse(ecran, COUL_CLAIR,
                            (cx - rx + 4, cy - rim_ry + 3, rx * 2 - 8, rim_ry * 2 - 6), 4)
        pygame.draw.ellipse(ecran, COUL_FONCE,
                            (cx - rx, cy - rim_ry, rx * 2, rim_ry * 2), 2)
        ecran.set_clip(old_clip)

        # -- 6. Fleches directionnelles ----------------------------------------
        arrow_y = cy
        pts_left = [
            (cx - rx - 45, arrow_y),
            (cx - rx - 20, arrow_y - 22),
            (cx - rx - 20, arrow_y + 22),
        ]
        pygame.draw.polygon(ecran, OR,   pts_left)
        pygame.draw.polygon(ecran, NOIR, pts_left, 3)

        pts_right = [
            (cx + rx + 45, arrow_y),
            (cx + rx + 20, arrow_y - 22),
            (cx + rx + 20, arrow_y + 22),
        ]
        pygame.draw.polygon(ecran, OR,   pts_right)
        pygame.draw.polygon(ecran, NOIR, pts_right, 3)

        # -- 7. Label "TON BOL" ------------------------------------------------
        f     = pygame.font.Font(None, 34)
        t_lbl = f.render("TON BOL", True, NOIR)
        r     = t_lbl.get_rect(center=(cx, base_y + 20))
        fond  = pygame.Rect(r.x - 10, r.y - 5, r.width + 20, r.height + 10)
        pygame.draw.rect(ecran, JAUNE, fond, border_radius=7)
        pygame.draw.rect(ecran, NOIR,  fond, 4,  border_radius=7)
        ecran.blit(t_lbl, r)

    def collision_avec(self, aliment):
        dx = aliment.x - self.x
        dy = aliment.y - self.y
        return (dx/(self.largeur/2))**2 + (dy/(self.hauteur/2))**2 <= 1.2


# -----------------------------------------------------------------------------
# Particules
# -----------------------------------------------------------------------------

class Particule:
    def __init__(self, x, y, couleur):
        self.x = x; self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, -2)
        self.couleur = couleur
        self.vie = 35
        self.taille = random.randint(4, 10)

    def update(self):
        self.x += self.vx; self.y += self.vy
        self.vy += 0.25; self.vie -= 1

    def dessiner(self, ecran):
        if self.vie > 0:
            pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)


# -----------------------------------------------------------------------------
# Jeu principal
# -----------------------------------------------------------------------------

class JeuPetitDej:

    # -- Difficulte progressive (style Subway Surfers) ----------------------
    VITESSE_DEPART    = 2.5    # vitesse douce au depart
    VITESSE_MAX       = 10.0   # plafond raisonnable
    VITESSE_INCREMENT = 0.20   # progression plus lente toutes les 10 s
    SPAWN_DEPART      = 1600   # ms entre chaque spawn au depart (plus espace)
    SPAWN_MIN         = 450    # spawn max moins frenetique
    SPAWN_INCREMENT   = 55     # reduction plus douce
    RATIO_PIEGES_DEPART = 0.0  # pas de pieges les premieres secondes
    RATIO_PIEGES_MAX    = 0.50 # maximum 50% de pieges
    RATIO_PIEGES_PALIER = 30   # pieges arrivent progressivement

    TYPES_BONS = [
        {"nom": "Oeuf",         "energie": 25, "sante": 30, "poids": 3},
        {"nom": "Yaourt",       "energie": 20, "sante": 25, "poids": 3},
        {"nom": "Pomme",        "energie": 15, "sante": 20, "poids": 3},
        {"nom": "Pain complet", "energie": 30, "sante": 25, "poids": 3},
        {"nom": "Amandes",      "energie": 20, "sante": 25, "poids": 2},
        {"nom": "Kiwi",         "energie": 15, "sante": 20, "poids": 2},
    ]
    TYPES_PIEGES = [
        {"nom": "Bonbons", "energie": -20, "sante": -25},
        {"nom": "Biscuit", "energie": -10, "sante": -15},
        {"nom": "Soda",    "energie": -20, "sante": -25},
    ]

    def __init__(self):
        self.ecran   = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("LA COURSE DU PETIT-DEJEUNER")
        self.horloge = pygame.time.Clock()

        self.fonte_titre      = pygame.font.Font(None, 65)
        self.fonte_sous_titre = pygame.font.Font(None, 38)
        self.fonte_texte      = pygame.font.Font(None, 26)
        self.fonte_score      = pygame.font.Font(None, 48)
        self.fonte_petite     = pygame.font.Font(None, 20)
        self.fonte_nom        = pygame.font.Font(None, 28)

        self.scene = "accueil"
        self.tuto_page        = 0      # page courante du tuto (0 = pas commence)
        self.premiere_partie  = True   # affiche le bouton TUTO la 1ere fois
        self._reset()

        # -- Sons ------------------------------------------------
        self._generer_sons()

        # -- Meilleur score -----------------------------------------
        self.meilleur_score = self._charger_meilleur_score()

        # -- Boutique -----------------------------------------------
        self.boutique = self._charger_boutique()
        self.tuto_boutique = 0  # onglet boutique (0=skins, 1=ameliorations)

        # -- Pass Royal ---------------------------------------------
        self.pass_page = 0           # page affichée dans l'écran pass (0-3)
        self.pass_xp_gagnee = 0      # XP gagnée lors de la dernière partie

        # -- Boites de recompenses ----------------------------------
        self._boite_etat        = "menu"   # "menu" | "shake" | "reveal"
        self._boite_ouverte_id  = None
        self._boite_recompense  = None
        self._boite_anim_debut  = 0
        self._boite_selected    = 0

        # -- Tutoriels first-time (overlay) --------------------------
        self._tuto_boutique_vu  = False
        self._tuto_boites_vu    = False
        self._tuto_pass_vu      = False
        self._tuto_perso_vu     = False

    # -- Reset -------------------------------------------------------------
    def _reset(self):
        # Appliquer upgrades depuis la boutique
        skin    = self.boutique["skin_actif"]    if hasattr(self, "boutique") else "celeste"
        lv_t    = self.boutique["taille_niveau"] if hasattr(self, "boutique") else 0
        lv_v    = self.boutique["vitesse_niveau"] if hasattr(self, "boutique") else 0
        larg_bonus = [0, 20, 40][lv_t]
        vit_bonus  = [0,  2,  4][lv_v]
        bol_mode = self.boutique.get("bol_mode", "boutique") if hasattr(self, "boutique") else "boutique"
        self.bol = Bol(couleur_skin=skin, largeur_bonus=larg_bonus, vitesse_bonus=vit_bonus)
        if bol_mode == "perso":
            # Couleur choisie + stickers perso, sans sticker decoratif du skin
            c = self.boutique.get("bol_perso_couleur", [220, 80, 80]) if hasattr(self, "boutique") else [220, 80, 80]
            self.bol.custom_color = tuple(c)
            self.bol.skip_skin_sticker = True
            self.bol.stickers_slots = list(self.boutique.get("stickers_slots", [None, None, None])) if hasattr(self, "boutique") else [None, None, None]
        else:
            # Skin boutique : couleur + sticker decoratif, sans stickers perso
            self.bol.custom_color = None
            self.bol.skip_skin_sticker = False
            self.bol.stickers_slots = [None, None, None]
        self.aliments         = []
        self.particules       = []
        self.messages         = []
        self.dernier_spawn    = 0
        self.temps_debut      = 0

        self.score_energie    = 0
        self.score_sante      = 0
        self.combo            = 0
        self.max_combo        = 0
        self.pieges_attrapes  = 0
        self.defaite_pieges   = False
        self.bons_manques     = 0
        self.defaite_manques  = False
        self.en_pause         = False
        self.temps_fin        = 0
        self.pieces_gagnees   = 0   # pieces gagnees dans cette partie
        self._pass_xp_applique = False
        self._pass_montee_niveau = False

        # Power-ups
        self.powerups           = []
        self.dernier_spawn_pu   = 0
        self.bouclier_actif     = False
        self.slowmo_fin         = 0
        self.aimant_fin         = 0

    # -- Difficulte selon temps ecoule -------------------------------------
    def _temps_ecoule(self):
        return (pygame.time.get_ticks() - self.temps_debut) / 1000

    def _vitesse_actuelle(self):
        paliers = int(self._temps_ecoule() / 10)
        return min(self.VITESSE_MAX, self.VITESSE_DEPART + paliers * self.VITESSE_INCREMENT)

    def _spawn_interval(self):
        paliers = int(self._temps_ecoule() / 10)
        return max(self.SPAWN_MIN, self.SPAWN_DEPART - paliers * self.SPAWN_INCREMENT)

    def _ratio_pieges(self):
        t = self._temps_ecoule()
        if t < 3:
            return 0.0
        ratio = (t - 3) / self.RATIO_PIEGES_PALIER * self.RATIO_PIEGES_MAX
        return min(self.RATIO_PIEGES_MAX, ratio)

    def _niveau_label(self):
        t = self._temps_ecoule()
        if t < 10:   return "DEBUTANT",  VERT
        if t < 30:   return "INTERMEDIAIRE", ORANGE
        if t < 60:   return "EXPERT",    ROUGE
        return "CHAOS !", ROUGE_FLUO

    # -- Spawn -------------------------------------------------------------
    def _spawn_aliment(self):
        if len(self.aliments) >= 14:
            return
        if random.random() < self._ratio_pieges():
            d = random.choice(self.TYPES_PIEGES)
            a = AlimentTombant(d["nom"], d["energie"], d["sante"], self._vitesse_actuelle())
        else:
            poids_total = sum(t["poids"] for t in self.TYPES_BONS)
            choix = random.uniform(0, poids_total)
            cumul = 0
            for t in self.TYPES_BONS:
                cumul += t["poids"]
                if choix <= cumul:
                    a = AlimentTombant(t["nom"], t["energie"], t["sante"], self._vitesse_actuelle())
                    break
        self.aliments.append(a)

    def _spawn_powerup(self):
        types = ["bouclier", "slowmo", "aimant"]
        # Ne pas spawner bouclier si deja actif
        if self.bouclier_actif:
            types = ["slowmo", "aimant"]
        t = random.choice(types)
        self.powerups.append(PowerUp(t, self._vitesse_actuelle()))

    # -- Helpers -----------------------------------------------------------
    def _ajouter_message(self, texte, couleur, taille=40):
        self.messages.append({"texte": texte, "couleur": couleur,
                               "y": float(HAUTEUR//2 - 100), "vie": 70, "taille": taille})

    def _creer_particules(self, x, y, couleur, n=25):
        for _ in range(n):
            self.particules.append(Particule(x, y, couleur))

    # -- Sons ------------------------------------------------------------------------------------
    def _generer_son(self, freq, duree_ms, volume=0.5):
        import math as _m
        sr = 44100
        n  = int(sr * duree_ms / 1000)
        buf = bytearray(n * 2)
        for i in range(n):
            fade = min(1.0, (n - i) / (sr * 0.05))  # fade out rapide
            val  = _m.sin(2 * _m.pi * freq * i / sr) * volume * fade
            s    = max(-32768, min(32767, int(val * 32767)))
            buf[i*2]   = s & 0xFF
            buf[i*2+1] = (s >> 8) & 0xFF
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _generer_sons(self):
        try:
            self.son_bon     = self._generer_son(880, 120, 0.4)
            self.son_piege   = self._generer_son(200, 300, 0.5)
            self.son_rate    = self._generer_son(350, 150, 0.35)
            self.son_combo   = self._generer_son(1100, 200, 0.45)
            self.son_depart  = self._generer_son(660, 180, 0.5)
            self.son_powerup = self._generer_son(1320, 250, 0.5)
            self.sons_ok     = True
            self._generer_musique_arcade()
        except Exception:
            self.sons_ok = False

    def _generer_musique_arcade(self):
        """Melodie douce et joyeuse style carillon, boucle de 8 mesures."""
        import math as _m
        sr     = 44100
        bpm    = 112
        beat   = sr * 60 // bpm
        total  = beat * 32          # 8 mesures de 4 temps
        buf    = bytearray(total * 2)

        def mixer(idx, val):
            if 0 <= idx < total:
                cur = int.from_bytes(buf[idx*2:idx*2+2], "little", signed=True)
                s   = max(-32768, min(32767, cur + int(val * 32767)))
                buf[idx*2]   = s & 0xFF
                buf[idx*2+1] = (s >> 8) & 0xFF

        def note_sine(freq, debut, duree, vol=0.14):
            """Sinus avec attaque douce et extinction progressive."""
            atk = min(int(sr * 0.02), duree // 4)
            rel = min(int(sr * 0.06), duree // 3)
            for i in range(duree):
                t_i = i / sr
                if i < atk:
                    env = i / atk
                elif i > duree - rel:
                    env = (duree - i) / rel
                else:
                    env = 1.0
                # Legere harmonique pour sonner "xylophone"
                v = (_m.sin(2*_m.pi*freq*t_i) * 0.7 +
                     _m.sin(2*_m.pi*freq*2*t_i) * 0.2 +
                     _m.sin(2*_m.pi*freq*3*t_i) * 0.1) * vol * env
                mixer(debut + i, v)

        # Gamme Do majeur
        C4,D4,E4,F4,G4,A4,B4 = 262,294,330,349,392,440,494
        C5,D5,E5,G5,A5       = 523,587,659,784,880
        C3,G3,A3,F3          = 131,196,220,175

        dn = beat * 3 // 4   # noire pointee (note normale)
        dh = beat // 2       # croche
        dw = beat * 2        # blanche

        # -- Melodie (voix principale) --------------------------------------
        melodie = [
            # Mesure 1 - "Do Re Mi Sol"
            (C5, 0,      dn), (D5, beat,   dn), (E5, beat*2, dn), (G5, beat*3, dn),
            # Mesure 2 - "Mi Re Do Mi"
            (E5, beat*4, dn), (D5, beat*5, dn), (C5, beat*6, dw),
            # Mesure 3 - "Sol La Sol Mi"
            (G5, beat*8,  dn), (A5, beat*9,  dn), (G5, beat*10, dn), (E5, beat*11, dn),
            # Mesure 4 - "Mi Re Do - " (descente)
            (E5, beat*12, dn), (D5, beat*13, dn), (C5, beat*14, dw),
            # Mesure 5 - variation plus animee
            (E5, beat*16, dh), (G5, beat*16+dh, dh), (A5, beat*17, dn),
            (G5, beat*18, dh), (E5, beat*18+dh, dh), (D5, beat*19, dn),
            # Mesure 6
            (C5, beat*20, dh), (E5, beat*20+dh, dh), (G5, beat*21, dn),
            (E5, beat*22, dh), (D5, beat*22+dh, dh), (C5, beat*23, dn),
            # Mesure 7 - montee
            (D5, beat*24, dn), (E5, beat*25, dn), (G5, beat*26, dn), (A5, beat*27, dn),
            # Mesure 8 - fin apaisee
            (G5, beat*28, dn), (E5, beat*29, dn), (C5, beat*30, dw),
        ]
        for freq, debut, duree in melodie:
            note_sine(freq, debut, duree, vol=0.16)

        # -- Accompagnement arpege (voix medium) ---------------------------
        arpege = [
            (C4,0),(E4,dh),(G4,beat),(E4,beat+dh),
            (C4,beat*2),(E4,beat*2+dh),(G4,beat*3),(E4,beat*3+dh),
            (C4,beat*4),(E4,beat*4+dh),(G4,beat*5),(E4,beat*5+dh),
            (C4,beat*6),(E4,beat*6+dh),(G4,beat*7),(E4,beat*7+dh),
            (G3,beat*8),(B4//2,beat*8+dh),(D4,beat*9),(B4//2,beat*9+dh),
            (G3,beat*10),(B4//2,beat*10+dh),(D4,beat*11),(B4//2,beat*11+dh),
            (A3,beat*12),(C4,beat*12+dh),(E4,beat*13),(C4,beat*13+dh),
            (A3,beat*14),(C4,beat*14+dh),(E4,beat*15),(C4,beat*15+dh),
        ]
        for freq, debut, duree in [(f, d, dh) for f, d in arpege]:
            note_sine(freq, debut, dh, vol=0.08)
        # Repeter l'arpege pour les mesures 5-8
        for freq, debut, duree in [(f, d + beat*16, dh) for f, d in arpege]:
            note_sine(freq, debut, dh, vol=0.08)

        # -- Basse douce (temps forts uniquement) --------------------------
        basse = [
            (C3,0),(C3,beat*2),(C3,beat*4),(C3,beat*6),
            (G3,beat*8),(G3,beat*10),(A3,beat*12),(F3,beat*14),
            (C3,beat*16),(C3,beat*18),(C3,beat*20),(C3,beat*22),
            (G3,beat*24),(A3,beat*26),(F3,beat*28),(C3,beat*30),
        ]
        for freq, debut in basse:
            note_sine(freq, debut, beat, vol=0.12)

        son = pygame.mixer.Sound(buffer=bytes(buf))
        son.set_volume(0.45)
        son.play(-1)
        self._musique_arcade = son

    def _jouer_son(self, son):
        if self.sons_ok:
            son.play()

    # -- Meilleur score -----------------------------------------------------------------
    def _charger_meilleur_score(self):
        try:
            with open("meilleur_score.txt") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def _sauvegarder_meilleur_score(self, score):
        try:
            with open("meilleur_score.txt", "w") as f:
                f.write(str(score))
        except Exception:
            pass

    def _charger_boutique(self):
        import json
        defaut = {
            "pieces": 0,
            "skin_actif": "celeste",
            "skins_achetes": ["celeste"],
            "taille_niveau": 0,
            "vitesse_niveau": 0,
            "combo_niveau": 0,
            "pieces_niveau": 0,
            # -- Pass Royal --
            "pass_xp": 0,
            "pass_niveau": 0,
            "pass_premium": False,
            "pass_recompenses_recues": [],
            "pass_recompenses_disponibles": [],
            # -- Stickers personnalises --
            "stickers_achetes": ["etoile"],
            "stickers_slots": [None, None, None],
            # -- Boites de recompenses --
            "boites_inventaire": {},   # {"boite_normale": 2, "grande_boite": 0, ...}
            # -- Bol personnalise --
            "bol_mode": "boutique",             # "boutique" ou "perso"
            "bol_perso_couleur": [220, 80, 80], # [r, g, b] couleur du bol perso
        }
        try:
            with open("boutique.json") as f:
                data = json.load(f)
                for k, v in defaut.items():
                    data.setdefault(k, v)
                return data
        except Exception:
            return defaut

    def _sauvegarder_boutique(self):
        import json
        try:
            with open("boutique.json", "w") as f:
                json.dump(self.boutique, f)
        except Exception:
            pass

    # -- Pass Royal : calcul XP et distribution des récompenses ----------
    def _calculer_xp_partie(self):
        """Calcule l'XP gagnée en fin de partie selon les performances."""
        score_total = self.score_energie + self.score_sante
        t = self.temps_fin if self.temps_fin > 0 else self._temps_ecoule()
        xp = 0
        # Base : score / 5
        xp += max(0, score_total // 5)
        # Bonus survie
        if t >= 60:  xp += 50
        elif t >= 30:  xp += 25
        elif t >= 15:  xp += 10
        # Bonus combo
        if self.max_combo >= 10: xp += 40
        elif self.max_combo >= 5:  xp += 20
        elif self.max_combo >= 3:  xp += 8
        # Bonus pièces gagnées (1 XP / 10 pièces)
        xp += self.pieces_gagnees // 10
        return max(5, xp)  # au moins 5 XP par partie

    def _appliquer_xp_pass(self, xp_gagnee):
        """Ajoute de l'XP, monte les paliers. Met les récompenses en 'disponibles' (pas auto-données)."""
        self.boutique["pass_xp"] = self.boutique.get("pass_xp", 0) + xp_gagnee
        total_xp = self.boutique["pass_xp"]
        recu  = self.boutique.get("pass_recompenses_recues", [])
        dispo = self.boutique.get("pass_recompenses_disponibles", [])

        # Déterminer le nouveau palier
        nouveau_niveau = 0
        for tier_data in PASS_TIERS:
            if total_xp >= tier_data["xp_cumul"]:
                nouveau_niveau = tier_data["tier"]
        self.boutique["pass_niveau"] = nouveau_niveau

        # Mettre les récompenses débloquées en "disponibles" (le joueur doit les réclamer)
        for tier_data in PASS_TIERS:
            t_num = tier_data["tier"]
            if t_num > nouveau_niveau:
                break
            cle_free = f"free_{t_num}"
            if cle_free not in recu and cle_free not in dispo:
                dispo.append(cle_free)
            # Premium : seulement si le pass est acheté
            if self.boutique.get("pass_premium", False):
                cle_prem = f"premium_{t_num}"
                if cle_prem not in recu and cle_prem not in dispo:
                    dispo.append(cle_prem)

        self.boutique["pass_recompenses_disponibles"] = dispo
        self._sauvegarder_boutique()

    def _donner_recompense(self, reward):
        """Applique une récompense de pass (pièces, boite, ou skin)."""
        if reward[0] == "pieces":
            self.boutique["pieces"] = self.boutique.get("pieces", 0) + reward[1]
        elif reward[0] == "boite":
            inv = self.boutique.get("boites_inventaire", {})
            inv[reward[1]] = inv.get(reward[1], 0) + 1
            self.boutique["boites_inventaire"] = inv
        elif reward[0] == "skin":
            skin_cle = reward[1]
            achetes = self.boutique.get("skins_achetes", [])
            if skin_cle not in achetes:
                achetes.append(skin_cle)
            self.boutique["skins_achetes"] = achetes

    # -- Fond anime --------------------------------------------------------
    def _dessiner_fond(self):
        for row in range(HAUTEUR):
            ratio = row / HAUTEUR
            r = int(BLEU_CIEL[0] + (BLEU_FONCE[0]-BLEU_CIEL[0]) * ratio * 0.3)
            g = int(BLEU_CIEL[1] + (BLEU_FONCE[1]-BLEU_CIEL[1]) * ratio * 0.3)
            b = int(BLEU_CIEL[2] + (BLEU_FONCE[2]-BLEU_CIEL[2]) * ratio * 0.3)
            pygame.draw.line(self.ecran, (r,g,b), (0,row), (LARGEUR,row))
        t = pygame.time.get_ticks() / 1000
        for i in range(5):
            x = ((t*25 + i*280) % (LARGEUR+220)) - 110
            y = 90 + i*75
            for j in range(3):
                pygame.draw.circle(self.ecran, BLANC, (int(x+( j-1)*45), int(y)), 38+j*6)

    def _dessiner_sol(self):
        pygame.draw.rect(self.ecran, (34,139,34), (0, HAUTEUR-55, LARGEUR, 55))
        for i in range(0, LARGEUR, 35):
            xg = i + int(math.sin(i * 0.7) * 4)
            pygame.draw.line(self.ecran, (0,100,0), (xg, HAUTEUR-55), (xg, HAUTEUR-67), 3)

    # -- HUD ---------------------------------------------------------------
    def _dessiner_hud(self):
        t = self._temps_ecoule()
        label, couleur_label = self._niveau_label()

        # Barre noire en haut
        pygame.draw.rect(self.ecran, (0,0,0,200), (0,0,LARGEUR,105))

        # Temps ecoule
        txt_t = self.fonte_score.render(f"{int(t)}s", True, OR)
        self.ecran.blit(txt_t, (LARGEUR//2 - txt_t.get_width()//2, 20))

        # Vitesse / niveau
        txt_niv = self.fonte_texte.render(f"NIVEAU : {label}", True, couleur_label)
        self.ecran.blit(txt_niv, (LARGEUR//2 - txt_niv.get_width()//2, 65))

        # Scores
        self.ecran.blit(self.fonte_texte.render(f"Energie: {self.score_energie}", True, OR), (35, 28))
        self.ecran.blit(self.fonte_texte.render(f"Sante: {self.score_sante}", True, ROUGE),   (35, 60))

        # Pieces gagnees cette partie
        pieces_surf = self.fonte_texte.render(f"Pieces: +{self.pieces_gagnees}", True, OR)
        self.ecran.blit(pieces_surf, (35, 88))

        # Combo
        if self.combo > 1:
            self.ecran.blit(self.fonte_sous_titre.render(f"COMBO x{self.combo}!", True, JAUNE),
                            (LARGEUR-230, 30))

        # Pieges (toujours affiche)
        couleur_pieges = ROUGE_FLUO if self.pieges_attrapes > 0 else GRIS
        self.ecran.blit(self.fonte_texte.render(f"MAUVAIS: {self.pieges_attrapes}/3", True, couleur_pieges),
                        (LARGEUR-220, 70))

        # Bons manques
        if self.bons_manques > 0:
            self.ecran.blit(self.fonte_texte.render(f"RATES: {self.bons_manques}/5", True, ORANGE),
                            (35, 108))

        # Power-ups actifs
        now_hud = pygame.time.get_ticks()
        pu_y = 140
        if self.bouclier_actif:
            pygame.draw.rect(self.ecran, (80, 160, 255), (20, pu_y, 160, 28), border_radius=7)
            self.ecran.blit(self.fonte_petite.render("BOUCLIER ACTIF", True, BLANC), (28, pu_y + 7))
            pu_y += 34
        if now_hud < self.slowmo_fin:
            reste = (self.slowmo_fin - now_hud) / 6000
            pygame.draw.rect(self.ecran, (60, 20, 90), (20, pu_y, 160, 28), border_radius=7)
            pygame.draw.rect(self.ecran, (180, 80, 255), (20, pu_y, int(160 * reste), 28), border_radius=7)
            self.ecran.blit(self.fonte_petite.render("SLOW-MO", True, BLANC), (28, pu_y + 7))
            pu_y += 34
        if now_hud < self.aimant_fin:
            reste = (self.aimant_fin - now_hud) / 7000
            pygame.draw.rect(self.ecran, (90, 70, 0), (20, pu_y, 160, 28), border_radius=7)
            pygame.draw.rect(self.ecran, OR, (20, pu_y, int(160 * reste), 28), border_radius=7)
            self.ecran.blit(self.fonte_petite.render("AIMANT", True, NOIR), (28, pu_y + 7))
            pu_y += 34

        # Barre de vitesse (cote droit)
        ratio_v = (self._vitesse_actuelle() - self.VITESSE_DEPART) / (self.VITESSE_MAX - self.VITESSE_DEPART)
        barre_w = 200
        barre_x = LARGEUR - barre_w - 20
        barre_y = 130
        self.ecran.blit(self.fonte_petite.render("VITESSE", True, BLANC), (barre_x, barre_y))
        pygame.draw.rect(self.ecran, (60,60,60), (barre_x, barre_y+18, barre_w, 16), border_radius=8)
        pygame.draw.rect(self.ecran, ROUGE_FLUO,  (barre_x, barre_y+18, int(barre_w*ratio_v), 16), border_radius=8)
        pygame.draw.rect(self.ecran, BLANC,       (barre_x, barre_y+18, barre_w, 16), 2, border_radius=8)

        # Objectif du niveau en cours (coin bas droit)

    # -- Scenes ------------------------------------------------------------
    def scene_choix_bol(self):
        """Ecran de selection du bol avant de lancer la partie."""
        self._dessiner_fond()
        self._dessiner_sol()
        now    = pygame.time.get_ticks()
        souris = pygame.mouse.get_pos()

        # ── Fond semi-transparent central ────────────────────────────────────
        panel_w, panel_h = 680, 380
        panel_x = LARGEUR // 2 - panel_w // 2
        panel_y = HAUTEUR // 2 - panel_h // 2
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((10, 10, 30, 210))
        self.ecran.blit(panel, (panel_x, panel_y))
        pygame.draw.rect(self.ecran, OR, (panel_x, panel_y, panel_w, panel_h), 3, border_radius=24)

        # ── Titre ─────────────────────────────────────────────────────────────
        titre = self.fonte_sous_titre.render("Avec quel bol souhaites-tu jouer ?", True, OR)
        self.ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, panel_y + 52)))

        # ── Aperçu miniature du bol boutique ──────────────────────────────────
        skin_actif = self.boutique.get("skin_actif", "classique")
        info_skin  = Bol.SKINS.get(skin_actif, list(Bol.SKINS.values())[0])
        coul_b     = info_skin["couleur"]
        coul_bf    = tuple(max(0, int(c * 0.65)) for c in coul_b)
        coul_bl    = tuple(min(255, int(c * 1.25 + 20)) for c in coul_b)

        cx_bou = LARGEUR // 2 - 155
        cy_bou = panel_y + 190
        pulse  = 0.5 + 0.5 * math.sin(now / 300)

        # Halo bol boutique
        r_h = int(46 + 5 * pulse)
        surf_h = pygame.Surface((r_h*2+4, r_h*2+4), pygame.SRCALPHA)
        pygame.draw.circle(surf_h, (*coul_b, 70), (r_h+2, r_h+2), r_h)
        self.ecran.blit(surf_h, (cx_bou - r_h - 2, cy_bou - r_h - 2))

        pygame.draw.circle(self.ecran, coul_bf, (cx_bou, cy_bou), 40)
        pygame.draw.circle(self.ecran, coul_b,  (cx_bou, cy_bou), 38)
        pygame.draw.circle(self.ecran, coul_bl, (cx_bou, cy_bou), 28)
        pygame.draw.ellipse(self.ecran, tuple(min(255, c + 80) for c in coul_b),
                            (cx_bou - 14, cy_bou - 22, 20, 12))
        nom_s = self.fonte_petite.render(info_skin["nom"], True, BLANC)
        self.ecran.blit(nom_s, nom_s.get_rect(center=(cx_bou, cy_bou + 52)))

        # ── Aperçu miniature du bol perso ─────────────────────────────────────
        cx_per = LARGEUR // 2 + 155
        cy_per = panel_y + 190
        perso_col_raw = self.boutique.get("bol_perso_couleur", [100, 160, 255])
        coul_p  = tuple(perso_col_raw)
        coul_pf = tuple(max(0, int(c * 0.65)) for c in coul_p)
        coul_pl = tuple(min(255, int(c * 1.25 + 20)) for c in coul_p)

        r_hp = int(46 + 5 * pulse)
        surf_hp = pygame.Surface((r_hp*2+4, r_hp*2+4), pygame.SRCALPHA)
        pygame.draw.circle(surf_hp, (*coul_p, 70), (r_hp+2, r_hp+2), r_hp)
        self.ecran.blit(surf_hp, (cx_per - r_hp - 2, cy_per - r_hp - 2))

        pygame.draw.circle(self.ecran, coul_pf, (cx_per, cy_per), 40)
        pygame.draw.circle(self.ecran, coul_p,  (cx_per, cy_per), 38)
        pygame.draw.circle(self.ecran, coul_pl, (cx_per, cy_per), 28)
        pygame.draw.ellipse(self.ecran, tuple(min(255, c + 80) for c in coul_p),
                            (cx_per - 14, cy_per - 22, 20, 12))
        nom_per = self.fonte_petite.render("Mon bol Perso", True, BLANC)
        self.ecran.blit(nom_per, nom_per.get_rect(center=(cx_per, cy_per + 52)))

        # ── Boutons ───────────────────────────────────────────────────────────
        btn_bou = pygame.Rect(cx_bou - 95, cy_bou + 75, 190, 46)
        btn_per = pygame.Rect(cx_per - 95, cy_per + 75, 190, 46)
        h_bou   = btn_bou.collidepoint(souris)
        h_per   = btn_per.collidepoint(souris)

        pygame.draw.rect(self.ecran, OR if h_bou else (130, 90, 0),  btn_bou, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn_bou, 2, border_radius=12)
        t_bou = self.fonte_sous_titre.render("Boutique", True, NOIR if h_bou else BLANC)
        self.ecran.blit(t_bou, t_bou.get_rect(center=btn_bou.center))

        pygame.draw.rect(self.ecran, ROSE_PASS if h_per else (130, 20, 100), btn_per, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn_per, 2, border_radius=12)
        t_per2 = self.fonte_sous_titre.render("Personnalisation", True, NOIR if h_per else BLANC)
        self.ecran.blit(t_per2, t_per2.get_rect(center=btn_per.center))

        # ── Bouton Retour ─────────────────────────────────────────────────────
        btn_retour = pygame.Rect(panel_x + 20, panel_y + panel_h - 58, 150, 38)
        h_ret = btn_retour.collidepoint(souris)
        pygame.draw.rect(self.ecran, ROUGE if h_ret else (100, 25, 25), btn_retour, border_radius=10)
        pygame.draw.rect(self.ecran, BLANC, btn_retour, 2, border_radius=10)
        t_ret = self.fonte_petite.render("<< Retour", True, BLANC)
        self.ecran.blit(t_ret, t_ret.get_rect(center=btn_retour.center))

        def _lancer(mode):
            self.boutique["bol_mode"] = mode
            self._sauvegarder_boutique()
            self._reset()
            self.countdown_debut = pygame.time.get_ticks()
            self._cd_last_step = -1
            self.scene = "countdown"

        # ── Evenements ────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "accueil"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_bou.collidepoint(event.pos):
                    _lancer("boutique")
                elif btn_per.collidepoint(event.pos):
                    _lancer("perso")
                elif btn_retour.collidepoint(event.pos):
                    self.scene = "accueil"

        return True

    def scene_countdown(self):
        self._dessiner_fond()
        self._dessiner_sol()
        now     = pygame.time.get_ticks()
        elapsed = (now - self.countdown_debut) / 1000.0
        step    = int(elapsed)

        if step >= 4:
            self.scene = "jeu"
            self.temps_debut = now
            return True

        chiffres = ["3", "2", "1", "GO !"]
        couleurs  = [ROUGE, ORANGE, VERT, OR]
        texte   = chiffres[min(step, 3)]
        couleur = couleurs[min(step, 3)]

        frac  = elapsed - step
        scale = 1.0 + 0.4 * (1.0 - frac)
        taille = int(180 * scale)
        fonte_cd = pygame.font.Font(None, max(10, taille))
        alpha = max(0, int(255 * (1.0 - frac * 0.5)))

        surf  = fonte_cd.render(texte, True, couleur)
        ombre = fonte_cd.render(texte, True, NOIR)
        surf.set_alpha(alpha)
        ombre.set_alpha(alpha // 2)
        cx, cy = LARGEUR // 2, HAUTEUR // 2
        self.ecran.blit(ombre, ombre.get_rect(center=(cx+6, cy+6)))
        self.ecran.blit(surf,  surf.get_rect(center=(cx, cy)))

        if not hasattr(self, '_cd_last_step') or self._cd_last_step != step:
            self._cd_last_step = step
            self._jouer_son(self.son_depart)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def scene_pause(self):
        overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.ecran.blit(overlay, (0, 0))

        titre = self.fonte_titre.render("PAUSE", True, BLANC)
        self.ecran.blit(titre, titre.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 80)))

        sous = self.fonte_sous_titre.render("Appuie sur ECHAP pour reprendre", True, GRIS)
        self.ecran.blit(sous, sous.get_rect(center=(LARGEUR//2, HAUTEUR//2)))

        souris = pygame.mouse.get_pos()
        btn_quit = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2 + 60, 300, 55)
        hover = btn_quit.collidepoint(souris)
        pygame.draw.rect(self.ecran, ROUGE if hover else (150, 50, 50), btn_quit, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn_quit, 3, border_radius=12)
        t_q = self.fonte_sous_titre.render("Quitter la partie", True, BLANC)
        self.ecran.blit(t_q, t_q.get_rect(center=btn_quit.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "jeu"
            if event.type == pygame.MOUSEBUTTONDOWN and btn_quit.collidepoint(event.pos):
                self._reset()
                self.scene = "accueil"
        return True

    def scene_gameover(self):
        self._dessiner_fond()
        self._dessiner_sol()
        now     = pygame.time.get_ticks()
        elapsed = (now - self.gameover_debut) / 1000.0

        if elapsed >= 2.2:
            self.scene = "resultats"
            return True

        alpha = int(120 + 60 * math.sin(elapsed * 8))
        overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        overlay.fill((180, 0, 0, alpha))
        self.ecran.blit(overlay, (0, 0))

        scale = min(1.0, elapsed / 0.4)
        taille = int(120 * scale)
        if taille > 10:
            fonte_go = pygame.font.Font(None, taille)
            surf  = fonte_go.render("GAME OVER", True, BLANC)
            ombre = fonte_go.render("GAME OVER", True, ROUGE)
            cx, cy = LARGEUR // 2, HAUTEUR // 2
            self.ecran.blit(ombre, ombre.get_rect(center=(cx+5, cy+5)))
            self.ecran.blit(surf,  surf.get_rect(center=(cx, cy)))

        if elapsed > 1.0:
            sous = self.fonte_sous_titre.render("Resultats dans un instant...", True, GRIS)
            sous.set_alpha(int(255 * min(1.0, (elapsed - 1.0) * 2)))
            self.ecran.blit(sous, sous.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 80)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def scene_accueil(self):
        self._dessiner_fond()
        self._dessiner_sol()
        now = pygame.time.get_ticks()

        # -- Banniere titre
        ban = pygame.Surface((LARGEUR, 155), pygame.SRCALPHA)
        ban.fill((0, 0, 0, 110))
        self.ecran.blit(ban, (0, 0))

        bob = math.sin(now / 600) * 4
        for txt, cy, col in [("LA COURSE DU", 48, BLANC), ("PETIT-DEJEUNER", 105, OR)]:
            ombre = self.fonte_titre.render(txt, True, NOIR)
            surf  = self.fonte_titre.render(txt, True, col)
            r = surf.get_rect(center=(LARGEUR//2, int(cy + bob)))
            self.ecran.blit(ombre, (r.x+4, r.y+4))
            self.ecran.blit(surf, r)

        def encadre(x, y, w, h, bg, border, rayon=14):
            pygame.draw.rect(self.ecran, bg,     (x, y, w, h), border_radius=rayon)
            pygame.draw.rect(self.ecran, border, (x, y, w, h), 4, border_radius=rayon)

        cx = LARGEUR // 2

        # BUT DU JEU
        encadre(cx - 420, 190, 840, 90, (255, 248, 200), OR)
        t = self.fonte_sous_titre.render("BUT DU JEU", True, (140, 90, 0))
        self.ecran.blit(t, t.get_rect(center=(cx, 210)))
        t2 = self.fonte_texte.render(
            "Attrape les bons aliments du petit-dejeuner pour rester en forme jusqu'a 12h !", True, (80, 55, 0))
        self.ecran.blit(t2, t2.get_rect(center=(cx, 248)))

        # MEILLEUR SCORE
        encadre(cx - 200, 310, 400, 100, (255, 245, 195), OR)
        t3 = self.fonte_sous_titre.render("MEILLEUR SCORE", True, (140, 100, 0))
        self.ecran.blit(t3, t3.get_rect(center=(cx, 330)))
        score_surf = self.fonte_titre.render(str(self.meilleur_score), True, OR)
        self.ecran.blit(score_surf, score_surf.get_rect(center=(cx, 372)))

        # Boutons
        souris = pygame.mouse.get_pos()

        # JOUER
        btn_jouer = pygame.Rect(cx - 200, 445, 400, 72)
        h_jouer   = btn_jouer.collidepoint(souris)
        pulse = int(5 * abs(math.sin(now / 400)))
        pygame.draw.rect(self.ecran, (0, 160, 60),
                         btn_jouer.inflate(pulse*2, pulse*2), border_radius=22)
        pygame.draw.rect(self.ecran, VERT if h_jouer else (30, 150, 55), btn_jouer, border_radius=18)
        pygame.draw.rect(self.ecran, BLANC, btn_jouer, 4, border_radius=18)
        t_j = self.fonte_titre.render("JOUER !", True, BLANC)
        self.ecran.blit(t_j, t_j.get_rect(center=btn_jouer.center))

        # TUTORIEL + BOUTIQUE (cote a cote)
        btn_tuto = pygame.Rect(cx - 290, 540, 250, 52)
        h_tuto   = btn_tuto.collidepoint(souris)
        pygame.draw.rect(self.ecran, VIOLET if h_tuto else (100, 30, 150), btn_tuto, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn_tuto, 2, border_radius=12)
        t_t = self.fonte_sous_titre.render("TUTORIEL ->", True, BLANC)
        self.ecran.blit(t_t, t_t.get_rect(center=btn_tuto.center))

        btn_boutique = pygame.Rect(cx + 40, 540, 250, 52)
        h_bout = btn_boutique.collidepoint(souris)
        pygame.draw.rect(self.ecran, OR if h_bout else (140, 100, 0), btn_boutique, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn_boutique, 2, border_radius=12)
        t_b = self.fonte_sous_titre.render("BOUTIQUE ->", True, BLANC)
        self.ecran.blit(t_b, t_b.get_rect(center=btn_boutique.center))

        # BOITES + PERSO (cote a cote)
        btn_boites = pygame.Rect(cx - 290, 602, 250, 52)
        h_boites   = btn_boites.collidepoint(souris)
        inv_acc = self.boutique.get("boites_inventaire", {})
        nb_boites_total = sum(inv_acc.values())
        pulse_b = int(4 * abs(math.sin(now / 380)))
        couleur_boite = (70, 155, 255) if h_boites else (30, 90, 180)
        pygame.draw.rect(self.ecran, (50, 120, 230),
                         btn_boites.inflate(pulse_b*2 if nb_boites_total > 0 else 0,
                                            pulse_b*2 if nb_boites_total > 0 else 0), border_radius=14)
        pygame.draw.rect(self.ecran, couleur_boite, btn_boites, border_radius=12)
        pygame.draw.rect(self.ecran, (120, 180, 255), btn_boites, 2, border_radius=12)
        label_boites = f"BOITES ({nb_boites_total})" if nb_boites_total > 0 else "BOITES"
        t_boi = self.fonte_sous_titre.render(label_boites, True, BLANC)
        self.ecran.blit(t_boi, t_boi.get_rect(center=btn_boites.center))
        if nb_boites_total > 0:
            notif = self.fonte_petite.render("A ouvrir !", True, OR)
            self.ecran.blit(notif, notif.get_rect(center=(btn_boites.right - 38, btn_boites.top - 10)))

        btn_perso = pygame.Rect(cx + 40, 602, 250, 52)
        h_perso   = btn_perso.collidepoint(souris)
        pygame.draw.rect(self.ecran, ROSE_PASS if h_perso else (130, 20, 100), btn_perso, border_radius=12)
        pygame.draw.rect(self.ecran, (255, 140, 220), btn_perso, 2, border_radius=12)
        t_per = self.fonte_sous_titre.render("PERSO ->", True, BLANC)
        self.ecran.blit(t_per, t_per.get_rect(center=btn_perso.center))

        # PASS ROYAL (bouton centré en bas)
        btn_pass = pygame.Rect(cx - 160, 664, 320, 52)
        h_pass = btn_pass.collidepoint(souris)
        pygame.draw.rect(self.ecran, VIOLET_PASS if h_pass else (60, 20, 120), btn_pass, border_radius=12)
        pygame.draw.rect(self.ecran, (200, 150, 255), btn_pass, 3, border_radius=12)
        # Étoile animée
        pulse_acc = int(4 * abs(math.sin(now / 350)))
        pygame.draw.rect(self.ecran, VIOLET_PASS,
                         btn_pass.inflate(pulse_acc*2, pulse_acc*2), border_radius=14)
        pygame.draw.rect(self.ecran, VIOLET_PASS if h_pass else (60, 20, 120), btn_pass, border_radius=12)
        pygame.draw.rect(self.ecran, (200, 150, 255), btn_pass, 3, border_radius=12)
        surf_pass = self.fonte_sous_titre.render("* PASS ROYAL *", True, (220, 180, 255))
        self.ecran.blit(surf_pass, surf_pass.get_rect(center=btn_pass.center))
        # Mini barre XP sous le bouton
        pass_niv_acc = self.boutique.get("pass_niveau", 0)
        pass_xp_acc  = self.boutique.get("pass_xp", 0)
        xp_label = self.fonte_petite.render(f"Palier {pass_niv_acc}/{len(PASS_TIERS)}  |  {pass_xp_acc} XP", True, (160, 120, 220))
        self.ecran.blit(xp_label, xp_label.get_rect(center=(cx, 726)))

        # Affichage pieces totales (grand, avec icone pièce)
        pieces_val = self.boutique['pieces']
        p_box_w, p_box_h = 260, 52
        p_box_x, p_box_y = LARGEUR - p_box_w - 16, 12
        pygame.draw.rect(self.ecran, (60, 45, 0), (p_box_x, p_box_y, p_box_w, p_box_h), border_radius=14)
        pygame.draw.rect(self.ecran, OR, (p_box_x, p_box_y, p_box_w, p_box_h), 2, border_radius=14)
        # Icône pièce
        pygame.draw.circle(self.ecran, (180, 130, 0), (p_box_x + 28, p_box_y + 26), 18)
        pygame.draw.circle(self.ecran, OR,             (p_box_x + 28, p_box_y + 26), 16)
        pygame.draw.circle(self.ecran, (255, 240, 100),(p_box_x + 28, p_box_y + 26), 12)
        pygame.draw.circle(self.ecran, (255, 255, 200),(p_box_x + 23, p_box_y + 21),  5)
        pieces_surf = self.fonte_sous_titre.render(f"{pieces_val}", True, OR)
        self.ecran.blit(pieces_surf, pieces_surf.get_rect(midleft=(p_box_x + 52, p_box_y + 26)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_jouer.collidepoint(event.pos):
                    self.scene = "choix_bol"
                elif btn_tuto.collidepoint(event.pos):
                    self.tuto_page = 0
                    self.scene = "tuto"
                elif btn_boutique.collidepoint(event.pos):
                    self.scene = "boutique"
                elif btn_boites.collidepoint(event.pos):
                    self._boite_etat = "menu"
                    self._boite_ouverte_id = None
                    self._boite_recompense = None
                    self._boite_selected = 0
                    self.scene = "boites"
                elif btn_perso.collidepoint(event.pos):
                    self.scene = "perso"
                elif btn_pass.collidepoint(event.pos):
                    self.scene = "pass"

        return True

    def scene_tuto(self):
        """Tutoriel interactif."""
        self._dessiner_fond()
        self._dessiner_sol()

        now = pygame.time.get_ticks()
        pages = [
            {
                "titre": "BIENVENUE !",
                "couleur": OR,
                "textes": [
                    "Bienvenue dans LA COURSE DU PETIT-DEJEUNER !",
                    "",
                    "Des aliments tombent du ciel. Ton bol se deplace",
                    "a gauche et a droite pour les attraper.",
                    "",
                    "Utilise les fleches GAUCHE/DROITE ou les touches A/D.",
                ],
                "demo": "bol"
            },
            {
                "titre": "LES ALIMENTS",
                "couleur": VERT,
                "textes": [
                    "Les bons aliments sont entoures de VERT :",
                    "Oeuf, Yaourt, Pomme, Pain complet, Amandes, Kiwi.",
                    "",
                    "Les mauvais aliments sont entoures de ROUGE :",
                    "Bonbons, Biscuit, Soda. Evite-les !",
                    "",
                    "Tu attrapes 3 mauvais aliments (rouges) => tu perds !",
                    "Tu laisses passer 5 bons aliments sans les attraper => tu perds !",
                ],
                "demo": "aliments"
            },
            {
                "titre": "LES POWER-UPS",
                "couleur": VIOLET,
                "textes": [
                    "[B]  BOUCLIER  - Attrape-le pour l'activer ! Si tu touches",
                    "     un mauvais aliment, le bouclier te protege une fois.",
                    "",
                    "[S]  SLOW-MO  - ralentit tous les aliments pendant 6 secondes.",
                    "",
                    "[A]  AIMANT  - attire les bons aliments vers ton bol.",
                    "",
                    "Les power-ups apparaissent toutes les 12 a 18 secondes !",
                ],
                "demo": "powerups"
            },
        ]

        p = pages[self.tuto_page]

        # Fond de la boite
        box = pygame.Rect(LARGEUR//2 - 480, 80, 960, 580)
        pygame.draw.rect(self.ecran, (20, 20, 40), box, border_radius=20)
        pygame.draw.rect(self.ecran, p["couleur"], box, 5, border_radius=20)

        # Titre de page
        titre_surf = self.fonte_titre.render(p["titre"], True, p["couleur"])
        ombre_surf = self.fonte_titre.render(p["titre"], True, NOIR)
        self.ecran.blit(ombre_surf, ombre_surf.get_rect(center=(LARGEUR//2 + 3, 130)))
        self.ecran.blit(titre_surf, titre_surf.get_rect(center=(LARGEUR//2, 130)))

        # Indicateur de page
        for i in range(len(pages)):
            col = p["couleur"] if i == self.tuto_page else (80, 80, 80)
            pygame.draw.circle(self.ecran, col, (LARGEUR//2 - (len(pages)-1)*18 + i*36, 175), 8)

        # Textes
        ty = 200
        for ligne in p["textes"]:
            if ligne == "":
                ty += 10
            elif ligne.startswith("["):
                col_pu = (80,160,255) if "[B]" in ligne else (180,80,255) if "[S]" in ligne else (210,160,0)
                self.ecran.blit(self.fonte_texte.render(ligne, True, col_pu), (LARGEUR//2 - 440, ty))
                ty += 28
            else:
                self.ecran.blit(self.fonte_texte.render(ligne, True, BLANC), (LARGEUR//2 - 440, ty))
                ty += 26

        # Demo animee a droite
        demo_x, demo_y = LARGEUR//2 + 280, 380
        if p["demo"] == "bol":
            bx_d = demo_x + int(math.sin(now / 600) * 50)
            self.bol.x = bx_d
            self.bol.y = demo_y
            self.bol.dessiner(self.ecran)
            self.bol.x = LARGEUR // 2
            self.bol.y = HAUTEUR - 130
        elif p["demo"] == "aliments":
            dessiner_oeuf(self.ecran, demo_x - 60, demo_y - 40, 32)
            dessiner_pomme(self.ecran, demo_x + 60, demo_y - 40, 32)
            dessiner_bonbons(self.ecran, demo_x, demo_y + 40, 28)
            pygame.draw.circle(self.ecran, VERT,  (demo_x - 60, demo_y - 40), 44, 3)
            pygame.draw.circle(self.ecran, VERT,  (demo_x + 60, demo_y - 40), 44, 3)
            pygame.draw.circle(self.ecran, ROUGE, (demo_x, demo_y + 40),      40, 3)
        elif p["demo"] == "powerups":
            pulse = 0.5 + 0.5 * math.sin(now / 300)
            cols = [(80,160,255), (180,80,255), (210,160,0)]
            labels = ["B", "S", "A"]
            for i, (col, lab) in enumerate(zip(cols, labels)):
                px = demo_x - 60 + i * 60
                py = demo_y
                r = int(24 + 6 * pulse)
                pygame.draw.circle(self.ecran, col, (px, py), r, 4)
                pygame.draw.circle(self.ecran, BLANC, (px, py), r - 6)
                f = pygame.font.Font(None, 32)
                t = f.render(lab, True, col)
                self.ecran.blit(t, t.get_rect(center=(px, py)))

        # Boutons navigation
        souris = pygame.mouse.get_pos()
        btn_prev = pygame.Rect(LARGEUR//2 - 480, 688, 200, 52)
        btn_next = pygame.Rect(LARGEUR//2 + 280, 688, 200, 52)
        btn_jouer = pygame.Rect(LARGEUR//2 + 60, 688, 200, 52)
        btn_accueil = pygame.Rect(LARGEUR//2 - 260, 688, 200, 52)

        if self.tuto_page > 0:
            hp = btn_prev.collidepoint(souris)
            pygame.draw.rect(self.ecran, (80,80,80) if not hp else (120,120,120), btn_prev, border_radius=12)
            pygame.draw.rect(self.ecran, BLANC, btn_prev, 2, border_radius=12)
            t = self.fonte_sous_titre.render("<< Precedent", True, BLANC)
            self.ecran.blit(t, t.get_rect(center=btn_prev.center))

        if self.tuto_page < len(pages) - 1:
            hn = btn_next.collidepoint(souris)
            pygame.draw.rect(self.ecran, p["couleur"] if hn else (60,60,120), btn_next, border_radius=12)
            pygame.draw.rect(self.ecran, BLANC, btn_next, 2, border_radius=12)
            t = self.fonte_sous_titre.render("Suivant >>", True, BLANC)
            self.ecran.blit(t, t.get_rect(center=btn_next.center))
        else:
            # Bouton JOUER
            hj = btn_jouer.collidepoint(souris)
            pygame.draw.rect(self.ecran, VERT if hj else (52,152,60), btn_jouer, border_radius=12)
            pygame.draw.rect(self.ecran, BLANC, btn_jouer, 2, border_radius=12)
            t = self.fonte_titre.render("JOUER !", True, BLANC)
            self.ecran.blit(t, t.get_rect(center=btn_jouer.center))
            # Bouton RETOUR ACCUEIL
            ha = btn_accueil.collidepoint(souris)
            pygame.draw.rect(self.ecran, ROUGE if ha else (120,40,40), btn_accueil, border_radius=12)
            pygame.draw.rect(self.ecran, BLANC, btn_accueil, 2, border_radius=12)
            t_a = self.fonte_sous_titre.render("<< Accueil", True, BLANC)
            self.ecran.blit(t_a, t_a.get_rect(center=btn_accueil.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "accueil"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.tuto_page > 0 and btn_prev.collidepoint(event.pos):
                    self.tuto_page -= 1
                elif self.tuto_page < len(pages) - 1 and btn_next.collidepoint(event.pos):
                    self.tuto_page += 1
                elif self.tuto_page == len(pages) - 1 and btn_jouer.collidepoint(event.pos):
                    self._reset()
                    self.countdown_debut = pygame.time.get_ticks()
                    self._cd_last_step = -1
                    self.scene = "countdown"
                elif self.tuto_page == len(pages) - 1 and btn_accueil.collidepoint(event.pos):
                    self.scene = "accueil"

        return True

    def scene_jeu(self):
        self._dessiner_fond()
        self._dessiner_sol()

        # Controles
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]  or touches[pygame.K_a]: self.bol.deplacer_gauche()
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]: self.bol.deplacer_droite()

        # Spawn aliments
        now = pygame.time.get_ticks()
        if now - self.dernier_spawn > self._spawn_interval():
            self._spawn_aliment()
            self.dernier_spawn = now

        # Spawn power-ups (toutes les 12-18 secondes)
        intervalle_pu = random.randint(12000, 18000) if not hasattr(self, '_pu_intervalle') else self._pu_intervalle
        if not hasattr(self, '_pu_intervalle'):
            self._pu_intervalle = 14000
        if now - self.dernier_spawn_pu > self._pu_intervalle:
            self._spawn_powerup()
            self.dernier_spawn_pu = now
            self._pu_intervalle   = random.randint(12000, 18000)

        # Effets power-up actifs
        slowmo_actif = now < self.slowmo_fin
        aimant_actif = now < self.aimant_fin
        mult_vitesse  = 0.35 if slowmo_actif else 1.0

        # Aliments
        for aliment in self.aliments[:]:
            # Aimant : attire les bons aliments
            if aimant_actif and aliment.est_bon:
                dx = self.bol.x - aliment.x
                aliment.x += dx * 0.06
            # Slow-mo
            aliment.vitesse_tmp = aliment.vitesse
            aliment.vitesse = aliment.vitesse * mult_vitesse
            aliment.update()
            aliment.vitesse = aliment.vitesse_tmp
            if self.bol.collision_avec(aliment):
                self.aliments.remove(aliment)
                if aliment.est_bon:
                    self.score_energie += aliment.points_energie
                    self.score_sante   += aliment.points_sante
                    self.combo         += 1
                    self.max_combo      = max(self.max_combo, self.combo)
                    # Pieces : 2 de base + 1 par tranche de combo
                    lv_p = self.boutique.get("pieces_niveau", 0)
                    lv_c = self.boutique.get("combo_niveau",  0)
                    base_gains = 2 + (self.combo // 3)
                    mult_p = [1.0, 1.6, 2.5][lv_p]
                    gains  = int(base_gains * mult_p)
                    if self.combo >= 3:
                        gains += [0, 3, 7][lv_c]
                    self.pieces_gagnees        += gains
                    self.boutique["pieces"]    += gains
                    self._creer_particules(aliment.x, aliment.y, VERT)
                    self._ajouter_message(random.choice(["Super !", "Excellent !", "Bien joue !"]), VERT, 35)
                    if self.combo > 2:
                        self._jouer_son(self.son_combo)
                    else:
                        self._jouer_son(self.son_bon)
                else:
                    if self.bouclier_actif:
                        # Le bouclier absorbe le piege
                        self.bouclier_actif = False
                        self._creer_particules(aliment.x, aliment.y, (80, 160, 255))
                        self._ajouter_message("BOUCLIER !", (80, 160, 255), 40)
                        self._jouer_son(self.son_powerup)
                    else:
                        self.score_energie += aliment.points_energie
                        self.score_sante   += aliment.points_sante
                        self.combo          = 0
                        self.pieges_attrapes += 1
                        self._creer_particules(aliment.x, aliment.y, ROUGE)
                        self._ajouter_message("PIEGE !", ROUGE, 40)
                        self._jouer_son(self.son_piege)
                    if self.pieges_attrapes >= 3:
                        self.defaite_pieges = True
                        self.temps_fin = self._temps_ecoule()
                        self.gameover_debut = pygame.time.get_ticks()
                        self._sauvegarder_boutique()
                        self.scene = "gameover"
                        return True
            elif aliment.est_hors_ecran():
                self.aliments.remove(aliment)
                if aliment.est_bon:
                    self.bons_manques += 1
                    self._ajouter_message("Rate !", ORANGE, 32)
                    self._jouer_son(self.son_rate)
                    if self.bons_manques >= 5:
                        self.defaite_manques = True
                        self.temps_fin = self._temps_ecoule()
                        self.gameover_debut = pygame.time.get_ticks()
                        self._sauvegarder_boutique()
                        self.scene = "gameover"
                        return True
            else:
                aliment.dessiner(self.ecran, self.fonte_nom)

        # Power-ups : update + collision + dessin
        for pu in self.powerups[:]:
            pu.vitesse = pu.vitesse * mult_vitesse
            pu.update()
            pu.vitesse = pu.vitesse / mult_vitesse if mult_vitesse != 0 else pu.vitesse
            dx = pu.x - self.bol.x
            dy = pu.y - self.bol.y
            if (dx/(self.bol.largeur/2))**2 + (dy/(self.bol.hauteur/2))**2 <= 1.3:
                self.powerups.remove(pu)
                self._jouer_son(self.son_powerup)
                if pu.type_ == "bouclier":
                    self.bouclier_actif = True
                    self._ajouter_message("BOUCLIER ACTIF !", (80, 160, 255), 40)
                elif pu.type_ == "slowmo":
                    self.slowmo_fin = now + 6000
                    self._ajouter_message("SLOW-MO !", (180, 80, 255), 40)
                elif pu.type_ == "aimant":
                    self.aimant_fin = now + 7000
                    self._ajouter_message("AIMANT !", OR, 40)
                self._creer_particules(pu.x, pu.y, pu.couleur)
            elif pu.est_hors_ecran():
                self.powerups.remove(pu)
            else:
                pu.dessiner(self.ecran)

        # Particules
        for p in self.particules[:]:
            p.update()
            if p.vie <= 0:
                self.particules.remove(p)
            else:
                p.dessiner(self.ecran)

        self.bol.update()
        self.bol.dessiner(self.ecran)
        self._dessiner_hud()

        # Messages flottants
        for msg in self.messages[:]:
            msg["vie"] -= 1
            msg["y"]   -= 2.5
            if msg["vie"] <= 0:
                self.messages.remove(msg)
            else:
                f_msg = pygame.font.Font(None, msg["taille"])
                surf  = f_msg.render(msg["texte"], True, msg["couleur"])
                ombre = f_msg.render(msg["texte"], True, NOIR)
                r     = surf.get_rect(center=(LARGEUR//2, msg["y"]))
                self.ecran.blit(ombre, (r.x+3, r.y+3))
                self.ecran.blit(surf, r)

        # Evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.en_pause = True
                self.scene = "pause"

        return True

    def scene_resultats(self):
        self.ecran.fill((240,240,245))
        score_total = self.score_energie + self.score_sante
        # Utilise le temps fige a la fin de la partie
        t = self.temps_fin if self.temps_fin > 0 else self._temps_ecoule()

        if self.defaite_pieges:
            couleur, titre, eval_ = ROUGE_FLUO,"DEFAITE !",        "3 PIEGES ATTRAPES"
        elif self.defaite_manques:
            couleur, titre, eval_ = ROUGE_FLUO,"DEFAITE !",        "5 BONS ALIMENTS RATES"
        elif score_total >= 200:
            couleur, titre, eval_ = VERT,      "CHAMPION !",       "EXCELLENT"
        elif score_total >= 150:
            couleur, titre, eval_ = (34,139,34),"EXCELLENT !",     "TRES BON"
        elif score_total >= 100:
            couleur, titre, eval_ = ORANGE,    "BIEN !",           "BON"
        else:
            couleur, titre, eval_ = ROUGE,     "ATTENTION !",      "INSUFFISANT"

        pygame.draw.rect(self.ecran, couleur, (0,0,LARGEUR,145))
        for txt, cy in [(titre, 55), (eval_, 105)]:
            surf = (self.fonte_titre if cy==55 else self.fonte_sous_titre).render(txt, True, BLANC)
            self.ecran.blit(surf, surf.get_rect(center=(LARGEUR//2, cy)))

        # Score + temps survecu
        y = 175
        # Sauvegarde meilleur score
        if score_total > self.meilleur_score:
            self.meilleur_score = score_total
            self._sauvegarder_meilleur_score(score_total)
            nouveau_record = True
        else:
            nouveau_record = False

        # -- Calcul et application XP pass (une seule fois par partie) ------
        if not hasattr(self, '_pass_xp_applique') or not self._pass_xp_applique:
            self.pass_xp_gagnee = self._calculer_xp_partie()
            ancien_niveau = self.boutique.get("pass_niveau", 0)
            self._appliquer_xp_pass(self.pass_xp_gagnee)
            self._pass_xp_applique = True
            self._pass_montee_niveau = self.boutique.get("pass_niveau", 0) > ancien_niveau
        else:
            self._pass_montee_niveau = False

        self.ecran.blit(self.fonte_sous_titre.render("VOTRE SCORE", True, couleur), (60, y))
        self.ecran.blit(self.fonte_score.render(str(score_total), True, couleur), (200, y+40))
        if nouveau_record and score_total > 0:
            record_surf = self.fonte_sous_titre.render("NOUVEAU RECORD !", True, OR)
            self.ecran.blit(record_surf, (370, y+48))
        best_surf = self.fonte_texte.render(f"Meilleur score : {self.meilleur_score}", True, GRIS)
        self.ecran.blit(best_surf, (60, y+92))
        self.ecran.blit(self.fonte_texte.render(
            f"Energie: {self.score_energie}  |  Sante: {self.score_sante}  |  Temps: {int(t)}s  |  Meilleur combo: x{self.max_combo}",
            True, GRIS), (60, y+114))

        # -- Barre d'XP Pass Royal -----------------------------------------
        pass_niv = self.boutique.get("pass_niveau", 0)
        pass_xp  = self.boutique.get("pass_xp", 0)
        # Trouver XP du palier actuel et suivant
        xp_cur_palier = PASS_TIERS[min(pass_niv, len(PASS_TIERS)-1)]["xp_cumul"]
        if pass_niv < len(PASS_TIERS):
            xp_next_palier = PASS_TIERS[pass_niv]["xp_cumul"]
        else:
            xp_next_palier = XP_MAX_TOTAL
        prog_pct = 0.0
        if xp_next_palier > xp_cur_palier:
            prog_pct = min(1.0, (pass_xp - xp_cur_palier) / (xp_next_palier - xp_cur_palier))

        xp_box = pygame.Rect(50, y + 138, LARGEUR - 100, 56)
        pygame.draw.rect(self.ecran, (15, 10, 35), xp_box, border_radius=12)
        pygame.draw.rect(self.ecran, VIOLET_PASS, xp_box, 3, border_radius=12)
        # Titre PASS
        surf_pt = self.fonte_petite.render(f"PASS ROYAL  |  Palier {pass_niv}/{len(PASS_TIERS)}  |  +{self.pass_xp_gagnee} XP cette partie", True, (200, 150, 255))
        self.ecran.blit(surf_pt, (70, y + 145))
        # Barre de progression
        bx2, by2, bw2, bh2 = 70, y + 161, LARGEUR - 160, 16
        pygame.draw.rect(self.ecran, (40, 30, 70), (bx2, by2, bw2, bh2), border_radius=8)
        if prog_pct > 0:
            pygame.draw.rect(self.ecran, VIOLET_PASS, (bx2, by2, int(bw2 * prog_pct), bh2), border_radius=8)
        pygame.draw.rect(self.ecran, (200, 150, 255), (bx2, by2, bw2, bh2), 2, border_radius=8)
        xp_txt = self.fonte_petite.render(f"{pass_xp} / {xp_next_palier} XP", True, BLANC)
        self.ecran.blit(xp_txt, xp_txt.get_rect(center=(bx2 + bw2 // 2, by2 + bh2 // 2)))
        if self._pass_montee_niveau:
            surf_up = self.fonte_sous_titre.render(f"PALIER {pass_niv} ATTEINT !", True, OR)
            self.ecran.blit(surf_up, surf_up.get_rect(midright=(LARGEUR - 65, y + 162)))

        # Analyse nutritionnelle
        expl_rect = pygame.Rect(50, 355, LARGEUR-100, 340)
        pygame.draw.rect(self.ecran, BLANC, expl_rect, border_radius=15)
        pygame.draw.rect(self.ecran, couleur, expl_rect, 5, border_radius=15)
        self.ecran.blit(self.fonte_sous_titre.render("ANALYSE NUTRITIONNELLE", True, couleur), (70, 335))

        if score_total >= 150:
            lignes = [
                ("POURQUOI C'EST EXCELLENT :", True),
                ("", False),
                ("1. GLYCEMIE STABLE : glucides complexes = liberation progressive du glucose.", False),
                ("   Pas de pic d'energie ! (Source : ANSES, 2016)", False),
                ("", False),
                ("2. SATIETE PROLONGEE : les proteines ralentissent la digestion.", False),
                ("   Vous tiendrez jusqu'au dejeuner ! (Source : PNNS 2019-2023)", False),
                ("", False),
                ("3. ENERGIE DURABLE : les bonnes graisses fournissent une energie progressive.", False),
                ("   (Source : Table Ciqual ANSES)", False),
            ]
        elif self.defaite_pieges or self.defaite_manques or score_total < 100:
            lignes = [
                ("PROBLEME MAJEUR :", True),
                ("", False),
                ("Les sucres RAPIDES (cereales sucrees, viennoiseries, sodas) provoquent", False),
                ("un PIC de glycemie puis une CHUTE brutale.", False),
                ("", False),
                ("Consequence : COUP DE POMPE a 10h !", False),
                ("(Source : ANSES, 'Sucres dans l'alimentation' 2016)", False),
                ("", False),
                ("Sans PROTEINES ni FIBRES, la faim revient en 1-2h.", False),
                ("(Source : Etude INCA 3, ANSES 2017)", False),
            ]
        else:
            lignes = [
                ("POINTS A AMELIORER :", True),
                ("", False),
                ("- Ajouter plus de PROTEINES (oeufs, yaourt) pour un effet coupe-faim.", False),
                ("", False),
                ("- Privilegier les GLUCIDES COMPLEXES (avoine, pain complet) a IG bas.", False),
                ("", False),
                ("- Eviter les sucres rapides.", False),
                ("(Source : ANSES, Actualisation des reperes du PNNS 2016)", False),
            ]

        ye = 425
        for texte, gras in lignes:
            if texte == "":
                ye += 8
            else:
                f = self.fonte_texte if gras else self.fonte_petite
                c = couleur if gras else GRIS
                self.ecran.blit(f.render(texte, True, c), (70, ye))
                ye += 24 if gras else 18

        # Boutons
        souris = pygame.mouse.get_pos()
        btn = pygame.Rect(LARGEUR//2 - 290, 730, 260, 52)
        hover = btn.collidepoint(souris)
        pygame.draw.rect(self.ecran, VERT if hover else (52,152,219), btn, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn, 4, border_radius=12)
        t_btn = self.fonte_sous_titre.render("REJOUER", True, BLANC)
        self.ecran.blit(t_btn, t_btn.get_rect(center=btn.center))

        # Bouton PASS ROYAL
        btn_pass = pygame.Rect(LARGEUR//2 + 30, 730, 260, 52)
        h_pass = btn_pass.collidepoint(souris)
        pygame.draw.rect(self.ecran, VIOLET_PASS if h_pass else (60, 20, 120), btn_pass, border_radius=12)
        pygame.draw.rect(self.ecran, (200, 150, 255), btn_pass, 3, border_radius=12)
        surf_pass = self.fonte_sous_titre.render("PASS ROYAL ->", True, BLANC)
        self.ecran.blit(surf_pass, surf_pass.get_rect(center=btn_pass.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "accueil"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event.pos):
                    self._pass_xp_applique = False
                    self.scene = "accueil"
                elif btn_pass.collidepoint(event.pos):
                    self._pass_xp_applique = False
                    self.scene = "pass"

        return True

    # -------------------------------------------------------------------------
    #  HELPER : dessiner une boite style Brawl Stars
    # -------------------------------------------------------------------------
    def _dessiner_boite_visuel(self, ecran, cx, cy, boite_info, taille=80, angle=0.0, scale=1.0):
        """Dessine une boite façon Brawl Stars (corps + poignée + œil de crâne)."""
        import math as _m
        col   = boite_info["couleur"]
        bord  = boite_info["bord"]
        s     = taille * scale
        hw, hh = int(s * 0.55), int(s * 0.48)

        # Ombre portée
        pygame.draw.ellipse(ecran, (0, 0, 0, 80) if False else (20, 20, 20),
                            (cx - hw, cy + hh - 4, hw * 2, int(hh * 0.3)))

        # Corps principal
        corps = pygame.Rect(cx - hw, cy - hh, hw * 2, hh * 2)
        pygame.draw.rect(ecran, col, corps, border_radius=int(s * 0.18))
        # Reflet supérieur
        reflet = pygame.Rect(cx - hw + 6, cy - hh + 5, hw * 2 - 12, int(hh * 0.45))
        surf_r = pygame.Surface((reflet.width, reflet.height), pygame.SRCALPHA)
        surf_r.fill((255, 255, 255, 55))
        ecran.blit(surf_r, (reflet.x, reflet.y))
        # Contour
        pygame.draw.rect(ecran, bord, corps, int(s * 0.055), border_radius=int(s * 0.18))

        # Ligne de séparation horizontale (couvercle)
        lid_y = cy - int(hh * 0.20)
        pygame.draw.line(ecran, bord, (cx - hw + 4, lid_y), (cx + hw - 4, lid_y), int(s * 0.045))
        # Charnière (petits rectangles arrondis)
        for dx in (-int(hw * 0.28), int(hw * 0.28)):
            r_h = pygame.Rect(cx + dx - int(s*0.07), lid_y - int(s*0.06),
                              int(s*0.14), int(s*0.12))
            pygame.draw.rect(ecran, bord, r_h, border_radius=3)
            pygame.draw.rect(ecran, col, r_h.inflate(-4, -4), border_radius=2)

        # Poignée (arc en haut)
        pygame.draw.arc(ecran, bord,
                        (cx - int(s*0.22), cy - hh - int(s*0.22),
                         int(s*0.44), int(s*0.30)),
                        0, _m.pi, int(s*0.07))

        # Œil de crâne (style Brawl Stars)
        ey, ex_off = cy + int(hh * 0.08), int(s * 0.22)
        for ex in (cx - ex_off, cx + ex_off):
            pygame.draw.ellipse(ecran, NOIR,
                                (ex - int(s*0.12), ey - int(s*0.12),
                                 int(s*0.24), int(s*0.24)))
            pygame.draw.ellipse(ecran, BLANC,
                                (ex - int(s*0.09), ey - int(s*0.09),
                                 int(s*0.18), int(s*0.18)))
            # Pupille
            pygame.draw.circle(ecran, NOIR, (ex + int(s*0.03), ey + int(s*0.02)),
                                int(s*0.06))

    # -------------------------------------------------------------------------
    #  HELPER : tirer une récompense dans une boite
    # -------------------------------------------------------------------------
    def _tirer_recompense_boite(self, boite_id):
        """Tire aléatoirement une récompense selon les poids de la boite."""
        boite_info = next((b for b in BOITES_CATALOGUE if b["id"] == boite_id), None)
        if not boite_info:
            return ("pieces", 50)
        pool  = boite_info["contenu"]
        total = sum(p for _, _, p in pool)
        r = random.uniform(0, total)
        cumul = 0
        for typ, val, poids in pool:
            cumul += poids
            if r <= cumul:
                if typ == "sticker":
                    # Tirer un sticker non encore obtenu, sinon des pièces
                    achetes = self.boutique.get("stickers_achetes", ["etoile"])
                    manquants = [s for s in STICKERS_CATALOGUE if s["id"] not in achetes]
                    if manquants:
                        stk = random.choice(manquants)
                        return ("sticker", stk["id"])
                    return ("pieces", 80)   # compensation si tout débloqué
                elif typ == "bol":
                    # Tirer un bol premium non encore obtenu
                    tous_skins   = [k for k, v in Bol.SKINS.items()
                                    if v.get("pass_only", False)]
                    achetes_skins = self.boutique.get("skins_achetes", [])
                    manquants_skins = [s for s in tous_skins if s not in achetes_skins]
                    if manquants_skins:
                        return ("skin", random.choice(manquants_skins))
                    return ("pieces", 200)
                return (typ, val)
        return ("pieces", 50)

    # -------------------------------------------------------------------------
    #  SCENE BOITES
    # -------------------------------------------------------------------------
    def scene_boites(self):
        """Écran d'ouverture de boîtes style Brawl Stars."""
        self._dessiner_fond()
        self._dessiner_sol()
        now    = pygame.time.get_ticks()
        souris = pygame.mouse.get_pos()
        pieces = self.boutique.get("pieces", 0)
        inv    = self.boutique.get("boites_inventaire", {})

        # ── Header ───────────────────────────────────────────────────────────
        ban = pygame.Surface((LARGEUR, 110), pygame.SRCALPHA)
        ban.fill((0, 0, 0, 170))
        self.ecran.blit(ban, (0, 0))

        pulse_h = int(3 * math.sin(now / 400))
        titre_s = self.fonte_titre.render("BOITES DE RECOMPENSES", True, (120, 185, 255))
        ombre_s = self.fonte_titre.render("BOITES DE RECOMPENSES", True, (10, 30, 80))
        self.ecran.blit(ombre_s, ombre_s.get_rect(center=(LARGEUR//2+3, 50+pulse_h+3)))
        self.ecran.blit(titre_s, titre_s.get_rect(center=(LARGEUR//2, 50+pulse_h)))

        pieces_surf = self.fonte_texte.render(f"Pieces : {pieces}", True, OR)
        self.ecran.blit(pieces_surf, pieces_surf.get_rect(topright=(LARGEUR - 22, 14)))

        # ── Bouton retour ────────────────────────────────────────────────────
        btn_ret = pygame.Rect(22, HAUTEUR - 66, 180, 48)
        h_ret   = btn_ret.collidepoint(souris)
        pygame.draw.rect(self.ecran, ROUGE if h_ret else (120, 30, 30), btn_ret, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn_ret, 2, border_radius=12)
        self.ecran.blit(self.fonte_sous_titre.render("<< Retour", True, BLANC),
                        self.fonte_sous_titre.render("<< Retour", True, BLANC).get_rect(center=btn_ret.center))

        # ════════════════════════════════════════════════════════════════════
        #  ÉTAT MENU : 3 boites côte à côte + inventaire + boutons
        # ════════════════════════════════════════════════════════════════════
        if self._boite_etat == "menu":
            NB = len(BOITES_CATALOGUE)
            CARD_W = (LARGEUR - 80) // NB
            CARD_H = 480
            START_X = 40
            START_Y = 120

            for i, b in enumerate(BOITES_CATALOGUE):
                cx_c = START_X + i * CARD_W + CARD_W // 2
                cy_c = START_Y

                selectionne = (i == self._boite_selected)
                # Fond carte
                rect_c = pygame.Rect(START_X + i * CARD_W + 6, START_Y - 8,
                                     CARD_W - 12, CARD_H)
                bg_c = (18, 35, 55) if selectionne else (14, 22, 40)
                pygame.draw.rect(self.ecran, bg_c, rect_c, border_radius=18)
                pygame.draw.rect(self.ecran, b["bord"] if selectionne else (40, 60, 90),
                                 rect_c, 3 if selectionne else 2, border_radius=18)

                # Animation flottaison
                offset_y = int(8 * math.sin(now / 700 + i * 1.2)) if selectionne else 0
                bob_scale = 1.0 + 0.04 * math.sin(now / 500 + i * 0.8) if selectionne else 1.0

                # Boite dessinée
                self._dessiner_boite_visuel(self.ecran,
                                            cx_c, cy_c + 80 + offset_y,
                                            b, taille=75, scale=bob_scale)

                # Nom
                nom_s = self.fonte_sous_titre.render(b["nom"], True, b["bord"])
                self.ecran.blit(nom_s, nom_s.get_rect(center=(cx_c, START_Y + 18)))

                # Description
                desc_s = self.fonte_petite.render(b["desc"], True, (150, 190, 230))
                self.ecran.blit(desc_s, desc_s.get_rect(center=(cx_c, START_Y + 38)))

                # Inventaire
                nb_inv = inv.get(b["id"], 0)
                inv_col = OR if nb_inv > 0 else GRIS
                inv_s = self.fonte_texte.render(f"Inventaire : {nb_inv}", True, inv_col)
                self.ecran.blit(inv_s, inv_s.get_rect(center=(cx_c, cy_c + 178)))

                # Contenu / probabilités
                ty_c = cy_c + 210
                self.ecran.blit(self.fonte_petite.render("Contenu :", True, (140, 180, 220)),
                                (START_X + i*CARD_W + 18, ty_c))
                ty_c += 18
                total_p = sum(p for _, _, p in b["contenu"])
                for typ, val, poids in b["contenu"]:
                    pct = int(poids * 100 / total_p)
                    if typ == "pieces":
                        label = f"{val} pieces  ({pct}%)"
                        col_c = OR
                    elif typ == "xp":
                        label = f"+{val} XP pass  ({pct}%)"
                        col_c = (180, 100, 255)
                    elif typ == "sticker":
                        label = f"Sticker rare  ({pct}%)"
                        col_c = ROSE_PASS
                    else:
                        label = f"Bol exclusif  ({pct}%)"
                        col_c = (255, 200, 60)
                    self.ecran.blit(self.fonte_petite.render(label, True, col_c),
                                    (START_X + i*CARD_W + 18, ty_c))
                    ty_c += 17

                # Prix d'achat
                prix_y = START_Y + CARD_H - 115
                prix_s = self.fonte_texte.render(f"Acheter : {b['prix']} pieces", True,
                                                 OR if pieces >= b["prix"] else GRIS)
                self.ecran.blit(prix_s, prix_s.get_rect(center=(cx_c, prix_y)))

                # Bouton ACHETER
                btn_ach = pygame.Rect(cx_c - 90, prix_y + 18, 180, 36)
                peut_ach = pieces >= b["prix"]
                h_ach    = btn_ach.collidepoint(souris)
                bg_ach   = (120, 85, 0) if (peut_ach and h_ach) else ((70, 55, 0) if peut_ach else (40,40,50))
                pygame.draw.rect(self.ecran, bg_ach, btn_ach, border_radius=10)
                pygame.draw.rect(self.ecran, OR if peut_ach else GRIS, btn_ach, 2, border_radius=10)
                self.ecran.blit(self.fonte_texte.render("Acheter", True, OR if peut_ach else GRIS),
                                self.fonte_texte.render("Acheter", True, OR).get_rect(center=btn_ach.center))

                # Bouton OUVRIR
                btn_ouv = pygame.Rect(cx_c - 100, prix_y + 62, 200, 44)
                peut_ouv = nb_inv > 0
                h_ouv    = btn_ouv.collidepoint(souris)
                bg_ouv = b["couleur"] if (peut_ouv and h_ouv) else \
                         (tuple(max(0, c-50) for c in b["couleur"]) if peut_ouv else (35, 35, 45))
                pygame.draw.rect(self.ecran, bg_ouv, btn_ouv, border_radius=12)
                pygame.draw.rect(self.ecran, b["bord"] if peut_ouv else GRIS, btn_ouv, 2, border_radius=12)
                txt_ouv = "OUVRIR !" if peut_ouv else "Aucune boite"
                col_txt_ouv = BLANC if peut_ouv else GRIS
                self.ecran.blit(self.fonte_sous_titre.render(txt_ouv, True, col_txt_ouv),
                                self.fonte_sous_titre.render(txt_ouv, True, col_txt_ouv).get_rect(center=btn_ouv.center))

                # Enregistrer les boutons pour la gestion des clics
                if not hasattr(self, '_boites_btn_cache'):
                    self._boites_btn_cache = {}
                self._boites_btn_cache[f"ach_{i}"] = (btn_ach, b["id"], "acheter")
                self._boites_btn_cache[f"ouv_{i}"] = (btn_ouv, b["id"], "ouvrir")

        # ════════════════════════════════════════════════════════════════════
        #  ÉTAT SHAKE : animation de la boite qui s'ouvre
        # ════════════════════════════════════════════════════════════════════
        elif self._boite_etat == "shake":
            b = next((x for x in BOITES_CATALOGUE if x["id"] == self._boite_ouverte_id), BOITES_CATALOGUE[0])
            elapsed = (now - self._boite_anim_debut) / 1000.0

            # Shake
            shake_x = int(18 * math.sin(elapsed * 22) * max(0, 1.0 - elapsed / 1.2))
            shake_y = int(10 * math.cos(elapsed * 28) * max(0, 1.0 - elapsed / 1.2))

            # Scale grow
            scale = 1.0 + 0.25 * min(1.0, elapsed / 0.5)

            # Flash
            if elapsed > 0.8:
                alpha_flash = min(255, int((elapsed - 0.8) / 0.4 * 255))
                surf_flash = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
                surf_flash.fill((*b["bord"], alpha_flash))
                self.ecran.blit(surf_flash, (0, 0))

            cx_s, cy_s = LARGEUR // 2 + shake_x, HAUTEUR // 2 - 40 + shake_y
            self._dessiner_boite_visuel(self.ecran, cx_s, cy_s, b, taille=120, scale=scale)

            # Texte
            hint = self.fonte_sous_titre.render("Ouverture...", True, b["bord"])
            self.ecran.blit(hint, hint.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 120)))

            # Transition
            if elapsed >= 1.2:
                self._boite_etat    = "reveal"
                self._boite_anim_debut = now

        # ════════════════════════════════════════════════════════════════════
        #  ÉTAT REVEAL : afficher la récompense
        # ════════════════════════════════════════════════════════════════════
        elif self._boite_etat == "reveal":
            b = next((x for x in BOITES_CATALOGUE if x["id"] == self._boite_ouverte_id), BOITES_CATALOGUE[0])
            elapsed = (now - self._boite_anim_debut) / 1000.0
            rew = self._boite_recompense

            # Fond lumineux animé
            alpha_bg = min(200, int(elapsed * 400))
            surf_bg = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
            surf_bg.fill((0, 0, 0, alpha_bg))
            self.ecran.blit(surf_bg, (0, 0))

            # Rayons de lumière
            nb_rayons = 16
            for ri in range(nb_rayons):
                ang = math.pi * 2 * ri / nb_rayons + elapsed * 0.3
                lx1 = LARGEUR // 2 + int(30 * math.cos(ang))
                ly1 = HAUTEUR // 2 - 60 + int(30 * math.sin(ang))
                lx2 = LARGEUR // 2 + int(500 * math.cos(ang))
                ly2 = HAUTEUR // 2 - 60 + int(500 * math.sin(ang))
                surf_r = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
                pygame.draw.line(surf_r, (*b["bord"], 25), (lx1, ly1), (lx2, ly2), 18)
                self.ecran.blit(surf_r, (0, 0))

            # Icône de la récompense
            scale_r = min(1.0, elapsed * 2.5)
            cx_r, cy_r = LARGEUR // 2, HAUTEUR // 2 - 60

            # Cercle brillant derrière
            rayon_halo = int(120 * scale_r)
            if rayon_halo > 0:
                surf_halo = pygame.Surface((rayon_halo*2, rayon_halo*2), pygame.SRCALPHA)
                pygame.draw.circle(surf_halo, (*b["bord"], 80), (rayon_halo, rayon_halo), rayon_halo)
                self.ecran.blit(surf_halo, (cx_r - rayon_halo, cy_r - rayon_halo))

            # Texte NOUVEAU ! pour sticker/bol
            if rew[0] in ("sticker", "skin") and elapsed > 0.3:
                nouveau_s = self.fonte_titre.render("NOUVEAU !", True, OR)
                alpha_n   = min(255, int((elapsed - 0.3) * 400))
                nouveau_s.set_alpha(alpha_n)
                self.ecran.blit(nouveau_s, nouveau_s.get_rect(center=(LARGEUR//2, cy_r - 110)))

            # Description de la récompense
            if elapsed > 0.2:
                if rew[0] == "pieces":
                    desc_r = f"+{rew[1]} PIECES"
                    col_r  = OR
                    # Dessin pièce
                    pygame.draw.circle(self.ecran, OR, (cx_r, cy_r), int(55 * scale_r))
                    pygame.draw.circle(self.ecran, (255, 240, 100), (cx_r, cy_r), int(45 * scale_r))
                    if scale_r > 0.5:
                        pf = pygame.font.Font(None, int(60 * scale_r))
                        ps = pf.render("$", True, (160, 110, 0))
                        self.ecran.blit(ps, ps.get_rect(center=(cx_r, cy_r)))
                elif rew[0] == "xp":
                    desc_r = f"+{rew[1]} XP"
                    col_r  = (200, 140, 255)
                    pygame.draw.circle(self.ecran, VIOLET_PASS, (cx_r, cy_r), int(55 * scale_r))
                    if scale_r > 0.5:
                        pf = pygame.font.Font(None, int(55 * scale_r))
                        ps = pf.render("XP", True, BLANC)
                        self.ecran.blit(ps, ps.get_rect(center=(cx_r, cy_r)))
                elif rew[0] == "sticker":
                    stk_info = next((s for s in STICKERS_CATALOGUE if s["id"] == rew[1]), None)
                    desc_r = f"STICKER : {stk_info['nom'] if stk_info else rew[1]}"
                    col_r  = ROSE_PASS
                    # Dessine un grand symbole de sticker
                    r_stk = int(60 * scale_r)
                    if r_stk > 6:
                        pygame.draw.circle(self.ecran, ROSE_PASS, (cx_r, cy_r), r_stk)
                        pygame.draw.circle(self.ecran, (255, 180, 230), (cx_r, cy_r), r_stk - 8)
                        if r_stk > 20:
                            pf2 = pygame.font.Font(None, int(r_stk * 1.2))
                            sym = {"etoile": "*", "coeur": "v", "flamme": "~", "eclair": "Z",
                                   "couronne": "^", "flocon": "+", "diamant": "<>",
                                   "lune": ")", "arc": "w", "nuage": "o"}.get(rew[1], "*")
                            ps2 = pf2.render(sym, True, BLANC)
                            self.ecran.blit(ps2, ps2.get_rect(center=(cx_r, cy_r)))
                else:  # skin/bol
                    skins_noms = {"cosmos": "Bol Cosmos", "plasma": "Bol Plasma",
                                  "lava": "Bol Lava", "roi": "Bol Royal"}
                    desc_r = f"BOL : {skins_noms.get(rew[1], rew[1])}"
                    col_r  = (255, 220, 60)
                    # Dessine une étoile
                    if scale_r > 0.3:
                        for si in range(5):
                            ang_e = math.pi * 2 * si / 5 - math.pi / 2
                            ang_e2 = ang_e + math.pi / 5
                            r1, r2 = int(60 * scale_r), int(28 * scale_r)
                            pts_e = []
                            for j in range(5):
                                a1 = math.pi * 2 * j / 5 - math.pi / 2
                                a2 = a1 + math.pi / 5
                                pts_e += [(cx_r + int(r1 * math.cos(a1)), cy_r + int(r1 * math.sin(a1))),
                                          (cx_r + int(r2 * math.cos(a2)), cy_r + int(r2 * math.sin(a2)))]
                            pygame.draw.polygon(self.ecran, OR, pts_e)
                            pygame.draw.polygon(self.ecran, (200, 140, 0), pts_e, 2)

                alpha_d = min(255, int((elapsed - 0.2) * 300))
                surf_desc = self.fonte_titre.render(desc_r, True, col_r)
                surf_desc.set_alpha(alpha_d)
                self.ecran.blit(surf_desc, surf_desc.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 80)))

            # Bouton OK / Ouvrir encore
            if elapsed > 0.6:
                btn_ok  = pygame.Rect(LARGEUR//2 - 240, HAUTEUR - 120, 200, 52)
                btn_enc = pygame.Rect(LARGEUR//2 + 40,  HAUTEUR - 120, 200, 52)

                b_id_cur = self._boite_ouverte_id
                nb_encore = inv.get(b_id_cur, 0)

                h_ok  = btn_ok.collidepoint(souris)
                h_enc = btn_enc.collidepoint(souris)

                pygame.draw.rect(self.ecran, VERT if h_ok else (40, 120, 40), btn_ok, border_radius=12)
                pygame.draw.rect(self.ecran, BLANC, btn_ok, 2, border_radius=12)
                self.ecran.blit(self.fonte_sous_titre.render("OK", True, BLANC),
                                self.fonte_sous_titre.render("OK", True, BLANC).get_rect(center=btn_ok.center))

                peut_enc = nb_encore > 0
                bg_enc = b["couleur"] if (h_enc and peut_enc) else \
                         (tuple(max(0,c-60) for c in b["couleur"]) if peut_enc else (35,35,45))
                pygame.draw.rect(self.ecran, bg_enc, btn_enc, border_radius=12)
                pygame.draw.rect(self.ecran, b["bord"] if peut_enc else GRIS, btn_enc, 2, border_radius=12)
                encore_txt = f"Encore ! ({nb_encore})" if peut_enc else "Plus de boites"
                self.ecran.blit(self.fonte_sous_titre.render(encore_txt, True, BLANC if peut_enc else GRIS),
                                self.fonte_sous_titre.render(encore_txt, True, BLANC).get_rect(center=btn_enc.center))

        # ── Gestion des événements ────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self._boite_etat == "menu":
                    self.scene = "accueil"
                else:
                    self._boite_etat = "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Retour
                if btn_ret.collidepoint(event.pos) and self._boite_etat == "menu":
                    self.scene = "accueil"
                    return True

                if self._boite_etat == "menu":
                    # Sélection carte (clic n'importe où sur la carte)
                    NB_b   = len(BOITES_CATALOGUE)
                    CARD_W_b = (LARGEUR - 80) // NB_b
                    for i_b, b_b in enumerate(BOITES_CATALOGUE):
                        rect_carte = pygame.Rect(40 + i_b * CARD_W_b + 6, 120 - 8,
                                                 CARD_W_b - 12, 480)
                        if rect_carte.collidepoint(event.pos):
                            self._boite_selected = i_b

                        # Bouton ACHETER
                        key_a = f"ach_{i_b}"
                        if key_a in getattr(self, '_boites_btn_cache', {}):
                            btn_a, bid, _ = self._boites_btn_cache[key_a]
                            if btn_a.collidepoint(event.pos):
                                if pieces >= b_b["prix"]:
                                    self.boutique["pieces"] -= b_b["prix"]
                                    inv_c = self.boutique.get("boites_inventaire", {})
                                    inv_c[b_b["id"]] = inv_c.get(b_b["id"], 0) + 1
                                    self.boutique["boites_inventaire"] = inv_c
                                    inv = inv_c
                                    pieces = self.boutique["pieces"]
                                    self._sauvegarder_boutique()

                        # Bouton OUVRIR
                        key_o = f"ouv_{i_b}"
                        if key_o in getattr(self, '_boites_btn_cache', {}):
                            btn_o, bid, _ = self._boites_btn_cache[key_o]
                            if btn_o.collidepoint(event.pos):
                                nb_cur = inv.get(b_b["id"], 0)
                                if nb_cur > 0:
                                    # Retirer la boîte
                                    inv[b_b["id"]] = nb_cur - 1
                                    self.boutique["boites_inventaire"] = inv
                                    # Tirer la récompense
                                    rew = self._tirer_recompense_boite(b_b["id"])
                                    self._boite_recompense  = rew
                                    self._boite_ouverte_id  = b_b["id"]
                                    # Appliquer la récompense
                                    if rew[0] == "pieces":
                                        self.boutique["pieces"] = self.boutique.get("pieces",0) + rew[1]
                                    elif rew[0] == "xp":
                                        self._appliquer_xp_pass(rew[1])
                                    elif rew[0] == "sticker":
                                        s_ach = self.boutique.get("stickers_achetes", ["etoile"])
                                        if rew[1] not in s_ach:
                                            s_ach.append(rew[1])
                                        self.boutique["stickers_achetes"] = s_ach
                                    elif rew[0] == "skin":
                                        s_ach2 = self.boutique.get("skins_achetes", [])
                                        if rew[1] not in s_ach2:
                                            s_ach2.append(rew[1])
                                        self.boutique["skins_achetes"] = s_ach2
                                    self._sauvegarder_boutique()
                                    # Animation
                                    self._boite_etat      = "shake"
                                    self._boite_anim_debut = now

                elif self._boite_etat == "reveal":
                    elapsed_rev = (now - self._boite_anim_debut) / 1000.0
                    if elapsed_rev > 0.6:
                        b_cur = next((x for x in BOITES_CATALOGUE if x["id"] == self._boite_ouverte_id), BOITES_CATALOGUE[0])
                        btn_ok_ev  = pygame.Rect(LARGEUR//2 - 240, HAUTEUR - 120, 200, 52)
                        btn_enc_ev = pygame.Rect(LARGEUR//2 + 40,  HAUTEUR - 120, 200, 52)
                        inv_cur = self.boutique.get("boites_inventaire", {})

                        if btn_ok_ev.collidepoint(event.pos):
                            self._boite_etat = "menu"
                            self._boite_recompense = None

                        elif btn_enc_ev.collidepoint(event.pos):
                            nb_enc = inv_cur.get(self._boite_ouverte_id, 0)
                            if nb_enc > 0:
                                # Ouvrir encore
                                inv_cur[self._boite_ouverte_id] = nb_enc - 1
                                self.boutique["boites_inventaire"] = inv_cur
                                rew2 = self._tirer_recompense_boite(self._boite_ouverte_id)
                                self._boite_recompense = rew2
                                if rew2[0] == "pieces":
                                    self.boutique["pieces"] = self.boutique.get("pieces",0) + rew2[1]
                                elif rew2[0] == "xp":
                                    self._appliquer_xp_pass(rew2[1])
                                elif rew2[0] == "sticker":
                                    s_a = self.boutique.get("stickers_achetes", ["etoile"])
                                    if rew2[1] not in s_a:
                                        s_a.append(rew2[1])
                                    self.boutique["stickers_achetes"] = s_a
                                elif rew2[0] == "skin":
                                    s_a2 = self.boutique.get("skins_achetes", [])
                                    if rew2[1] not in s_a2:
                                        s_a2.append(rew2[1])
                                    self.boutique["skins_achetes"] = s_a2
                                self._sauvegarder_boutique()
                                self._boite_etat       = "shake"
                                self._boite_anim_debut = now

        # ── Overlay first-time boites ─────────────────────────────────────────
        if not self._tuto_boites_vu and self._boite_etat == "menu":
            self._dessiner_overlay_firsttime(
                "BOITES DE RECOMPENSES",
                (120, 185, 255),
                [
                    "Ouvre des boites pour gagner des recompenses aleatoires !",
                    "",
                    "  Boite (80p)  : pieces, XP pass ou sticker rare.",
                    "  Grande Boite (220p)  : pieces, XP, stickers",
                    "  et petite chance d'obtenir un bol exclusif !",
                    "  Mega Boite (600p)  : grosses pieces, beaucoup d'XP,",
                    "  stickers et bols exclusifs avec bonne probabilite.",
                    "",
                    "Tu obtiens des boites en achetant ici ou en reclamant",
                    "des paliers du Pass Royal.",
                    "Si tu as deja tout debloque : compensation en pieces.",
                ],
            )
            btn_ok_ft = pygame.Rect(LARGEUR//2 - 130, HAUTEUR//2 + 200, 260, 52)
            souris_ft = pygame.mouse.get_pos()
            h_ft = btn_ok_ft.collidepoint(souris_ft)
            pygame.draw.rect(self.ecran, (70, 155, 255) if h_ft else (30, 90, 180), btn_ok_ft, border_radius=14)
            pygame.draw.rect(self.ecran, BLANC, btn_ok_ft, 2, border_radius=14)
            self.ecran.blit(self.fonte_sous_titre.render("Compris !", True, BLANC),
                            self.fonte_sous_titre.render("Compris !", True, BLANC).get_rect(center=btn_ok_ft.center))
            for ev_ft in pygame.event.get():
                if ev_ft.type == pygame.QUIT:
                    return False
                if ev_ft.type == pygame.MOUSEBUTTONDOWN and btn_ok_ft.collidepoint(ev_ft.pos):
                    self._tuto_boites_vu = True
            return True

        return True

    def scene_pass(self):
        """Écran Pass Royal — 20 paliers, voie gratuite + voie premium.
        Le joueur doit manuellement réclamer chaque récompense débloquée."""
        self._dessiner_fond()
        self._dessiner_sol()
        now    = pygame.time.get_ticks()
        souris = pygame.mouse.get_pos()

        pass_niv  = self.boutique.get("pass_niveau", 0)
        pass_xp   = self.boutique.get("pass_xp", 0)
        premium   = self.boutique.get("pass_premium", False)
        recu      = self.boutique.get("pass_recompenses_recues", [])
        dispo     = self.boutique.get("pass_recompenses_disponibles", [])
        pieces    = self.boutique.get("pieces", 0)

        # ── Header ───────────────────────────────────────────────────────────
        ban = pygame.Surface((LARGEUR, 120), pygame.SRCALPHA)
        ban.fill((0, 0, 0, 170))
        self.ecran.blit(ban, (0, 0))

        pulse_h = int(3 * math.sin(now / 400))
        titre_s = self.fonte_titre.render("*  PASS  ROYAL  *", True, (220, 175, 255))
        ombre_s = self.fonte_titre.render("*  PASS  ROYAL  *", True, (60, 0, 120))
        self.ecran.blit(ombre_s, ombre_s.get_rect(center=(LARGEUR//2 + 3, 52 + pulse_h + 3)))
        self.ecran.blit(titre_s, titre_s.get_rect(center=(LARGEUR//2, 52 + pulse_h)))

        surf_pi = self.fonte_texte.render(f"Pieces : {pieces}", True, OR)
        self.ecran.blit(surf_pi, surf_pi.get_rect(topright=(LARGEUR - 25, 14)))
        surf_nv = self.fonte_texte.render(f"Palier  {pass_niv} / {len(PASS_TIERS)}", True, (200, 160, 255))
        self.ecran.blit(surf_nv, surf_nv.get_rect(topleft=(25, 14)))

        # ── Barre XP globale ─────────────────────────────────────────────────
        if pass_niv < len(PASS_TIERS):
            xp_next = PASS_TIERS[pass_niv]["xp_cumul"]
        else:
            xp_next = XP_MAX_TOTAL
        xp_cur_base = PASS_TIERS[min(pass_niv, len(PASS_TIERS)-1)]["xp_cumul"]
        prog = 0.0
        if xp_next > xp_cur_base:
            prog = min(1.0, (pass_xp - xp_cur_base) / (xp_next - xp_cur_base))

        bx_g, by_g, bw_g, bh_g = 25, 82, LARGEUR - 50, 22
        pygame.draw.rect(self.ecran, (30, 20, 60), (bx_g, by_g, bw_g, bh_g), border_radius=11)
        if prog > 0:
            pygame.draw.rect(self.ecran, VIOLET_PASS,
                             (bx_g, by_g, int(bw_g * prog), bh_g), border_radius=11)
        pygame.draw.rect(self.ecran, (200, 150, 255), (bx_g, by_g, bw_g, bh_g), 2, border_radius=11)
        xp_lbl = self.fonte_petite.render(f"{pass_xp} XP  -  prochain palier : {xp_next} XP", True, BLANC)
        self.ecran.blit(xp_lbl, xp_lbl.get_rect(center=(LARGEUR//2, by_g + bh_g//2)))

        # ── Bouton Premium ────────────────────────────────────────────────────
        btn_prem = pygame.Rect(LARGEUR//2 - 200, 114, 400, 38)
        if not premium:
            h_pr = btn_prem.collidepoint(souris)
            peut = pieces >= PASS_PRIX_PREMIUM
            bg_p = (140, 80, 0) if (h_pr and peut) else ((90, 50, 0) if peut else (40, 40, 55))
            pygame.draw.rect(self.ecran, bg_p, btn_prem, border_radius=10)
            pygame.draw.rect(self.ecran, OR if peut else GRIS, btn_prem, 2, border_radius=10)
            lbl_p = self.fonte_texte.render(
                f"Debloquer VOIE ROYALE  -  {PASS_PRIX_PREMIUM} pieces", True, OR if peut else GRIS)
            self.ecran.blit(lbl_p, lbl_p.get_rect(center=btn_prem.center))
        else:
            pygame.draw.rect(self.ecran, (30, 80, 30), btn_prem, border_radius=10)
            pygame.draw.rect(self.ecran, VERT, btn_prem, 2, border_radius=10)
            lbl_ok = self.fonte_texte.render("[OK] VOIE ROYALE DEBLOQUEE", True, VERT)
            self.ecran.blit(lbl_ok, lbl_ok.get_rect(center=btn_prem.center))

        # ── Grille des paliers ────────────────────────────────────────────────
        TIERS_PAR_PAGE = 5
        NB_PAGES = (len(PASS_TIERS) + TIERS_PAR_PAGE - 1) // TIERS_PAR_PAGE

        btn_prev = pygame.Rect(18, HAUTEUR - 68, 110, 46)
        btn_next = pygame.Rect(LARGEUR - 128, HAUTEUR - 68, 110, 46)
        btn_ret  = pygame.Rect(LARGEUR//2 - 110, HAUTEUR - 68, 220, 46)

        for pi in range(NB_PAGES):
            dot_x = LARGEUR//2 - (NB_PAGES * 18)//2 + pi * 18
            dot_y = HAUTEUR - 82
            col_dot = (200, 150, 255) if pi == self.pass_page else (60, 40, 100)
            pygame.draw.circle(self.ecran, col_dot, (dot_x, dot_y), 6)

        debut = self.pass_page * TIERS_PAR_PAGE
        fin   = min(debut + TIERS_PAR_PAGE, len(PASS_TIERS))
        tiers_affiches = PASS_TIERS[debut:fin]

        CARD_W = (LARGEUR - 60) // TIERS_PAR_PAGE
        CARD_H = 470
        START_Y = 162
        START_X = 30

        # Stocker les boutons RECLAMER à tester au clic
        claim_buttons = []   # liste de (pygame.Rect, cle_reward, tier_data, is_premium)

        for i, td in enumerate(tiers_affiches):
            t_num   = td["tier"]
            cx_card = START_X + i * CARD_W + CARD_W // 2
            cy_card = START_Y

            debloque   = (t_num <= pass_niv)
            actif_tier = (t_num == pass_niv + 1)

            # ─ Colonne fond ─────────────────────────
            rect_col = pygame.Rect(START_X + i * CARD_W + 4, START_Y - 10,
                                   CARD_W - 8, CARD_H)
            bg_col = (22, 18, 45) if not debloque else (18, 35, 18)
            pygame.draw.rect(self.ecran, bg_col, rect_col, border_radius=14)
            bord_col = VERT if debloque else ((200, 150, 255) if actif_tier else (50, 45, 80))
            pygame.draw.rect(self.ecran, bord_col, rect_col, 2, border_radius=14)

            # ─ Numéro de palier ──────────────────────
            col_num = OR if debloque else ((220, 180, 255) if actif_tier else GRIS)
            surf_num = self.fonte_sous_titre.render(f"Palier {t_num}", True, col_num)
            self.ecran.blit(surf_num, surf_num.get_rect(center=(cx_card, START_Y + 14)))

            surf_xp = self.fonte_petite.render(f"{td['xp_cumul']} XP", True, (160, 130, 200))
            self.ecran.blit(surf_xp, surf_xp.get_rect(center=(cx_card, START_Y + 34)))

            pygame.draw.line(self.ecran, bord_col,
                             (START_X + i * CARD_W + 14, START_Y + 46),
                             (START_X + i * CARD_W + CARD_W - 14, START_Y + 46), 1)

            # ─── VOIE GRATUITE ────────────────────────
            ry_free  = START_Y + 58
            free_rew = td["free"]
            cle_free = f"free_{t_num}"
            deja_free    = cle_free in recu
            dispo_free   = cle_free in dispo   # débloqué mais pas encore réclamé

            btn_claim_free = self._dessiner_carte_recompense_v2(
                self.ecran, cx_card, ry_free, CARD_W - 20,
                free_rew, deja_free, dispo_free, debloque, False, now, souris)
            if btn_claim_free:
                claim_buttons.append((btn_claim_free, cle_free, td, False))

            lbl_g_col = (60, 200, 60) if deja_free else ((255, 200, 50) if dispo_free else GRIS)
            lbl_g = self.fonte_petite.render(
                "RECLAME !" if deja_free else ("A RECLAMER!" if dispo_free else "GRATUIT"),
                True, lbl_g_col)
            self.ecran.blit(lbl_g, lbl_g.get_rect(center=(cx_card, ry_free + 118)))

            # ─── SÉPARATEUR ──────────────────────────
            sep_y = ry_free + 134
            pygame.draw.line(self.ecran, (80, 60, 120),
                             (START_X + i * CARD_W + 14, sep_y),
                             (START_X + i * CARD_W + CARD_W - 14, sep_y), 1)

            # ─── VOIE ROYALE (PREMIUM) ────────────────
            ry_prem  = sep_y + 14
            prem_rew = td["premium"]
            cle_prem = f"premium_{t_num}"
            deja_prem  = cle_prem in recu
            dispo_prem = cle_prem in dispo

            prem_bg = pygame.Rect(START_X + i * CARD_W + 8, ry_prem - 4,
                                  CARD_W - 16, 134)
            prem_bg_col = (35, 25, 8) if premium else (25, 20, 40)
            pygame.draw.rect(self.ecran, prem_bg_col, prem_bg, border_radius=10)
            prem_bord = OR if premium else (80, 70, 100)
            pygame.draw.rect(self.ecran, prem_bord, prem_bg, 2, border_radius=10)

            btn_claim_prem = self._dessiner_carte_recompense_v2(
                self.ecran, cx_card, ry_prem, CARD_W - 20,
                prem_rew, deja_prem, dispo_prem, debloque and premium, True, now, souris)
            if btn_claim_prem:
                claim_buttons.append((btn_claim_prem, cle_prem, td, True))

            lbl_r_col = (60, 200, 60) if deja_prem else ((255, 200, 50) if (dispo_prem and premium) else (OR if premium else (80, 70, 60)))
            lbl_r_txt = ("RECLAME !" if deja_prem else
                         ("A RECLAMER!" if (dispo_prem and premium) else "* ROYAL"))
            lbl_r = self.fonte_petite.render(lbl_r_txt, True, lbl_r_col)
            self.ecran.blit(lbl_r, lbl_r.get_rect(center=(cx_card, ry_prem + 118)))

        # ── Boutons navigation ────────────────────────────────────────────────
        if self.pass_page > 0:
            h_pv = btn_prev.collidepoint(souris)
            pygame.draw.rect(self.ecran, VIOLET_PASS if h_pv else (50, 30, 100), btn_prev, border_radius=10)
            pygame.draw.rect(self.ecran, (200, 150, 255), btn_prev, 2, border_radius=10)
            s = self.fonte_sous_titre.render("<< Prev", True, BLANC)
            self.ecran.blit(s, s.get_rect(center=btn_prev.center))
        if self.pass_page < NB_PAGES - 1:
            h_nx = btn_next.collidepoint(souris)
            pygame.draw.rect(self.ecran, VIOLET_PASS if h_nx else (50, 30, 100), btn_next, border_radius=10)
            pygame.draw.rect(self.ecran, (200, 150, 255), btn_next, 2, border_radius=10)
            s = self.fonte_sous_titre.render("Next >>", True, BLANC)
            self.ecran.blit(s, s.get_rect(center=btn_next.center))
        h_ret = btn_ret.collidepoint(souris)
        pygame.draw.rect(self.ecran, ROUGE if h_ret else (100, 20, 20), btn_ret, border_radius=10)
        pygame.draw.rect(self.ecran, BLANC, btn_ret, 2, border_radius=10)
        s = self.fonte_sous_titre.render("<< Retour", True, BLANC)
        self.ecran.blit(s, s.get_rect(center=btn_ret.center))

        # ── Gestion événements ────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene = "accueil"
                elif event.key == pygame.K_LEFT and self.pass_page > 0:
                    self.pass_page -= 1
                elif event.key == pygame.K_RIGHT and self.pass_page < NB_PAGES - 1:
                    self.pass_page += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_ret.collidepoint(event.pos):
                    self.scene = "accueil"
                elif self.pass_page > 0 and btn_prev.collidepoint(event.pos):
                    self.pass_page -= 1
                elif self.pass_page < NB_PAGES - 1 and btn_next.collidepoint(event.pos):
                    self.pass_page += 1

                # Achat voie royale premium
                elif not premium and btn_prem.collidepoint(event.pos):
                    if pieces >= PASS_PRIX_PREMIUM:
                        self.boutique["pieces"] -= PASS_PRIX_PREMIUM
                        self.boutique["pass_premium"] = True
                        # Rendre disponibles (à réclamer) les récompenses premium déjà débloquées
                        dispo_maj = self.boutique.get("pass_recompenses_disponibles", [])
                        recu_maj  = self.boutique.get("pass_recompenses_recues", [])
                        for tier_data in PASS_TIERS:
                            if tier_data["tier"] <= pass_niv:
                                cle_p = f"premium_{tier_data['tier']}"
                                if cle_p not in recu_maj and cle_p not in dispo_maj:
                                    dispo_maj.append(cle_p)
                        self.boutique["pass_recompenses_disponibles"] = dispo_maj
                        self._sauvegarder_boutique()

                # Boutons RECLAMER
                else:
                    for (btn_r, cle_r, tier_r, is_prem_r) in claim_buttons:
                        if btn_r.collidepoint(event.pos):
                            dispo_maj = self.boutique.get("pass_recompenses_disponibles", [])
                            recu_maj  = self.boutique.get("pass_recompenses_recues", [])
                            if cle_r in dispo_maj:
                                dispo_maj.remove(cle_r)
                                recu_maj.append(cle_r)
                                # Donner la récompense
                                reward = tier_r["premium"] if is_prem_r else tier_r["free"]
                                self._donner_recompense(reward)
                                self.boutique["pass_recompenses_disponibles"] = dispo_maj
                                self.boutique["pass_recompenses_recues"] = recu_maj
                                self._sauvegarder_boutique()
                            break

        # ── Overlay first-time pass ───────────────────────────────────────────
        if not self._tuto_pass_vu:
            self._dessiner_overlay_firsttime(
                "PASS ROYAL",
                (200, 150, 255),
                [
                    "Le Pass Royal te recompense pour chaque partie jouee !",
                    "",
                    "  Paliers  : gagne de l'XP en jouant pour monter",
                    "  les 20 paliers du pass.",
                    "",
                    "  Voie GRATUITE  : pieces et boites pour tout le monde.",
                    "  Voie ROYALE  : skins exclusifs + grosses boites",
                    "  (se debloque contre 1200 pieces).",
                    "",
                    "Reclame tes recompenses en cliquant sur RECLAMER !",
                    "Elles ne sont pas donnees automatiquement.",
                ],
            )
            btn_ok_ft = pygame.Rect(LARGEUR//2 - 130, HAUTEUR//2 + 200, 260, 52)
            souris_ft = pygame.mouse.get_pos()
            h_ft = btn_ok_ft.collidepoint(souris_ft)
            pygame.draw.rect(self.ecran, VIOLET_PASS if h_ft else (60, 20, 120), btn_ok_ft, border_radius=14)
            pygame.draw.rect(self.ecran, BLANC, btn_ok_ft, 2, border_radius=14)
            self.ecran.blit(self.fonte_sous_titre.render("Compris !", True, BLANC),
                            self.fonte_sous_titre.render("Compris !", True, BLANC).get_rect(center=btn_ok_ft.center))
            for ev_ft in pygame.event.get():
                if ev_ft.type == pygame.QUIT:
                    return False
                if ev_ft.type == pygame.MOUSEBUTTONDOWN and btn_ok_ft.collidepoint(ev_ft.pos):
                    self._tuto_pass_vu = True
            return True

        return True

    def _dessiner_carte_recompense_v2(self, ecran, cx, cy, largeur, reward,
                                       deja_recue, disponible, debloque,
                                       is_premium, now_ms, souris):
        """Version améliorée : retourne le pygame.Rect du bouton RECLAMER si applicable, sinon None."""
        import math as _m
        w = min(largeur - 10, 120)
        h = 100
        rx_c, ry_c = cx - w//2, cy

        # Fond
        if deja_recue:
            bg = (18, 45, 18)
        elif disponible:
            # Fond brillant pour attirer l'attention
            pulse_bg = int(15 * abs(_m.sin(now_ms / 400.0 + cx)))
            bg = (30 + pulse_bg, 55 + pulse_bg, 20)
        elif debloque:
            bg = (30, 50, 30)
        elif is_premium:
            bg = (35, 25, 8)
        else:
            bg = (30, 25, 55)
        pygame.draw.rect(ecran, bg, (rx_c, ry_c, w, h), border_radius=10)

        if deja_recue:
            bord_c = VERT
        elif disponible:
            # Bordure pulsante orange/verte
            pulse_b = 0.5 + 0.5 * _m.sin(now_ms / 200.0 + cx)
            r_b = int(200 + 55 * pulse_b)
            g_b = int(180 * pulse_b)
            bord_c = (r_b, g_b, 0)
        elif is_premium and debloque:
            bord_c = OR
        elif debloque:
            bord_c = (200, 150, 255)
        else:
            bord_c = (70, 60, 100)
        pygame.draw.rect(ecran, bord_c, (rx_c, ry_c, w, h), 2, border_radius=10)

        # Contenu (icône)
        if reward[0] == "pieces":
            pulse_r = int(3 * _m.sin(now_ms / 300.0 + cx))
            r_ico = 20 + pulse_r if disponible else 20
            pygame.draw.circle(ecran, (160, 120, 0), (cx, ry_c + 34), r_ico + 2)
            pygame.draw.circle(ecran, OR,            (cx, ry_c + 34), r_ico)
            pygame.draw.circle(ecran, (255, 240, 100), (cx, ry_c + 34), r_ico - 4)
            pygame.draw.circle(ecran, (255, 255, 200), (cx - 5, ry_c + 29), r_ico // 3)
            surf_v = self.fonte_sous_titre.render(str(reward[1]), True, OR if not deja_recue else VERT)
            ecran.blit(surf_v, surf_v.get_rect(center=(cx, ry_c + 60)))
        else:
            skin_info = Bol.SKINS.get(reward[1], {})
            coul_skin = skin_info.get("couleur", GRIS)
            coul_f = tuple(max(0, int(c * 0.65)) for c in coul_skin)
            rx_b, ry_b = 28, 16
            bx_b, by_b = cx, ry_c + 34
            pygame.draw.ellipse(ecran, coul_f,   (bx_b - rx_b, by_b - ry_b, rx_b*2, ry_b*2 + 6))
            pygame.draw.ellipse(ecran, coul_skin, (bx_b - rx_b + 2, by_b - ry_b + 2, rx_b*2 - 4, ry_b*2 + 2))
            pygame.draw.ellipse(ecran, tuple(min(255, c+50) for c in coul_skin),
                                (bx_b - rx_b, by_b - ry_b - 6, rx_b*2, 12))
            nom_s = skin_info.get("nom", reward[1])
            surf_n = self.fonte_petite.render(nom_s, True, coul_skin if not deja_recue else VERT)
            ecran.blit(surf_n, surf_n.get_rect(center=(cx, ry_c + 60)))

        # Indicateurs état
        if deja_recue:
            pygame.draw.circle(ecran, VERT, (rx_c + w - 13, ry_c + 13), 10)
            pygame.draw.circle(ecran, (0, 60, 0), (rx_c + w - 13, ry_c + 13), 10, 2)
            pygame.draw.lines(ecran, BLANC, False,
                              [(rx_c+w-19, ry_c+13), (rx_c+w-13, ry_c+18), (rx_c+w-6, ry_c+8)], 2)
        elif not debloque and not disponible:
            pygame.draw.circle(ecran, (80, 70, 100), (rx_c + w - 13, ry_c + 13), 10)
            pygame.draw.rect(ecran, (100, 90, 120),
                             (rx_c + w - 18, ry_c + 13, 10, 8), border_radius=2)
            pygame.draw.arc(ecran, (150, 140, 180),
                            (rx_c + w - 18, ry_c + 7, 10, 10), 0, _m.pi, 2)

        # Bouton RECLAMER (uniquement si disponible et pas encore reçu)
        if disponible and not deja_recue:
            btn_h = 22
            btn_w = w - 8
            btn_rx = cx - btn_w // 2
            btn_ry = ry_c + h - btn_h - 4
            btn_rect = pygame.Rect(btn_rx, btn_ry, btn_w, btn_h)
            hover_claim = btn_rect.collidepoint(souris)
            # Animation pulsante du bouton
            pulse_c = 0.5 + 0.5 * _m.sin(now_ms / 180.0 + cx)
            bg_claim = (int(180*pulse_c + 60), int(100*pulse_c), 0) if hover_claim else (int(140*pulse_c+40), 80, 0)
            pygame.draw.rect(ecran, bg_claim, btn_rect, border_radius=6)
            pygame.draw.rect(ecran, (255, 200, 50), btn_rect, 2, border_radius=6)
            lbl_c = self.fonte_petite.render("RECLAMER!", True, (255, 230, 100))
            ecran.blit(lbl_c, lbl_c.get_rect(center=btn_rect.center))
            return btn_rect

        return None

    def _dessiner_carte_recompense(self, ecran, cx, cy, largeur, reward,
                                   deja_recue, debloque, is_premium, now_ms):
        """Dessine une petite carte de récompense (pièces ou skin) dans le Pass."""
        import math as _m
        w = min(largeur - 10, 120)
        h = 100
        rx_c, ry_c = cx - w//2, cy

        # Fond de la carte
        if deja_recue:
            bg = (18, 45, 18)
        elif debloque:
            bg = (30, 60, 30)
        elif is_premium:
            bg = (35, 25, 8)
        else:
            bg = (30, 25, 55)
        pygame.draw.rect(ecran, bg, (rx_c, ry_c, w, h), border_radius=10)

        bord_c = (VERT if deja_recue else
                  (OR if (is_premium and debloque) else
                   ((200, 150, 255) if debloque else (70, 60, 100))))
        pygame.draw.rect(ecran, bord_c, (rx_c, ry_c, w, h), 2, border_radius=10)

        # Contenu
        if reward[0] == "pieces":
            # Icône pièce dorée
            pulse_r = int(3 * _m.sin(now_ms / 300.0 + cx))
            r_ico = 20 + pulse_r if (debloque and not deja_recue) else 20
            pygame.draw.circle(ecran, (160, 120, 0), (cx, ry_c + 38), r_ico + 2)
            pygame.draw.circle(ecran, OR,            (cx, ry_c + 38), r_ico)
            pygame.draw.circle(ecran, (255, 240, 100), (cx, ry_c + 38), r_ico - 4)
            pygame.draw.circle(ecran, (255, 255, 200), (cx - 5, ry_c + 33), r_ico // 3)
            # Montant
            surf_v = self.fonte_sous_titre.render(str(reward[1]), True, OR if not deja_recue else VERT)
            ecran.blit(surf_v, surf_v.get_rect(center=(cx, ry_c + 72)))
        else:
            # Mini aperçu du skin
            skin_info = Bol.SKINS.get(reward[1], {})
            coul_skin = skin_info.get("couleur", GRIS)
            coul_f = tuple(max(0, int(c * 0.65)) for c in coul_skin)
            # Corps simplifié du bol
            rx_b, ry_b = 30, 18
            bx_b, by_b = cx, ry_c + 38
            # Ellipse corps
            pygame.draw.ellipse(ecran, coul_f,   (bx_b - rx_b, by_b - ry_b, rx_b*2, ry_b*2 + 6))
            pygame.draw.ellipse(ecran, coul_skin, (bx_b - rx_b + 2, by_b - ry_b + 2, rx_b*2 - 4, ry_b*2 + 2))
            # Rebord
            pygame.draw.ellipse(ecran, tuple(min(255, c+50) for c in coul_skin),
                                (bx_b - rx_b, by_b - ry_b - 6, rx_b*2, 12))
            # Nom du skin
            nom_s = skin_info.get("nom", reward[1])
            surf_n = self.fonte_petite.render(nom_s, True, coul_skin if not deja_recue else VERT)
            ecran.blit(surf_n, surf_n.get_rect(center=(cx, ry_c + 72)))

        # Coche si déjà reçu
        if deja_recue:
            pygame.draw.circle(ecran, VERT, (rx_c + w - 14, ry_c + 14), 10)
            pygame.draw.circle(ecran, (0, 60, 0), (rx_c + w - 14, ry_c + 14), 10, 2)
            # Coche blanche
            coche_pts = [(rx_c + w - 20, ry_c + 14),
                         (rx_c + w - 14, ry_c + 19),
                         (rx_c + w - 7,  ry_c + 9)]
            pygame.draw.lines(ecran, BLANC, False, coche_pts, 2)
        elif not debloque:
            # Cadenas
            pygame.draw.circle(ecran, (80, 70, 100), (rx_c + w - 14, ry_c + 14), 10)
            pygame.draw.rect(ecran, (100, 90, 120),
                             (rx_c + w - 19, ry_c + 14, 10, 8), border_radius=2)
            pygame.draw.arc(ecran, (150, 140, 180),
                            (rx_c + w - 19, ry_c + 8, 10, 10), 0, _m.pi, 2)

    # -------------------------------------------------------------------------
    #  HELPER : overlay d'explication first-time
    # -------------------------------------------------------------------------
    def _dessiner_overlay_firsttime(self, titre, couleur_titre, lignes):
        """Dessine un overlay semi-transparent avec titre + textes d'explication."""
        overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.ecran.blit(overlay, (0, 0))

        box_w, box_h = 760, 500
        box_x, box_y = (LARGEUR - box_w) // 2, (HAUTEUR - box_h) // 2 - 20
        pygame.draw.rect(self.ecran, (18, 18, 36), (box_x, box_y, box_w, box_h), border_radius=22)
        pygame.draw.rect(self.ecran, couleur_titre, (box_x, box_y, box_w, box_h), 3, border_radius=22)

        # Titre
        t_s = self.fonte_titre.render(titre, True, couleur_titre)
        o_s = self.fonte_titre.render(titre, True, NOIR)
        self.ecran.blit(o_s, o_s.get_rect(center=(LARGEUR//2 + 3, box_y + 48 + 3)))
        self.ecran.blit(t_s, t_s.get_rect(center=(LARGEUR//2, box_y + 48)))

        # Lignes
        ty = box_y + 95
        for ligne in lignes:
            if ligne == "":
                ty += 10
                continue
            gras = ligne.startswith("  ") and ":" in ligne
            f = self.fonte_texte if gras else self.fonte_petite
            col = BLANC if gras else (200, 200, 220)
            self.ecran.blit(f.render(ligne.strip(), True, col),
                            f.render(ligne.strip(), True, col).get_rect(
                                center=(LARGEUR//2, ty + (13 if not gras else 9))))
            ty += 26 if gras else 20

    # -------------------------------------------------------------------------
    #  SCENE PERSONNALISATION (ex-onglet boutique)
    # -------------------------------------------------------------------------
    def scene_perso(self):
        """Écran de personnalisation du bol perso (couleur + stickers)."""
        import math as _pm
        self._dessiner_fond()
        self._dessiner_sol()
        now    = pygame.time.get_ticks()
        souris = pygame.mouse.get_pos()

        stickers_achetes = self.boutique.get("stickers_achetes", ["etoile"])
        slots            = self.boutique.get("stickers_slots", [None, None, None])
        if len(slots) < MAX_SLOTS_STICKERS:
            slots = (slots + [None] * MAX_SLOTS_STICKERS)[:MAX_SLOTS_STICKERS]
        perso_col_raw = self.boutique.get("bol_perso_couleur", [220, 80, 80])
        perso_col     = tuple(perso_col_raw)

        # ── Header ────────────────────────────────────────────────────────────
        ban = pygame.Surface((LARGEUR, 115), pygame.SRCALPHA)
        ban.fill((0, 0, 0, 150))
        self.ecran.blit(ban, (0, 0))
        titre_s = self.fonte_titre.render("MON BOL PERSO", True, ROSE_PASS)
        self.ecran.blit(titre_s, titre_s.get_rect(center=(LARGEUR//2, 58)))
        p_txt = self.fonte_sous_titre.render(f"Pieces : {self.boutique['pieces']}", True, OR)
        self.ecran.blit(p_txt, p_txt.get_rect(topright=(LARGEUR - 25, 18)))

        # ── Apercu du bol perso (droite) ──────────────────────────────────────
        preview_cx, preview_cy = LARGEUR - 230, 400
        preview_rx, preview_ry = 140, 90
        coul_prev      = perso_col
        coul_fonce_p   = tuple(max(0, int(c * 0.65)) for c in coul_prev)
        coul_clair_p   = tuple(min(255, int(c * 1.25 + 20)) for c in coul_prev)
        nb_p = 80
        arc_p = []
        rim_ry_p = max(10, preview_ry // 5)
        for i in range(nb_p + 1):
            a = _pm.pi * i / nb_p
            px = preview_cx + _pm.cos(_pm.pi - a) * preview_rx
            py = preview_cy + rim_ry_p + _pm.sin(a) * (preview_ry - rim_ry_p)
            arc_p.append((int(px), int(py)))
        corps_p = [(preview_cx - preview_rx, preview_cy)] + arc_p + [(preview_cx + preview_rx, preview_cy)]
        pygame.draw.polygon(self.ecran, coul_prev, corps_p)
        ombre_p = arc_p[nb_p // 2:] + [(preview_cx + preview_rx, preview_cy)]
        if len(ombre_p) >= 3:
            pygame.draw.polygon(self.ecran, coul_fonce_p, ombre_p)
        reflet_p = [(preview_cx - preview_rx, preview_cy), (preview_cx - preview_rx + 10, preview_cy)] + arc_p[:nb_p // 6]
        if len(reflet_p) >= 3:
            pygame.draw.polygon(self.ecran, coul_clair_p, reflet_p)
        pygame.draw.polygon(self.ecran, coul_fonce_p, corps_p, 3)
        old_clip_p = self.ecran.get_clip()
        self.ecran.set_clip(pygame.Rect(preview_cx - preview_rx - 4, preview_cy - rim_ry_p - 4,
                                        preview_rx * 2 + 8, rim_ry_p + 4))
        pygame.draw.ellipse(self.ecran, coul_prev,
                            (preview_cx - preview_rx, preview_cy - rim_ry_p, preview_rx * 2, rim_ry_p * 2), 8)
        pygame.draw.ellipse(self.ecran, coul_clair_p,
                            (preview_cx - preview_rx + 4, preview_cy - rim_ry_p + 3,
                             preview_rx * 2 - 8, rim_ry_p * 2 - 6), 4)
        self.ecran.set_clip(old_clip_p)
        int_rx_p = preview_rx - 10
        int_ry_p = rim_ry_p + 2
        sw_p, sh_p = max(4, int_rx_p * 2), max(4, int_ry_p * 2)
        surf_ip = pygame.Surface((sw_p, sh_p), pygame.SRCALPHA)
        pygame.draw.ellipse(surf_ip, (245, 245, 242, 255), (0, 0, sw_p, sh_p))
        self.ecran.blit(surf_ip, (preview_cx - int_rx_p, preview_cy - int_ry_p))
        # Stickers sur l'apercu
        slot_pos_prev = [
            (preview_cx - preview_rx * 45 // 100, preview_cy + preview_ry * 55 // 100),
            (preview_cx,                           preview_cy + preview_ry * 70 // 100),
            (preview_cx + preview_rx * 45 // 100,  preview_cy + preview_ry * 55 // 100),
        ]
        tmp_bol = Bol()
        for si, stk in enumerate(slots):
            if stk:
                sx_p, sy_p = slot_pos_prev[si]
                tmp_bol._dessiner_sticker_custom(self.ecran, sx_p, sy_p, 18, stk, now)
        slot_noms = ["Gauche", "Centre", "Droite"]
        for si, (spx, spy) in enumerate(slot_pos_prev):
            lbl_s = self.fonte_petite.render(slot_noms[si], True, OR)
            self.ecran.blit(lbl_s, lbl_s.get_rect(center=(spx, spy + 26)))
        ap_txt = self.fonte_sous_titre.render("Apercu", True, OR)
        self.ecran.blit(ap_txt, ap_txt.get_rect(center=(preview_cx, preview_cy - preview_ry - 28)))

        # ── Palette de couleurs ───────────────────────────────────────────────
        PALETTE_COULEURS = [
            (220,  50,  50), (220, 120,  40), (210, 185,   0), ( 90, 200,  50),
            ( 20, 170,  80), ( 15, 190, 180), ( 30, 110, 220), ( 55,  35, 210),
            (135,  35, 220), (205,  35, 180), (220,  35, 110), (255, 255, 255),
            (160, 105,  50), ( 90,  90,  90), ( 20,  20,  20), (200, 160, 100),
        ]
        PALETTE_COLS = 8
        PALETTE_SIZE = 38
        PALETTE_PAD  = 8
        pal_start_x  = 30
        pal_start_y  = 148
        lbl_pal = self.fonte_sous_titre.render("Couleur du bol :", True, ROSE_PASS)
        self.ecran.blit(lbl_pal, (pal_start_x, pal_start_y - 28))
        pal_rects = []
        for idx_c, col_c in enumerate(PALETTE_COULEURS):
            col_ci = idx_c % PALETTE_COLS
            row_ci = idx_c // PALETTE_COLS
            cx_c = pal_start_x + col_ci * (PALETTE_SIZE + PALETTE_PAD)
            cy_c = pal_start_y + row_ci * (PALETTE_SIZE + PALETTE_PAD)
            r_c  = pygame.Rect(cx_c, cy_c, PALETTE_SIZE, PALETTE_SIZE)
            pal_rects.append((r_c, col_c))
            is_sel_c = (list(col_c) == list(perso_col_raw))
            hover_c  = r_c.collidepoint(souris)
            pygame.draw.rect(self.ecran, col_c, r_c, border_radius=9)
            if is_sel_c:
                pygame.draw.rect(self.ecran, BLANC, r_c, 3, border_radius=9)
                # coche
                pygame.draw.line(self.ecran, BLANC, (cx_c+8, cy_c+PALETTE_SIZE//2),
                                 (cx_c+PALETTE_SIZE//2-2, cy_c+PALETTE_SIZE-8), 3)
                pygame.draw.line(self.ecran, BLANC, (cx_c+PALETTE_SIZE//2-2, cy_c+PALETTE_SIZE-8),
                                 (cx_c+PALETTE_SIZE-6, cy_c+8), 3)
            elif hover_c:
                pygame.draw.rect(self.ecran, (200, 200, 200), r_c, 2, border_radius=9)
            else:
                pygame.draw.rect(self.ecran, tuple(max(0, c-60) for c in col_c), r_c, 1, border_radius=9)

        # ── Slots stickers ────────────────────────────────────────────────────
        SLOTS_Y  = pal_start_y + 2 * (PALETTE_SIZE + PALETTE_PAD) + 28
        if not hasattr(self, "_perso_slot_actif"):
            self._perso_slot_actif = 0
        START_SX = 30
        lbl_stk_titre = self.fonte_sous_titre.render("Stickers du bol :", True, ROSE_PASS)
        self.ecran.blit(lbl_stk_titre, (START_SX, SLOTS_Y - 28))
        for si in range(MAX_SLOTS_STICKERS):
            sr = pygame.Rect(START_SX + si * 240, SLOTS_Y, 220, 42)
            is_sel = (self._perso_slot_actif == si)
            bg_s = ROSE_PASS if is_sel else (50, 50, 70)
            pygame.draw.rect(self.ecran, bg_s, sr, border_radius=10)
            pygame.draw.rect(self.ecran, BLANC, sr, 2, border_radius=10)
            stk_in_slot = slots[si]
            stk_label = stk_in_slot if stk_in_slot else "vide"
            lbl = self.fonte_petite.render(f"Slot {si+1} : {stk_label}", True, NOIR if is_sel else BLANC)
            self.ecran.blit(lbl, lbl.get_rect(center=sr.center))

        btn_eff = pygame.Rect(START_SX, SLOTS_Y + 50, 200, 32)
        h_eff = btn_eff.collidepoint(souris)
        pygame.draw.rect(self.ecran, ROUGE if h_eff else (100, 30, 30), btn_eff, border_radius=8)
        pygame.draw.rect(self.ecran, BLANC, btn_eff, 2, border_radius=8)
        self.ecran.blit(self.fonte_petite.render("Effacer ce slot", True, BLANC),
                        self.fonte_petite.render("Effacer ce slot", True, BLANC).get_rect(center=btn_eff.center))

        # ── Grille stickers ───────────────────────────────────────────────────
        STICKERS_Y = SLOTS_Y + 92
        COLS_S  = 5
        CARD_SW = 175
        CARD_SH = 155
        PAD_SX  = (780 - COLS_S * CARD_SW) // (COLS_S + 1)
        for idx_s, stk_info in enumerate(STICKERS_CATALOGUE):
            col_s = idx_s % COLS_S
            row_s = idx_s // COLS_S
            bx_s  = START_SX + PAD_SX + col_s * (CARD_SW + PAD_SX)
            by_s  = STICKERS_Y + row_s * (CARD_SH + 12)
            achete_s  = stk_info["id"] in stickers_achetes
            hover_s   = pygame.Rect(bx_s, by_s, CARD_SW, CARD_SH).collidepoint(souris)
            selec_s   = any(s == stk_info["id"] for s in slots)
            bg_card = (30, 50, 30) if selec_s else ((45, 45, 65) if achete_s else (35, 35, 50))
            if hover_s and achete_s:
                bg_card = tuple(min(255, c + 20) for c in bg_card)
            pygame.draw.rect(self.ecran, bg_card, (bx_s, by_s, CARD_SW, CARD_SH), border_radius=12)
            bord_c = VERT if selec_s else (OR if achete_s else GRIS)
            pygame.draw.rect(self.ecran, bord_c, (bx_s, by_s, CARD_SW, CARD_SH), 2, border_radius=12)
            tmp_bol._dessiner_sticker_custom(self.ecran, bx_s + CARD_SW // 2, by_s + 50, 22, stk_info["id"], now)
            nom_stk = self.fonte_petite.render(stk_info["nom"], True, BLANC)
            self.ecran.blit(nom_stk, nom_stk.get_rect(center=(bx_s + CARD_SW // 2, by_s + 85)))
            btn_stk = pygame.Rect(bx_s + 18, by_s + CARD_SH - 40, CARD_SW - 36, 30)
            if achete_s:
                pygame.draw.rect(self.ecran, VERT, btn_stk, border_radius=7)
                pygame.draw.rect(self.ecran, BLANC, btn_stk, 1, border_radius=7)
                lbl_b = self.fonte_petite.render("Mettre sur le bol", True, NOIR)
            else:
                peut_s = self.boutique["pieces"] >= stk_info["prix"]
                bg_b = (100, 70, 0) if peut_s else (50, 50, 50)
                pygame.draw.rect(self.ecran, bg_b, btn_stk, border_radius=7)
                pygame.draw.rect(self.ecran, OR if peut_s else GRIS, btn_stk, 1, border_radius=7)
                lbl_b = self.fonte_petite.render(f"Acheter {stk_info['prix']}p", True, OR if peut_s else GRIS)
            self.ecran.blit(lbl_b, lbl_b.get_rect(center=btn_stk.center))

        # ── Bouton retour ─────────────────────────────────────────────────────
        btn_retour = pygame.Rect(40, HAUTEUR - 72, 200, 50)
        h_ret = btn_retour.collidepoint(souris)
        pygame.draw.rect(self.ecran, ROUGE if h_ret else (120, 30, 30), btn_retour, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn_retour, 2, border_radius=12)
        self.ecran.blit(self.fonte_sous_titre.render("<< Retour", True, BLANC),
                        self.fonte_sous_titre.render("<< Retour", True, BLANC).get_rect(center=btn_retour.center))

        # ── Overlay first-time ────────────────────────────────────────────────
        if not self._tuto_perso_vu:
            self._dessiner_overlay_firsttime(
                "PERSONNALISATION DU BOL",
                ROSE_PASS,
                [
                    "Ici tu peux personnaliser ton bol !",
                    "",
                    "  Couleur : choisis la couleur de ton bol",
                    "  parmi la palette en haut.",
                    "",
                    "  Stickers : tu as 3 emplacements.",
                    "  Clique sur un slot pour le selectionner,",
                    "  puis clique sur un sticker pour l'equiper.",
                    "",
                    "  Certains stickers sont gratuits (etoile),",
                    "  les autres s'achtent avec des pieces.",
                ],
            )
            btn_ok_ft = pygame.Rect(LARGEUR//2 - 130, HAUTEUR//2 + 200, 260, 52)
            souris_ft = pygame.mouse.get_pos()
            h_ft = btn_ok_ft.collidepoint(souris_ft)
            pygame.draw.rect(self.ecran, ROSE_PASS if h_ft else (130, 20, 100), btn_ok_ft, border_radius=14)
            pygame.draw.rect(self.ecran, BLANC, btn_ok_ft, 2, border_radius=14)
            self.ecran.blit(self.fonte_sous_titre.render("Compris !", True, BLANC),
                            self.fonte_sous_titre.render("Compris !", True, BLANC).get_rect(center=btn_ok_ft.center))
            for ev_ft in pygame.event.get():
                if ev_ft.type == pygame.QUIT:
                    return False
                if ev_ft.type == pygame.MOUSEBUTTONDOWN and btn_ok_ft.collidepoint(ev_ft.pos):
                    self._tuto_perso_vu = True
            return True

        # ── Événements ────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._sauvegarder_boutique()
                self.scene = "accueil"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retour.collidepoint(event.pos):
                    self._sauvegarder_boutique()
                    self.scene = "accueil"
                # Palette couleur
                for r_c, col_c in pal_rects:
                    if r_c.collidepoint(event.pos):
                        self.boutique["bol_perso_couleur"] = list(col_c)
                        self._sauvegarder_boutique()
                # Slots
                for si in range(MAX_SLOTS_STICKERS):
                    sr_ev = pygame.Rect(START_SX + si * 240, SLOTS_Y, 220, 42)
                    if sr_ev.collidepoint(event.pos):
                        self._perso_slot_actif = si
                slots_ev = self.boutique.get("stickers_slots", [None, None, None])
                if len(slots_ev) < MAX_SLOTS_STICKERS:
                    slots_ev = (slots_ev + [None]*MAX_SLOTS_STICKERS)[:MAX_SLOTS_STICKERS]
                if btn_eff.collidepoint(event.pos):
                    slots_ev[self._perso_slot_actif] = None
                    self.boutique["stickers_slots"] = slots_ev
                    self._sauvegarder_boutique()
                # Grille stickers
                stickers_achetes_ev = self.boutique.get("stickers_achetes", ["etoile"])
                for idx_s2, stk_info2 in enumerate(STICKERS_CATALOGUE):
                    col_s2 = idx_s2 % COLS_S
                    row_s2 = idx_s2 // COLS_S
                    bx_s2  = START_SX + PAD_SX + col_s2 * (CARD_SW + PAD_SX)
                    by_s2  = STICKERS_Y + row_s2 * (CARD_SH + 12)
                    btn_stk2 = pygame.Rect(bx_s2 + 18, by_s2 + CARD_SH - 40, CARD_SW - 36, 30)
                    if btn_stk2.collidepoint(event.pos):
                        sid = stk_info2["id"]
                        if sid in stickers_achetes_ev:
                            slots_ev[self._perso_slot_actif] = sid
                            self.boutique["stickers_slots"] = slots_ev
                            self._sauvegarder_boutique()
                        elif self.boutique["pieces"] >= stk_info2["prix"]:
                            self.boutique["pieces"] -= stk_info2["prix"]
                            stickers_achetes_ev.append(sid)
                            self.boutique["stickers_achetes"] = stickers_achetes_ev
                            slots_ev[self._perso_slot_actif] = sid
                            self.boutique["stickers_slots"] = slots_ev
                            self._sauvegarder_boutique()
        return True

    def scene_boutique(self):
        """Boutique : skins + ameliorations permanentes."""
        self._dessiner_fond()
        self._dessiner_sol()
        now    = pygame.time.get_ticks()
        souris = pygame.mouse.get_pos()

        # ---- Header ----------------------------------------------------------
        ban = pygame.Surface((LARGEUR, 115), pygame.SRCALPHA)
        ban.fill((0, 0, 0, 150))
        self.ecran.blit(ban, (0, 0))

        titre_surf = self.fonte_titre.render("BOUTIQUE", True, OR)
        self.ecran.blit(titre_surf, titre_surf.get_rect(center=(LARGEUR // 2, 58)))

        # Pieces dispo
        p_txt = self.fonte_sous_titre.render(f"Pieces disponibles : {self.boutique['pieces']}", True, OR)
        self.ecran.blit(p_txt, p_txt.get_rect(topright=(LARGEUR - 25, 18)))

        # ---- Onglets ---------------------------------------------------------
        onglets = ["SKINS", "AMELIORATIONS"]
        ong_rects = []
        for i, lab in enumerate(onglets):
            r = pygame.Rect(LARGEUR // 2 - 260 + i * 270, 125, 250, 42)
            ong_rects.append(r)
            actif = (self.tuto_boutique == i)
            pygame.draw.rect(self.ecran, OR if actif else (60, 60, 80), r, border_radius=10)
            pygame.draw.rect(self.ecran, BLANC, r, 2, border_radius=10)
            surf_l = self.fonte_sous_titre.render(lab, True, NOIR if actif else BLANC)
            self.ecran.blit(surf_l, surf_l.get_rect(center=r.center))

        # ---- Contenu selon onglet --------------------------------------------
        skin_btn_rects = {}  # initialise avant le if/else pour eviter UnboundLocalError
        if self.tuto_boutique == 0:
            # ===================== ONGLET SKINS ============================
            txt_h = self.fonte_sous_titre.render("Choisis ton bol !", True, BLANC)
            self.ecran.blit(txt_h, txt_h.get_rect(center=(LARGEUR // 2, 150)))

            skins_liste = list(Bol.SKINS.items())
            # Affichage en grille 5 colonnes x 3 lignes
            COLS   = 5
            CARD_W = 210
            CARD_H = 165
            PAD_X  = (LARGEUR - COLS * CARD_W) // (COLS + 1)
            ROW_START_Y = 210

            skin_btn_rects = {}
            for idx, (cle, info) in enumerate(skins_liste):
                col = idx % COLS
                row = idx // COLS
                cx  = PAD_X + col * (CARD_W + PAD_X) + CARD_W // 2
                cy  = ROW_START_Y + row * (CARD_H + 8) + 60

                achete = cle in self.boutique["skins_achetes"]
                actif  = (self.boutique["skin_actif"] == cle)
                coul   = info["couleur"]
                coul_f = tuple(max(0, int(c * 0.65)) for c in coul)
                coul_l = tuple(min(255, int(c * 1.25 + 20)) for c in coul)
                forme  = info.get("forme", "classic")
                sticker= info.get("sticker", None)

                # Fond de carte
                card_rect = pygame.Rect(cx - CARD_W // 2, cy - 68, CARD_W, CARD_H)
                bg_col = (20, 45, 20) if actif else (20, 20, 40)
                pygame.draw.rect(self.ecran, bg_col, card_rect, border_radius=12)
                bord_c = VERT if actif else (coul_f if achete else (60, 60, 80))
                pygame.draw.rect(self.ecran, bord_c, card_rect, 2, border_radius=12)

                # Halo si actif
                if actif:
                    pulse = 0.5 + 0.5 * math.sin(now / 250)
                    r_cercle = 32
                    r_h = int(r_cercle + 5 + 3 * pulse)
                    surf_h = pygame.Surface((r_h * 2 + 4, r_h * 2 + 4), pygame.SRCALPHA)
                    pygame.draw.circle(surf_h, (*coul, 90), (r_h + 2, r_h + 2), r_h)
                    self.ecran.blit(surf_h, (cx - r_h - 2, cy - r_h - 2 - 10))

                # Preview : mini bol selon la forme
                r_cercle = 28
                preview_cx = cx
                preview_cy = cy - 14

                if forme == "carre":
                    # Rectangle arrondi en bas pour simuler bol cube
                    rw, rh = r_cercle + 8, r_cercle + 4
                    pts_c = [
                        (preview_cx - rw, preview_cy - rh // 2),
                        (preview_cx + rw, preview_cy - rh // 2),
                        (preview_cx + rw, preview_cy + rh // 2),
                        (preview_cx + rw - 8, preview_cy + rh),
                        (preview_cx - rw + 8, preview_cy + rh),
                        (preview_cx - rw, preview_cy + rh // 2),
                    ]
                    pygame.draw.polygon(self.ecran, coul,  pts_c)
                    pygame.draw.polygon(self.ecran, coul_f, pts_c, 2)
                    pygame.draw.ellipse(self.ecran, coul_l,
                                        (preview_cx - rw + 4, preview_cy - rh // 2 - 4, rw * 2 - 8, 10))
                elif forme == "large":
                    rw, rh = r_cercle + 14, r_cercle - 8
                    pygame.draw.ellipse(self.ecran, coul_f, (preview_cx - rw - 2, preview_cy - rh + 2, (rw + 2) * 2, rh * 2 + 4))
                    pygame.draw.ellipse(self.ecran, coul,   (preview_cx - rw,     preview_cy - rh,     rw * 2,       rh * 2))
                    pygame.draw.ellipse(self.ecran, coul_l, (preview_cx - rw + 6, preview_cy - rh + 4, rw * 2 - 12,  rh - 4))
                    pygame.draw.ellipse(self.ecran, coul_f, (preview_cx - rw,     preview_cy - rh,     rw * 2,       rh * 2), 2)
                elif forme == "profond":
                    rw, rh = r_cercle - 8, r_cercle + 14
                    pygame.draw.ellipse(self.ecran, coul_f, (preview_cx - rw - 2, preview_cy - rh // 2 + 2, (rw + 2) * 2, rh * 2 + 4))
                    pygame.draw.ellipse(self.ecran, coul,   (preview_cx - rw,     preview_cy - rh // 2,     rw * 2,       rh * 2))
                    pygame.draw.ellipse(self.ecran, coul_l, (preview_cx - rw + 4, preview_cy - rh // 2 + 4, rw * 2 - 8,   rh - 4))
                    pygame.draw.ellipse(self.ecran, coul_f, (preview_cx - rw,     preview_cy - rh // 2,     rw * 2,       rh * 2), 2)
                elif forme == "hexagonal":
                    import math as _m2
                    hex_pts = []
                    for ki in range(6):
                        a = _m2.radians(ki * 60 - 30)
                        hex_pts.append((int(preview_cx + _m2.cos(a) * (r_cercle + 2)),
                                        int(preview_cy + _m2.sin(a) * (r_cercle - 2))))
                    pygame.draw.polygon(self.ecran, coul,  hex_pts)
                    pygame.draw.polygon(self.ecran, coul_l, hex_pts[0:3])
                    pygame.draw.polygon(self.ecran, coul_f, hex_pts, 2)
                else:
                    # classic
                    pygame.draw.circle(self.ecran, coul_f, (preview_cx, preview_cy), r_cercle + 3)
                    pygame.draw.circle(self.ecran, coul,   (preview_cx, preview_cy), r_cercle)
                    pygame.draw.circle(self.ecran, coul_l, (preview_cx, preview_cy), r_cercle - 8)
                    pygame.draw.ellipse(self.ecran, tuple(min(255, c + 80) for c in coul),
                                        (preview_cx - 14, preview_cy - 20, 20, 12))
                    pygame.draw.circle(self.ecran, coul_f, (preview_cx, preview_cy), r_cercle, 2)

                # Mini stickers sur preview
                if sticker == "etoiles":
                    for sk in [(-12, -4), (10, 0), (0, 12)]:
                        pygame.draw.circle(self.ecran, (255, 230, 0),
                                           (preview_cx + sk[0], preview_cy + sk[1]), 3)
                elif sticker == "coeurs":
                    pygame.draw.circle(self.ecran, (255, 80, 150), (preview_cx - 6, preview_cy + 4), 4)
                    pygame.draw.circle(self.ecran, (255, 80, 150), (preview_cx + 6, preview_cy + 4), 4)
                elif sticker == "feu":
                    pygame.draw.polygon(self.ecran, (255, 140, 0),
                                        [(preview_cx - 4, preview_cy - 2),
                                         (preview_cx,     preview_cy - 12),
                                         (preview_cx + 4, preview_cy - 2)])
                elif sticker == "galaxy":
                    for gk, gc in [(-8, (180, 100, 255)), (8, (100, 200, 255)), (0, (255, 200, 100))]:
                        pygame.draw.circle(self.ecran, gc,
                                           (preview_cx + gk, preview_cy + 4), 2)

                # Nom
                nom_s = self.fonte_petite.render(info["nom"], True, BLANC)
                self.ecran.blit(nom_s, nom_s.get_rect(center=(cx, cy + r_cercle + 8)))

                # Bouton achat / equiper
                pass_only = info.get("pass_only", False)
                btn_r = pygame.Rect(cx - 52, cy + r_cercle + 20, 104, 28)
                skin_btn_rects[cle] = btn_r

                if actif:
                    pygame.draw.rect(self.ecran, VERT, btn_r, border_radius=6)
                    pygame.draw.rect(self.ecran, BLANC, btn_r, 2, border_radius=6)
                    t_btn = self.fonte_petite.render("EQUIPE", True, BLANC)
                elif achete:
                    hover = btn_r.collidepoint(souris)
                    pygame.draw.rect(self.ecran, (50, 120, 50) if hover else (30, 80, 30), btn_r, border_radius=6)
                    pygame.draw.rect(self.ecran, BLANC, btn_r, 2, border_radius=6)
                    t_btn = self.fonte_petite.render("EQUIPPER", True, BLANC)
                elif pass_only:
                    # Skin exclusif Pass Royal — non achetable ici
                    pygame.draw.rect(self.ecran, (40, 20, 70), btn_r, border_radius=6)
                    pygame.draw.rect(self.ecran, VIOLET_PASS, btn_r, 2, border_radius=6)
                    t_btn = self.fonte_petite.render("* PASS", True, (180, 130, 255))
                    # Superposer un cadenas sur l'aperçu du bol
                    cadenas_r = pygame.Rect(cx - 12, cy - 26, 24, 24)
                    pygame.draw.rect(self.ecran, (20, 15, 40), cadenas_r, border_radius=4)
                    pygame.draw.rect(self.ecran, VIOLET_PASS, cadenas_r, 2, border_radius=4)
                    # Cadenas dessine (emoji non supporté par pygame)
                    _cx, _cy = cadenas_r.centerx, cadenas_r.centery
                    # Corps du cadenas
                    pygame.draw.rect(self.ecran, (180, 130, 255),
                                     (_cx - 6, _cy - 1, 12, 9), border_radius=2)
                    # Arceau du cadenas
                    pygame.draw.arc(self.ecran, (180, 130, 255),
                                    (_cx - 5, _cy - 9, 10, 10),
                                    0, 3.14159, 2)
                else:
                    peut = self.boutique["pieces"] >= info["prix"]
                    hover = btn_r.collidepoint(souris)
                    bg = (140, 100, 0) if (peut and hover) else ((100, 70, 0) if peut else (60, 60, 60))
                    pygame.draw.rect(self.ecran, bg, btn_r, border_radius=6)
                    pygame.draw.rect(self.ecran, OR if peut else GRIS, btn_r, 2, border_radius=6)
                    t_btn = self.fonte_petite.render(f"{info['prix']}p", True, OR if peut else GRIS)
                self.ecran.blit(t_btn, t_btn.get_rect(center=btn_r.center))

        elif self.tuto_boutique == 1:
            # ===================== ONGLET AMELIORATIONS =====================
            upgrades = [
                {
                    "cle": "taille_niveau",
                    "titre": "TAILLE DU BOL",
                    "icone": "T",
                    "couleur": (30, 150, 220),
                    "desc_niveaux": ["Standard (defaut)", "+20 px de largeur", "+40 px de largeur"],
                    "couts": [0, 150, 500],
                    "max": 2,
                },
                {
                    "cle": "vitesse_niveau",
                    "titre": "VITESSE DU BOL",
                    "icone": "V",
                    "couleur": (220, 100, 30),
                    "desc_niveaux": ["Standard (defaut)", "+2 pts de vitesse", "+4 pts de vitesse"],
                    "couts": [0, 120, 400],
                    "max": 2,
                },
                {
                    "cle": "combo_niveau",
                    "titre": "BONUS COMBO",
                    "icone": "C",
                    "couleur": (200, 60, 200),
                    "desc_niveaux": ["Aucun bonus", "+3 pieces par combo x3+", "+7 pieces par combo x3+"],
                    "couts": [0, 350, 900],
                    "max": 2,
                },
                {
                    "cle": "pieces_niveau",
                    "titre": "MULTIPLICATEUR PIECES",
                    "icone": "M",
                    "couleur": (200, 175, 0),
                    "desc_niveaux": ["x1 (normal)", "x1.6 pieces gagnees", "x2.5 pieces gagnees"],
                    "couts": [0, 500, 1400],
                    "max": 2,
                },
            ]

            # Grille 2x2
            COLS_UP = 2
            UPG_W, UPG_H = 545, 290
            UPG_PAD_X = (LARGEUR - COLS_UP * UPG_W) // (COLS_UP + 1)
            UPG_PAD_Y = 10

            for idx, upg in enumerate(upgrades):
                col_u = idx % COLS_UP
                row_u = idx // COLS_UP
                bx = UPG_PAD_X + col_u * (UPG_W + UPG_PAD_X)
                by = 175 + row_u * (UPG_H + UPG_PAD_Y)
                bw, bh = UPG_W, UPG_H

                coul = upg["couleur"]
                coul_f = tuple(max(0, int(c * 0.65)) for c in coul)
                niveau_actuel = self.boutique.get(upg["cle"], 0)

                # Carte fond
                pygame.draw.rect(self.ecran, (20, 20, 40), (bx, by, bw, bh), border_radius=14)
                pygame.draw.rect(self.ecran, coul, (bx, by, bw, bh), 3, border_radius=14)

                # Icone + titre
                f_ico = pygame.font.Font(None, 46)
                ico_s = f_ico.render(upg["icone"], True, coul)
                self.ecran.blit(ico_s, ico_s.get_rect(center=(bx + 38, by + 32)))
                t_h = self.fonte_sous_titre.render(upg["titre"], True, coul)
                self.ecran.blit(t_h, t_h.get_rect(midleft=(bx + 62, by + 32)))

                # Barre de progression
                bar_x, bar_y, bar_w, bar_h2 = bx + 25, by + 60, bw - 50, 14
                pygame.draw.rect(self.ecran, (50, 50, 70), (bar_x, bar_y, bar_w, bar_h2), border_radius=7)
                rempli = int(bar_w * niveau_actuel / upg["max"])
                if rempli > 0:
                    pygame.draw.rect(self.ecran, coul, (bar_x, bar_y, rempli, bar_h2), border_radius=7)
                pygame.draw.rect(self.ecran, BLANC, (bar_x, bar_y, bar_w, bar_h2), 2, border_radius=7)
                niv_txt = self.fonte_petite.render(f"Niveau {niveau_actuel}/{upg['max']}", True, BLANC)
                self.ecran.blit(niv_txt, niv_txt.get_rect(center=(bx + bw // 2, bar_y + bar_h2 // 2)))

                # Niveaux - hauteur compacte
                for lv in range(upg["max"] + 1):
                    ly = by + 85 + lv * 65
                    debloque = (lv <= niveau_actuel)
                    actif_lv = (lv == niveau_actuel)

                    pygame.draw.rect(self.ecran,
                                     (30, 50, 30) if debloque else (35, 35, 55),
                                     (bx + 15, ly, bw - 30, 58), border_radius=8)
                    bord_c = VERT if debloque else (80, 80, 100)
                    pygame.draw.rect(self.ecran, bord_c, (bx + 15, ly, bw - 30, 58), 2, border_radius=8)

                    puce = self.fonte_texte.render(f"Lv{lv}", True, coul if actif_lv else BLANC)
                    self.ecran.blit(puce, (bx + 25, ly + 8))
                    desc = self.fonte_texte.render(upg["desc_niveaux"][lv], True, BLANC)
                    self.ecran.blit(desc, (bx + 68, ly + 8))

                    if lv == 0:
                        etat = self.fonte_petite.render("GRATUIT", True, VERT)
                        self.ecran.blit(etat, etat.get_rect(midright=(bx + bw - 20, ly + 30)))
                    elif debloque:
                        etat = self.fonte_petite.render("DEJA ACHETE", True, VERT)
                        self.ecran.blit(etat, etat.get_rect(midright=(bx + bw - 20, ly + 30)))
                    else:
                        cout = upg["couts"][lv]
                        peut = (self.boutique["pieces"] >= cout and lv == niveau_actuel + 1)
                        btn_up = pygame.Rect(bx + bw - 145, ly + 14, 125, 28)
                        if lv == niveau_actuel + 1:
                            hover = btn_up.collidepoint(souris)
                            bg = (140, 100, 0) if (peut and hover) else ((100, 70, 0) if peut else (50, 50, 50))
                            pygame.draw.rect(self.ecran, bg, btn_up, border_radius=7)
                            pygame.draw.rect(self.ecran, OR if peut else GRIS, btn_up, 2, border_radius=7)
                            t_cout = self.fonte_petite.render(f"Acheter {cout}p", True, OR if peut else GRIS)
                            self.ecran.blit(t_cout, t_cout.get_rect(center=btn_up.center))
                            upg["_btn_rect"] = btn_up
                            upg["_btn_lv"]   = lv
                            upg["_btn_peut"] = peut
                        else:
                            verr = self.fonte_petite.render("Niveau precedent requis", True, (100, 100, 120))
                            self.ecran.blit(verr, verr.get_rect(midright=(bx + bw - 20, ly + 30)))

        # ---- Bouton Retour ---------------------------------------------------
        btn_retour = pygame.Rect(40, HAUTEUR - 72, 200, 50)
        h_ret = btn_retour.collidepoint(souris)
        pygame.draw.rect(self.ecran, ROUGE if h_ret else (120, 30, 30), btn_retour, border_radius=12)
        pygame.draw.rect(self.ecran, BLANC, btn_retour, 2, border_radius=12)
        t_ret = self.fonte_sous_titre.render("<< Retour", True, BLANC)
        self.ecran.blit(t_ret, t_ret.get_rect(center=btn_retour.center))

        # ---- Gestion evenements ----------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene = "accueil"
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Onglets
                for i, r in enumerate(ong_rects):
                    if r.collidepoint(event.pos):
                        self.tuto_boutique = i

                # Retour
                if btn_retour.collidepoint(event.pos):
                    self._sauvegarder_boutique()
                    self.scene = "accueil"

                # Skins
                if self.tuto_boutique == 0:
                    for cle, r in skin_btn_rects.items():
                        if r.collidepoint(event.pos):
                            achete    = cle in self.boutique["skins_achetes"]
                            info      = Bol.SKINS[cle]
                            pass_only = info.get("pass_only", False)
                            if achete:
                                self.boutique["skin_actif"] = cle
                                self._sauvegarder_boutique()
                            elif pass_only:
                                pass  # skins pass : non achetables ici
                            elif self.boutique["pieces"] >= info["prix"]:
                                self.boutique["pieces"] -= info["prix"]
                                self.boutique["skins_achetes"].append(cle)
                                self.boutique["skin_actif"] = cle
                                self._sauvegarder_boutique()

                # Ameliorations
                elif self.tuto_boutique == 1:
                    upgrades_loc = [
                        {"cle": "taille_niveau",   "couts": [0, 150, 500],  "max": 2},
                        {"cle": "vitesse_niveau",  "couts": [0, 120, 400],  "max": 2},
                        {"cle": "combo_niveau",    "couts": [0, 350, 900],  "max": 2},
                        {"cle": "pieces_niveau",   "couts": [0, 500, 1400], "max": 2},
                    ]
                    COLS_UP2 = 2
                    UPG_W2   = 545
                    UPG_H2   = 290
                    UPG_PX2  = (LARGEUR - COLS_UP2 * UPG_W2) // (COLS_UP2 + 1)
                    for upg in upgrades_loc:
                        niv = self.boutique.get(upg["cle"], 0)
                        if niv < upg["max"]:
                            idx2    = upgrades_loc.index(upg)
                            col_u2  = idx2 % COLS_UP2
                            row_u2  = idx2 // COLS_UP2
                            bx2 = UPG_PX2 + col_u2 * (UPG_W2 + UPG_PX2)
                            by2 = 175 + row_u2 * (UPG_H2 + 10)
                            lv_cible = niv + 1
                            ly2 = by2 + 85 + lv_cible * 65
                            btn_up2 = pygame.Rect(bx2 + UPG_W2 - 145, ly2 + 14, 125, 28)
                            cout2 = upg["couts"][lv_cible]
                            if btn_up2.collidepoint(event.pos) and self.boutique["pieces"] >= cout2:
                                self.boutique["pieces"] -= cout2
                                self.boutique[upg["cle"]] = self.boutique.get(upg["cle"], 0) + 1
                                self._sauvegarder_boutique()

        # ---- Overlay first-time boutique -------------------------------------
        if not self._tuto_boutique_vu:
            self._dessiner_overlay_firsttime(
                "BIENVENUE DANS LA BOUTIQUE !",
                OR,
                [
                    "Ici tu peux depenser tes pieces pour personnaliser",
                    "ton experience de jeu.",
                    "",
                    "  SKINS  : change l'apparence de ton bol.",
                    "  Choisis parmi 14 bols differents !",
                    "",
                    "  AMELIORATIONS  : ameliore ton bol en permanence.",
                    "  Taille, vitesse, multiplicateur de pieces...",
                    "",
                    "Les pieces se gagnent en attrapant des aliments.",
                    "Plus ton combo est haut, plus tu en gagnes !",
                ],
            )
            btn_ok_ft = pygame.Rect(LARGEUR//2 - 130, HAUTEUR//2 + 200, 260, 52)
            souris_ft = pygame.mouse.get_pos()
            h_ft = btn_ok_ft.collidepoint(souris_ft)
            pygame.draw.rect(self.ecran, OR if h_ft else (120, 80, 0), btn_ok_ft, border_radius=14)
            pygame.draw.rect(self.ecran, BLANC, btn_ok_ft, 2, border_radius=14)
            self.ecran.blit(self.fonte_sous_titre.render("Compris !", True, BLANC),
                            self.fonte_sous_titre.render("Compris !", True, BLANC).get_rect(center=btn_ok_ft.center))
            for ev_ft in pygame.event.get():
                if ev_ft.type == pygame.QUIT:
                    return False
                if ev_ft.type == pygame.MOUSEBUTTONDOWN and btn_ok_ft.collidepoint(ev_ft.pos):
                    self._tuto_boutique_vu = True
            return True

        return True

    # -- Boucle principale -------------------------------------------------
    def lancer(self):
        en_cours = True
        try:
            while en_cours:
                if   self.scene == "accueil":    en_cours = self.scene_accueil()
                elif self.scene == "tuto":       en_cours = self.scene_tuto()
                elif self.scene == "choix_bol":  en_cours = self.scene_choix_bol()
                elif self.scene == "boutique":   en_cours = self.scene_boutique()
                elif self.scene == "perso":      en_cours = self.scene_perso()
                elif self.scene == "pass":       en_cours = self.scene_pass()
                elif self.scene == "boites":     en_cours = self.scene_boites()
                elif self.scene == "countdown":  en_cours = self.scene_countdown()
                elif self.scene == "jeu":        en_cours = self.scene_jeu()
                elif self.scene == "pause":      en_cours = self.scene_pause()
                elif self.scene == "gameover":   en_cours = self.scene_gameover()
                elif self.scene == "resultats":  en_cours = self.scene_resultats()
                pygame.display.flip()
                self.horloge.tick(FPS)
        except Exception as e:
            print(f"Erreur : {e}")
            import traceback; traceback.print_exc()
        finally:
            # Reinitialisation complete : suppression des sauvegardes
            import os
            for f in ("meilleur_score.txt", "boutique.json"):
                try:
                    os.remove(f)
                except Exception:
                    pass
            pygame.quit()


if __name__ == "__main__":
    print("Lancement de LA COURSE DU PETIT-DEJEUNER - Version Endless !")
    JeuPetitDej().lancer()
    print("Merci d'avoir joue !")