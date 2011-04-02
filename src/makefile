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

# Set the name of the executable here
exec = run-freeseer


ALL: gui configtool
	@echo "You can now run $(exec)"

gui: 
	cd freeseer/frontend/default; make
	@echo "Re-generated GUI"

configtool:
	cd freeseer/configtool; make
	@echo "Re-Generated configtool"

clean_gui:
	cd freeseer/frontend/default; make clean
	@echo "GUI files cleaned up"
	
clean_configtool:
	cd freeseer/configtool; make clean
	@echo "configtool files cleaned up"

clean: clean_gui clean_configtool
	rm -f freeseer/*.pyc freeseer/*/*.pyc freeseer/*/*~

test: gui
	./$(exec)
