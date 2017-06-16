#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

if len(sys.argv) != 3:
	print "Mauvais nombre d'arguments"
	exit()

#Les espaces dans les noms de fichier, c'est le mal
DOSSIER_PHOTOS_ORIGINALES = "../photos/" + sys.argv[1]
DOSSIER_PHOTOS_FINALES = "../watermarked/" + sys.argv[1]

CHEMIN_WATERMARK = "../assets/watermark.png"

LARGEUR_MAX_PHOTOS_FINALES = 400 * 4
HAUTEUR_MAX_PHOTOS_FINALES = 300 * 4

# TEXTE = u"  © BDE Saint Jérôme - Tous droits réservés"
TEXTE = sys.argv[2].decode("utf-8") #u"  12/11/2014 - Soirée Contrée - BDE Saint Jérôme"
CHEMIN_POLICE_TEXTE = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"

EXTENSION_FICHIERS_FINAUX = ".jpg"

print "Test d'ouverture des dossiers..."

if not os.path.isdir(DOSSIER_PHOTOS_ORIGINALES):
	print "Dossier " + DOSSIER_PHOTOS_ORIGINALES + " introuvable"
	exit()

if not os.path.isdir(DOSSIER_PHOTOS_FINALES):
	print "Dossier " + DOSSIER_PHOTOS_FINALES + " introuvable"
	exit()

if DOSSIER_PHOTOS_ORIGINALES == DOSSIER_PHOTOS_FINALES:
	print "Dossier de destination et dossier source identiques"
	exit()

print "Chargement du watermark..."

if not os.path.isfile(CHEMIN_WATERMARK):
	print "Le watermark " + CHEMIN_WATERMARK + " n'est pas un fichier"
	exit()

print "Ouverture du watermark..."

IMAGE_WATERMARK_ORIGINAL = Image.open(CHEMIN_WATERMARK)
IMAGE_WATERMARK_ORIGINAL.load()

IMAGE_WATERMARK = IMAGE_WATERMARK_ORIGINAL

print "Démarrage du parcours du dossier de photos..."

LISTE_PHOTOS = os.listdir(DOSSIER_PHOTOS_ORIGINALES)
for NOM_PHOTO in LISTE_PHOTOS:

#NOM_PHOTO = sys.argv[2]

	CHEMIN_PHOTO = DOSSIER_PHOTOS_ORIGINALES + "/" + NOM_PHOTO
	if not os.path.isfile(CHEMIN_PHOTO):
		print "La photo originale " + NOM_PHOTO + " n'est pas un fichier"
		exit()

	print NOM_PHOTO + ": Chargement de l'image..."
	IMAGE_PHOTO = Image.open(CHEMIN_PHOTO)
	IMAGE_PHOTO.load()

	print NOM_PHOTO + ": Rotation de l'image selon les données EXIF..."

	IMAGE_PHOTO_EXIF_DATA = IMAGE_PHOTO._getexif()
	orientation_key = 274 # cf ExifTags
	if orientation_key in IMAGE_PHOTO_EXIF_DATA:
		orientation = IMAGE_PHOTO_EXIF_DATA[orientation_key]

		rotate_values = {
			3: 180,
			6: 270,
			8: 90
		}

		if orientation in rotate_values:
			# Rotate and save the picture
			IMAGE_PHOTO = IMAGE_PHOTO.rotate(rotate_values[orientation])
			print NOM_PHOTO + ": Image tournée de", rotate_values[orientation],"degrés"

	# Réduction de la résolution de la photo
	#IMAGE_PHOTO = IMAGE_PHOTO.resize([e/2 for e in IMAGE_PHOTO.size])

	print NOM_PHOTO + ": Mise à l'échelle de l'image..."
	LARGEUR_PHOTO,HAUTEUR_PHOTO = IMAGE_PHOTO.size

	if LARGEUR_PHOTO > LARGEUR_MAX_PHOTOS_FINALES or HAUTEUR_MAX_PHOTOS_FINALES:
		RATIO = LARGEUR_MAX_PHOTOS_FINALES/HAUTEUR_MAX_PHOTOS_FINALES
		A = (LARGEUR_MAX_PHOTOS_FINALES, HAUTEUR_PHOTO * LARGEUR_MAX_PHOTOS_FINALES / LARGEUR_PHOTO)
		B = (LARGEUR_PHOTO * HAUTEUR_MAX_PHOTOS_FINALES / HAUTEUR_PHOTO, HAUTEUR_MAX_PHOTOS_FINALES)
		if A[1] > HAUTEUR_MAX_PHOTOS_FINALES and B[0] <= LARGEUR_MAX_PHOTOS_FINALES:
			IMAGE_PHOTO = IMAGE_PHOTO.resize(B, Image.ANTIALIAS)
			#LARGEUR_PHOTO,HAUTEUR_PHOTO = B
		else:
			if B[0] > LARGEUR_MAX_PHOTOS_FINALES and A[1] <= HAUTEUR_MAX_PHOTOS_FINALES:
				IMAGE_PHOTO = IMAGE_PHOTO.resize(A, Image.ANTIALIAS)
				#LARGEUR_PHOTO,HAUTEUR_PHOTO = A
			else:
				print NOM_PHOTO + ": Erreur dans le calcul des proportions"
				exit()

	LARGEUR_PHOTO,HAUTEUR_PHOTO = IMAGE_PHOTO.size

	# Calcul de la taille du watermark
	print NOM_PHOTO + ": Mise à l'échelle du Watermark..."
	if LARGEUR_PHOTO >= HAUTEUR_PHOTO:
		POSITION_WATERMARK_X = 0
		POSITION_WATERMARK_Y = -1

		LARGEUR_WATERMARK,HAUTEUR_WATERMARK = IMAGE_WATERMARK.size
		HAUTEUR_WATERMARK_REDIM = (int) (HAUTEUR_PHOTO * 0.1)
		LARGEUR_WATERMARK_REDIM = (int) (((1.0*LARGEUR_WATERMARK) / HAUTEUR_WATERMARK) * HAUTEUR_WATERMARK_REDIM)
		IMAGE_WATERMARK_REDIM = IMAGE_WATERMARK.resize( (LARGEUR_WATERMARK_REDIM, HAUTEUR_WATERMARK_REDIM) )
	else:
		POSITION_WATERMARK_X = -1
		POSITION_WATERMARK_Y = -1

		IMAGE_WATERMARK_REDIM = IMAGE_WATERMARK.rotate(90)
		LARGEUR_WATERMARK,HAUTEUR_WATERMARK = IMAGE_WATERMARK_REDIM.size
		LARGEUR_WATERMARK_REDIM = (int) (LARGEUR_PHOTO * 0.1)
		HAUTEUR_WATERMARK_REDIM = (int) (((1.0*HAUTEUR_WATERMARK) / LARGEUR_WATERMARK) * LARGEUR_WATERMARK_REDIM)
		IMAGE_WATERMARK_REDIM = IMAGE_WATERMARK_REDIM.resize( (LARGEUR_WATERMARK_REDIM, HAUTEUR_WATERMARK_REDIM) )

	# Calcul de la position du watermark
	if POSITION_WATERMARK_X >= 0:
		POSITION_CALC_WATERMARK_X = 0
	else:
		POSITION_CALC_WATERMARK_X = LARGEUR_PHOTO - LARGEUR_WATERMARK_REDIM

	if POSITION_WATERMARK_Y >= 0:
		POSITION_CALC_WATERMARK_Y = 0
	else:
		POSITION_CALC_WATERMARK_Y = HAUTEUR_PHOTO - HAUTEUR_WATERMARK_REDIM

	# Calcul des taille, l'orientation, et la position du texte
	print NOM_PHOTO + ": Création du texte..."
	if LARGEUR_PHOTO >= HAUTEUR_PHOTO:
		POSITION_TEXTE_X = POSITION_CALC_WATERMARK_X + LARGEUR_WATERMARK_REDIM + 10
		POSITION_TEXTE_Y = POSITION_CALC_WATERMARK_Y + (HAUTEUR_WATERMARK_REDIM/4)
		TAILLE_TEXTE = HAUTEUR_PHOTO / 30

		POLICE_TEXTE = ImageFont.truetype(CHEMIN_POLICE_TEXTE, TAILLE_TEXTE)

		IMAGE_TEXTE = Image.new("RGBA", ((LARGEUR_PHOTO - LARGEUR_WATERMARK_REDIM), TAILLE_TEXTE * 2))
		DESSIN_TEXTE = ImageDraw.Draw(IMAGE_TEXTE)
		DESSIN_TEXTE.text((0,0), TEXTE, font=POLICE_TEXTE, fill=(255, 255, 255))
	else:
		POSITION_TEXTE_X = POSITION_CALC_WATERMARK_X + LARGEUR_WATERMARK_REDIM/4
		POSITION_TEXTE_Y = 0 - 10
		TAILLE_TEXTE = LARGEUR_PHOTO / 30

		POLICE_TEXTE = ImageFont.truetype(CHEMIN_POLICE_TEXTE, TAILLE_TEXTE)

		IMAGE_TEXTE = Image.new("RGBA", ((HAUTEUR_PHOTO - HAUTEUR_WATERMARK_REDIM), TAILLE_TEXTE * 2))
		DESSIN_TEXTE = ImageDraw.Draw(IMAGE_TEXTE)
		DESSIN_TEXTE.text((0,0), TEXTE, font=POLICE_TEXTE, fill=(255, 255, 255))
		IMAGE_TEXTE = IMAGE_TEXTE.rotate(90)

	del DESSIN_TEXTE
	del POLICE_TEXTE

	# Création du fond du Watermark
	if LARGEUR_PHOTO >= HAUTEUR_PHOTO:
		IMAGE_FOND_WATERMARK = Image.new("RGBA", (LARGEUR_PHOTO, HAUTEUR_WATERMARK), (0, 0, 0, 128))
		POSITION_FOND_WATERMARK_X = 0
		POSITION_FOND_WATERMARK_Y = POSITION_CALC_WATERMARK_Y
	else:
		IMAGE_FOND_WATERMARK = Image.new("RGBA", (HAUTEUR_WATERMARK, HAUTEUR_PHOTO), (0, 0, 0, 128))
		POSITION_FOND_WATERMARK_X = POSITION_CALC_WATERMARK_X
		POSITION_FOND_WATERMARK_Y = 0

	print NOM_PHOTO + ": Ajout du watermark..."
	IMAGE_PHOTO.paste(IMAGE_FOND_WATERMARK, (POSITION_FOND_WATERMARK_X, POSITION_FOND_WATERMARK_Y), IMAGE_FOND_WATERMARK)
	IMAGE_PHOTO.paste(IMAGE_WATERMARK_REDIM, (POSITION_CALC_WATERMARK_X, POSITION_CALC_WATERMARK_Y), IMAGE_WATERMARK_REDIM)
	IMAGE_PHOTO.paste(IMAGE_TEXTE, (POSITION_TEXTE_X, POSITION_TEXTE_Y), IMAGE_TEXTE)

	print NOM_PHOTO + ": Sauvegarde de l'image..."
	IMAGE_PHOTO.save(DOSSIER_PHOTOS_FINALES + "/" + NOM_PHOTO)

	del IMAGE_PHOTO
	del IMAGE_WATERMARK_REDIM
	del IMAGE_TEXTE
	del IMAGE_FOND_WATERMARK

del IMAGE_WATERMARK
