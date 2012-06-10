get_filename_component(TMP_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)
set(FREESEER_SRC ${TMP_DIR}/src)

cmake_minimum_required (VERSION 2.8)
project(Freeseer)

include(${FREESEER_SRC}/freeseer/framework/CMakeLists.txt)
include(${FREESEER_SRC}/freeseer/frontend/default/CMakeLists.txt)
include(${FREESEER_SRC}/freeseer/frontend/configtool/CMakeLists.txt)
include(${FREESEER_SRC}/freeseer/frontend/talkeditor/CMakeLists.txt)
