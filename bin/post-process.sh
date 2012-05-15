#!/bin/bash -x

# TODO
# - add a help option
# - add a directory option to send us to another directory to transcode
# - check the return code to see if it worked

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/fosslc/freeseer/

BASE_FF_OPTS="-s svga -ab 64k -async 3 -r 24 -aspect 4:3 -qscale 4"
OGG_FF_OPTS="-acodec libvorbis"

ls *.ogg | \
while read ORIGINAL
do
   # Set up some useful variables
   MPG="`echo ${ORIGINAL} | sed \"s/.ogg/.mpg/g\"`"
   GLUED="`echo ${ORIGINAL} | sed \"s/.ogg/_glued.mpg/g\"`"
   OUTPUT="`echo ${ORIGINAL} | sed \"s/.ogg/_processed.ogg/g\"`"

   # Transcode to mpeg so we can concatenate easily
   ffmpeg -i ${ORIGINAL} ${BASE_FF_OPTS} ${MPG}

   # Concatenate the intro segment with the video
   cat ../intro.mpg ${MPG} > ${GLUED}

   # Transcode to the finished product (an ogg/vorbis video with intro)
   ffmpeg -i ${GLUED} ${BASE_FF_OPTS} ${OGG_FF_OPTS} ${OUTPUT}
done
