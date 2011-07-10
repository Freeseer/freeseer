get_filename_component(TMP_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)
set(DEFAULT_UI_PATH ${TMP_DIR})

execute_process(COMMAND pyrcc4 ${DEFAULT_UI_PATH}/../../framework/resources/resource.qrc -o ${DEFAULT_UI_PATH}/resource_rc.py)

if (UNIX)
    execute_process(COMMAND pyuic4 ${DEFAULT_UI_PATH}/forms/freeseer_ui_qt.ui -o ${DEFAULT_UI_PATH}/freeseer_ui_qt.py)
endif(UNIX)
if (WIN32)
    execute_process(COMMAND pyuic4.bat ${DEFAULT_UI_PATH}/forms/freeseer_ui_qt.ui -o ${DEFAULT_UI_PATH}/freeseer_ui_qt.py)
endif(WIN32)
