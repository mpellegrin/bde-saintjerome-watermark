#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

if len(sys.argv) != 4:
	print "Wrong arguments count"
	exit()

#Les espaces dans les noms de fichier, c'est le mal
DIRECTORY_SOURCE = "../photos/" + sys.argv[1]
DIRECTORY_DESTINATION = "../watermarked/" + sys.argv[1]

WATERMARK_PATH = "../assets/watermark.png"

MAX_WIDTH_DESTINATION = 400 * 4
MAX_HEIGHT_DESTINATION = 300 * 4

TEXTE = sys.argv[3].decode("utf-8")
CHEMIN_FONT_TEXT = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"

print "Opening directories..."

if not os.path.isdir(DIRECTORY_SOURCE):
	print "Directory " + DIRECTORY_SOURCE + " cannot be found"
	exit()

if not os.path.isdir(DIRECTORY_DESTINATION):
	print "Directory " + DIRECTORY_DESTINATION + " cannot be found"
	exit()

if DIRECTORY_SOURCE == DIRECTORY_DESTINATION:
	print "Source and destination directory are the same"
	exit()

print "Checking watermark..."

if not os.path.isfile(WATERMARK_PATH):
	print "The watermark " + WATERMARK_PATH + " is not a file"
	exit()

print "Loading watermark..."

IMAGE_WATERMARK_ORIGINAL = Image.open(WATERMARK_PATH)
IMAGE_WATERMARK_ORIGINAL.load()

IMAGE_WATERMARK = IMAGE_WATERMARK_ORIGINAL

PHOTO_NAME = sys.argv[2]

PHOTO_PATH = DIRECTORY_SOURCE + "/" + PHOTO_NAME
if not os.path.isfile(PHOTO_PATH):
	print "The original file " + PHOTO_NAME + " is not a file"
	exit()

print PHOTO_NAME + ": Loading file..."
IMAGE_PHOTO = Image.open(PHOTO_PATH)
IMAGE_PHOTO.load()

print PHOTO_NAME + ": Rotating file with EXIF data..."

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
		print PHOTO_NAME + ": Image rotated from ", rotate_values[orientation]," degrees"

print PHOTO_NAME + ": Scaling image..."
PHOTO_WIDTH,PHOTO_HEIGHT = IMAGE_PHOTO.size

if PHOTO_WIDTH > MAX_WIDTH_DESTINATION or MAX_HEIGHT_DESTINATION:
	RATIO = MAX_WIDTH_DESTINATION/MAX_HEIGHT_DESTINATION
	A = (MAX_WIDTH_DESTINATION, PHOTO_HEIGHT * MAX_WIDTH_DESTINATION / PHOTO_WIDTH)
	B = (PHOTO_WIDTH * MAX_HEIGHT_DESTINATION / PHOTO_HEIGHT, MAX_HEIGHT_DESTINATION)
	if A[1] > MAX_HEIGHT_DESTINATION and B[0] <= MAX_WIDTH_DESTINATION:
		IMAGE_PHOTO = IMAGE_PHOTO.resize(B, Image.ANTIALIAS)
		#PHOTO_WIDTH,PHOTO_HEIGHT = B
	else:
		if B[0] > MAX_WIDTH_DESTINATION and A[1] <= MAX_HEIGHT_DESTINATION:
			IMAGE_PHOTO = IMAGE_PHOTO.resize(A, Image.ANTIALIAS)
			#PHOTO_WIDTH,PHOTO_HEIGHT = A
		else:
			#print PHOTO_NAME + ": Error while calculating scale"
			#exit()
			IMAGE_PHOTO = IMAGE_PHOTO.resize((MAX_WIDTH_DESTINATION, MAX_HEIGHT_DESTINATION), Image.ANTIALIAS)

PHOTO_WIDTH,PHOTO_HEIGHT = IMAGE_PHOTO.size

# Watermark size
print PHOTO_NAME + ": Scaling watermark..."
if PHOTO_WIDTH >= PHOTO_HEIGHT:
	WATERMARK_POSITION_X = 0
	WATERMARK_POSITION_Y = -1

	WATERMARK_WIDTH,WATERMARK_WIDTH = IMAGE_WATERMARK.size
	WATERMARK_WIDTH_RESIZED = (int) (PHOTO_HEIGHT * 0.1)
	WATERMARK_WIDTH_RESIZED = (int) (((1.0*WATERMARK_WIDTH) / WATERMARK_WIDTH) * WATERMARK_WIDTH_RESIZED)
	IMAGE_WATERMARK_RESIZED = IMAGE_WATERMARK.resize( (WATERMARK_WIDTH_RESIZED, WATERMARK_WIDTH_RESIZED) )
else:
	WATERMARK_POSITION_X = -1
	WATERMARK_POSITION_Y = -1

	IMAGE_WATERMARK_RESIZED = IMAGE_WATERMARK.rotate(90)
	WATERMARK_WIDTH,WATERMARK_WIDTH = IMAGE_WATERMARK_RESIZED.size
	WATERMARK_WIDTH_RESIZED = (int) (PHOTO_WIDTH * 0.1)
	WATERMARK_WIDTH_RESIZED = (int) (((1.0*WATERMARK_WIDTH) / WATERMARK_WIDTH) * WATERMARK_WIDTH_RESIZED)
	IMAGE_WATERMARK_RESIZED = IMAGE_WATERMARK_RESIZED.resize( (WATERMARK_WIDTH_RESIZED, WATERMARK_WIDTH_RESIZED) )

# Watermark position
if WATERMARK_POSITION_X >= 0:
	POSITION_CALC_WATERMARK_X = 0
else:
	POSITION_CALC_WATERMARK_X = PHOTO_WIDTH - WATERMARK_WIDTH_RESIZED

if WATERMARK_POSITION_Y >= 0:
	POSITION_CALC_WATERMARK_Y = 0
else:
	POSITION_CALC_WATERMARK_Y = PHOTO_HEIGHT - WATERMARK_WIDTH_RESIZED

# Size, orientation, and position of text
print PHOTO_NAME + ": Writting text..."
if PHOTO_WIDTH >= PHOTO_HEIGHT:
	TEXT_POSITION_X = POSITION_CALC_WATERMARK_X + WATERMARK_WIDTH_RESIZED
	TEXT_POSITION_Y = POSITION_CALC_WATERMARK_Y + (WATERMARK_WIDTH_RESIZED/4)
	TAILLE_TEXTE = PHOTO_HEIGHT / 30

	FONT_TEXT = ImageFont.truetype(CHEMIN_FONT_TEXT, TAILLE_TEXTE)

	IMAGE_TEXT = Image.new("RGBA", ((PHOTO_WIDTH - WATERMARK_WIDTH_RESIZED), TAILLE_TEXTE * 2))
	DRAW_TEXT = ImageDraw.Draw(IMAGE_TEXT)
	DRAW_TEXT.text((0,0), TEXTE, font=FONT_TEXT, fill=(255, 255, 255))
else:
	TEXT_POSITION_X = POSITION_CALC_WATERMARK_X + WATERMARK_WIDTH_RESIZED/4
	TEXT_POSITION_Y = 0
	TAILLE_TEXTE = PHOTO_WIDTH / 30

	FONT_TEXT = ImageFont.truetype(CHEMIN_FONT_TEXT, TAILLE_TEXTE)

	IMAGE_TEXT = Image.new("RGBA", ((PHOTO_HEIGHT - WATERMARK_WIDTH_RESIZED), TAILLE_TEXTE * 2))
	DRAW_TEXT = ImageDraw.Draw(IMAGE_TEXT)
	DRAW_TEXT.text((0,0), TEXTE, font=FONT_TEXT, fill=(255, 255, 255))
	IMAGE_TEXT = IMAGE_TEXT.rotate(90)

del DRAW_TEXT
del FONT_TEXT

# Watermark background
if PHOTO_WIDTH >= PHOTO_HEIGHT:
	IMAGE_BACKGROUND_WATERMARK = Image.new("RGBA", (PHOTO_WIDTH, WATERMARK_WIDTH + 10), (0, 0, 0, 128))
	BACKGROUND_WATERMARK_POSITION_X = 0
	BACKGROUND_WATERMARK_POSITION_Y = POSITION_CALC_WATERMARK_Y - 10
else:
	IMAGE_BACKGROUND_WATERMARK = Image.new("RGBA", (WATERMARK_WIDTH + 10, PHOTO_HEIGHT), (0, 0, 0, 128))
	BACKGROUND_WATERMARK_POSITION_X = POSITION_CALC_WATERMARK_X - 10
	BACKGROUND_WATERMARK_POSITION_Y = 0

print PHOTO_NAME + ": Adding watermark..."
IMAGE_PHOTO.paste(IMAGE_BACKGROUND_WATERMARK, (BACKGROUND_WATERMARK_POSITION_X, BACKGROUND_WATERMARK_POSITION_Y), IMAGE_BACKGROUND_WATERMARK)
IMAGE_PHOTO.paste(IMAGE_WATERMARK_RESIZED, (POSITION_CALC_WATERMARK_X, POSITION_CALC_WATERMARK_Y), IMAGE_WATERMARK_RESIZED)
IMAGE_PHOTO.paste(IMAGE_TEXT, (TEXT_POSITION_X, TEXT_POSITION_Y), IMAGE_TEXT)

print PHOTO_NAME + ": Saving up image..."
IMAGE_PHOTO.save(DIRECTORY_DESTINATION + "/" + PHOTO_NAME)

del IMAGE_PHOTO
del IMAGE_WATERMARK_RESIZED
del IMAGE_TEXT
del IMAGE_BACKGROUND_WATERMARK

del IMAGE_WATERMARK

