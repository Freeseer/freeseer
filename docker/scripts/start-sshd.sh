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

echo "Generating Root Password..."
PASS=$(pwgen -s 12 1)

printf "$PASS\n$PASS" | passwd > /dev/null 2>&1

echo "---"
echo "SSH Server configured"
echo "---"
echo "Your randomly generated root password is $PASS"
echo ""
echo "To connect to the dev system run the following command:"
echo "    ssh -X root@server -p <port>"
echo ""
echo "Where <port> is the port forwarded on your host."
echo ""

echo "Starting SSHD..."
mkdir /var/run/sshd
exec /usr/sbin/sshd -D
