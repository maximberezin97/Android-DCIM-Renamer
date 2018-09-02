# Android DCIM Renamer

This is a Python script that standardizes image/video/panorama file names to the Android standard naming scheme that generally looks like IMG_YYYYMMDD_HHMMSS.jpg.
My camera roll directory was a mess of different naming standards, and I had a tough time settling on one standard. I decided that Android's default naming scheme was a good idea because it is very common.
This script uses two regular expressions to match files that are in the format YYYY-MM-DD HH-MM-SS or just YYYY-MM-DD. It can also parse date/time metadata from EXIF data and file attributes. In my case, many files' dates were inaccurate and misplaced. I assumed that it was most likely that the earliest date/time associated with the file was most likely the date/time of capture, so in the latter regex case I sort all found dates and assume the earliest one.

There is one argument: a directory full of files. For example, you may call `python dcim_renamer.py "~/Pictures/Camera Roll"`

This script requires the Python Imaging Library (PIL) to handle EXIF data. The library is available as a fork on PyPI as Pillow.

This script was written in a few hours with no comments and no plans for further development. However, this script could be made better by adding support to edit file attributes, detect panoramas by resolution ratios, or adding user input to interactively select dates due to possible further inaccuracy.
