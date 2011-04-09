set(DEFAULT_UI_PATH ${CMAKE_CURRENT_LIST_DIR})

cmake_minimum_required (VERSION 2.8)
project (Freeseer)

execute_process(COMMAND pyuic4 ${DEFAULT_UI_PATH}/forms/freeseer_ui_qt.ui -o ${DEFAULT_UI_PATH}/freeseer_ui_qt.py)
execute_process(COMMAND pyuic4 ${DEFAULT_UI_PATH}/forms/freeseer_about.ui -o ${DEFAULT_UI_PATH}/freeseer_about.py)
execute_process(COMMAND pyrcc4 ${DEFAULT_UI_PATH}/forms/resource.qrc -o ${DEFAULT_UI_PATH}/resource_rc.py)
