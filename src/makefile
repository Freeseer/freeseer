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

ALL: gui lib 
	@echo "You can now run ./freeseer"

lib: sipqxtglobalshortcutQxtGlobalShortcut.cpp sipqxtglobalshortcutQxtGlobalShortcut.o
	@echo "Re-generated libraries"

gui: freeseer_ui_qt.py freeseer_about.py resource_rc.py
	@echo "Re-generated GUI"

sipqxtglobalshortcutQxtGlobalShortcut.cpp: lib/qxtglobalshortcut.sip
	sip -t Qt_4_4_1 -I /usr/share/sip/ -t WS_X11 -c lib/. lib/qxtglobalshortcut.sip

sipqxtglobalshortcutQxtGlobalShortcut.o: lib/config.py
	cd lib; python config.py; make 
	mv lib/*.so ./freeseer

freeseer_ui_qt.py: forms/freeseer_ui_qt.ui
	pyuic4 forms/freeseer_ui_qt.ui -o freeseer/freeseer_ui_qt.py

freeseer_about.py: forms/freeseer_about.ui
	pyuic4 forms/freeseer_about.ui -o freeseer/freeseer_about.py

resource_rc.py: forms/resource.qrc
	pyrcc4 forms/resource.qrc -o freeseer/resource_rc.py

clean:
	rm -f freeseer/resource_rc.py freeseer/freeseer_about.py freeseer/freeseer_ui_qt.py freeseer/*.pyc freeseer/*/*.pyc freeseer/*/*~ lib/Makefile lib/qxtglobalshortcutconfig.py lib/*.exp lib/*.sbf lib/sip* freeseer/qxtglobalshortcut.so

test: ALL
	./freeseer
