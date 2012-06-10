get_filename_component(TMP_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)
set(CONFIGTOOL_PATH ${TMP_DIR})

cmake_minimum_required (VERSION 2.8)

execute_process(COMMAND pyrcc4 ${CONFIGTOOL_PATH}/../../framework/resources/resource.qrc -o ${CONFIGTOOL_PATH}/resource_rc.py)

if(UNIX)
    execute_process(COMMAND pyuic4 ${CONFIGTOOL_PATH}/forms/freeseer_configtool_ui.ui -o ${CONFIGTOOL_PATH}/freeseer_configtool_ui.py)
endif(UNIX)
if(WIN32)
    execute_process(COMMAND pyuic4.bat ${CONFIGTOOL_PATH}/forms/freeseer_configtool_ui.ui -o ${CONFIGTOOL_PATH}/freeseer_configtool_ui.py)
endif(WIN32)
