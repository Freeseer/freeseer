set(TALKEDITOR_PATH ${CMAKE_CURRENT_LIST_DIR})

cmake_minimum_required (VERSION 2.8)

execute_process(COMMAND pyrcc4 ${TALKEDITOR_PATH}/forms/resource.qrc -o ${TALKEDITOR_PATH}/resource_rc.py)

if(UNIX)
    execute_process(COMMAND pyuic4 ${TALKEDITOR_PATH}/forms/talkeditor_ui_qt.ui -o ${TALKEDITOR_PATH}/talkeditor_ui_qt.py)
    execute_process(COMMAND pyuic4 ${TALKEDITOR_PATH}/forms/talkeditor_about.ui -o ${TALKEDITOR_PATH}/talkeditor_about.py)
endif(UNIX)
if(WIN32)
    execute_process(COMMAND pyuic4.bat ${TALKEDITOR_PATH}/forms/talkeditor_ui_qt.ui -o ${TALKEDITOR_PATH}/talkeditor_ui_qt.py)
    execute_process(COMMAND pyuic4.bat ${TALKEDITOR_PATH}/forms/talkeditor_about.ui -o ${TALKEDITOR_PATH}/talkeditor_about.py)
endif(WIN32)
