set(CONFIGTOOL_PATH ${CMAKE_CURRENT_LIST_DIR})

cmake_minimum_required (VERSION 2.8)

execute_process(COMMAND pyuic4 ${CONFIGTOOL_PATH}/../forms/freeseer_configtool_ui.ui -o ${CONFIGTOOL_PATH}/freeseer_configtool_ui.py)
execute_process(COMMAND pyrcc4 ${CONFIGTOOL_PATH}/../forms/resource.qrc -o ${CONFIGTOOL_PATH}/resource_rc.py)
