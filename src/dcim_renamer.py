import sys
import os
import re
import shutil
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

videos = ['.MP4', '.MOV']
images = ['.JPG', '.JPEG', '.PNG']
exif_images = ['.JPG', '.JPEG']
re1 = re.compile(r"(\d\d\d\d)-(\d\d)-(\d\d) (\d\d)\.(\d\d)\.(\d\d)(.*)?\.")
re2 = re.compile(r"(\d{8})_(\d{9})")

folder = sys.argv[1] if len(sys.argv) > 1 else ""
for root, dirs, files in os.walk(folder):
	for file in files:
		print(file, end='')
		path = os.path.join(folder, file)
		rename = ''
		times = []

		prefix = ''
		if os.path.splitext(file)[1].upper() in images:
			prefix = "IMG"
		elif os.path.splitext(file)[1].upper() in videos:
			prefix = "VID"
		if 'pano' in file.lower() or 'stitch' in file.lower():
			prefix = "PANO"
		rename = prefix

		re1_match = re.match(re1, file)
		if re1_match:
			year = re1_match.groups()[0]
			month = re1_match.groups()[1]
			day = re1_match.groups()[2]
			hour = re1_match.groups()[3]
			minute = re1_match.groups()[4]
			second = re1_match.groups()[5]
			time = year+month+day+hour+minute+second
			times.append(datetime.datetime.strptime(time, "%Y%m%d%H%M%S"))

		re2_match = re.match(re2, file)
		if re2_match:
			ymd = re2_match.groups()[0]
			hms = re2_match.groups()[1][:5]
			time = ymd+hms
			times.append(datetime.datetime.strptime(time, "%Y%m%d%H%M%S"))

		if os.path.splitext(file)[1] in exif_images:
			exif = Image.open(path)._getexif()
			for (k, v) in exif.items():
				# print(TAGS.get(k), '=', v)
				if TAGS.get(k) in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']:
					times.append(datetime.datetime.strptime(v, "%Y:%m:%d %H:%M:%S"))

		times.append(datetime.datetime.fromtimestamp(os.path.getatime(path)))
		times.append(datetime.datetime.fromtimestamp(os.path.getctime(path)))
		times.append(datetime.datetime.fromtimestamp(os.path.getmtime(path)))

		if times:
			try:
				retime = sorted(times)[0].strftime("%Y%m%d_%H%M%S")
				rename += '_'+retime
			except IndexError:
				for (k, v) in exif.items():
					print(TAGS.get(k), '=', v)
				exit()

			ext = os.path.splitext(file)[1].lower()

			new_path = os.path.join(folder, rename+ext)
			if os.path.exists(new_path):
				suffix = 1
				while os.path.exists(new_path):
					new_path = os.path.join(folder, rename+'_'+str(suffix)+ext)
					suffix += 1

			shutil.move(path, new_path)
			print('\tRENAMED', rename+ext, end='')			
		print()
