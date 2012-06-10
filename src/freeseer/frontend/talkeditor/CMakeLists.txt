get_filename_component(TMP_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)
set(TALKEDITOR_PATH ${TMP_DIR})

execute_process(COMMAND pyrcc4 ${TALKEDITOR_PATH}/../../framework/resources/resource.qrc -o ${TALKEDITOR_PATH}/resource_rc.py)

if(UNIX)
    execute_process(COMMAND pyuic4 ${TALKEDITOR_PATH}/forms/talkeditor_ui_qt.ui -o ${TALKEDITOR_PATH}/talkeditor_ui_qt.py)
endif(UNIX)
if(WIN32)
    execute_process(COMMAND pyuic4.bat ${TALKEDITOR_PATH}/forms/talkeditor_ui_qt.ui -o ${TALKEDITOR_PATH}/talkeditor_ui_qt.py)
endif(WIN32)
