# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
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
# http://wiki.github.com/Freeseer/freeseer/

FROM ubuntu:12.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y openssh-server pwgen
RUN apt-get install -y gstreamer-tools gstreamer0.10-plugins-good
RUN apt-get install -y sqlite libqt4-sql-sqlite
RUN apt-get install -y python-pip python-gst0.10 pyqt4-dev-tools python-qt4-sql python-feedparser python-httplib2 python-oauth python-simplejson
RUN pip install yapsy

ADD scripts /scripts
RUN chmod +x /scripts/*.sh

EXPOSE 22

CMD /scripts/start-sshd.sh

