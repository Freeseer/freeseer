#!/bin/bash

# TODO
# - add a help option
# - add a directory option to send us to another directory to transcode
# - check the return code to see if it worked

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2010  Free and Open Source Software Learning Centre
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

FF_OPTS="-s svga -acodec libvorbis -ab 64k -aspect 4:3"

ls *.ogg | \
while read source
do
  echo "Transcoding: ${source}"
  OUTPUT="`echo ${source} | sed \"s/.ogg/_processed.ogg/g\"`"
  echo "Creating: ${OUTPUT}"
  ffmpeg -i ${source} ${FF_OPTS} ${OUTPUT}
done
