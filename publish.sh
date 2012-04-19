#!/usr/bin/env bash

# Copies the HTML documentations files created by Sphinx,
# from the freeseer-docs repo to the freeseer.github.com repo.
# Then publishes the updated documentation by staging the files,
# commiting, and pushing them.
#
# Author(s):
# Dennis Ideler <ideler.dennis at gmail.com>
#
# Copyright 2012  Free and Open Source Software Learning Centre (FOSSLC)
# http://fosslc.org
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
#
# For support, questions, suggestions or any other inquiries, visit:
# http://freeseer.github.com

# Exit on error.
set -o errexit

# Verify all parameters are set.
#set -o nounset

echo "Locating freeseer.github.com repository..."
REPO=$(find $HOME -type d -name freeseer.github.com)

# Exit if not found.
if [ "$REPO" = "" ]; then echo "freeseer.github.com repo not found!"; exit 1; fi

# Keep track of freeseer-docs location.
DOCS="$( cd "$( dirname "$0" )" && pwd )"

# Silently switch to freeseer.github.com/docs. Exit if directory doesn't exist.
pushd "$REPO/docs" >/dev/null || { echo "You don't have the latest revision!"; exit 1; }

echo "Copying docs..."
cp -rp $DOCS/build/html/* .

echo "Publishing docs..."
git add .
git commit -m 'Updating docs'
git push # May require user's GitHub password.

# Silently switch back to the original directory.
popd >/dev/null
echo "Documentation published!"
