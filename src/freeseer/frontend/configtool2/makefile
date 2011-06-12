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

# This makefile generates the python code for the gui
# from an XML definition file
ALL: gui 

gui: configtoolui.py pluginloader.py

configtoolui.py: forms/configtoolui.ui
	pyuic4 forms/configtoolui.ui -o configtoolui.py

pluginloader.py: forms/pluginloader.ui
	pyuic4 forms/pluginloader.ui -o pluginloader.py

clean: 
	rm -f  configtoolui.py *.pyc *~

