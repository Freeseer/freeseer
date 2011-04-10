set(DEFAULT_UI_PATH ${CMAKE_CURRENT_LIST_DIR})

cmake_minimum_required (VERSION 2.8)
project (Freeseer)

execute_process(COMMAND pyrcc4 ${DEFAULT_UI_PATH}/forms/resource.qrc -o ${DEFAULT_UI_PATH}/resource_rc.py)

if (UNIX)
    execute_process(COMMAND pyuic4 ${DEFAULT_UI_PATH}/forms/freeseer_ui_qt.ui -o ${DEFAULT_UI_PATH}/freeseer_ui_qt.py)
    execute_process(COMMAND pyuic4 ${DEFAULT_UI_PATH}/forms/freeseer_about.ui -o ${DEFAULT_UI_PATH}/freeseer_about.py)
endif(UNIX)
if (WIN32)
    execute_process(COMMAND pyuic4.bat ${DEFAULT_UI_PATH}/forms/freeseer_ui_qt.ui -o ${DEFAULT_UI_PATH}/freeseer_ui_qt.py)
    execute_process(COMMAND pyuic4.bat ${DEFAULT_UI_PATH}/forms/freeseer_about.ui -o ${DEFAULT_UI_PATH}/freeseer_about.py)
endif(WIN32)

if (UNIX)
    execute_process(COMMAND sip -t Qt_4_4_1 -I /usr/share/sip/PyQt4 -t WS_X11 -c ${DEFAULT_UI_PATH}/lib/. ${DEFAULT_UI_PATH}/lib/qxtglobalshortcut.sip)
    execute_process(COMMAND python config.py
                    WORKING_DIRECTORY ${DEFAULT_UI_PATH}/lib)
    execute_process(COMMAND make
                    WORKING_DIRECTORY ${DEFAULT_UI_PATH}/lib)
    execute_process(COMMAND mv qxtglobalshortcut.so ${DEFAULT_UI_PATH}
                    WORKING_DIRECTORY ${DEFAULT_UI_PATH}/lib)
endif(UNIX)
