set(FRAMEWORK_PATH ${CMAKE_CURRENT_LIST_DIR})

execute_process(COMMAND pyrcc4 ${FRAMEWORK_PATH}/resources/resource.qrc -o ${FRAMEWORK_PATH}/resource_rc.py)

if (UNIX)
    execute_process(COMMAND pyuic4 ${FRAMEWORK_PATH}/forms/freeseer_about.ui -o ${FRAMEWORK_PATH}/freeseer_about.py)
endif(UNIX)
if (WIN32)
    execute_process(COMMAND pyuic4.bat ${FRAMEWORK_PATH}/forms/freeseer_about.ui -o ${FRAMEWORK_PATH}/freeseer_about.py)
endif(WIN32)
