set(DEFAULT_UI_PATH ${CMAKE_CURRENT_LIST_DIR})

execute_process(COMMAND pyrcc4 ${DEFAULT_UI_PATH}/../../framework/resources/resource.qrc -o ${DEFAULT_UI_PATH}/resource_rc.py)

if (UNIX)
    execute_process(COMMAND pyuic4 ${DEFAULT_UI_PATH}/forms/configtoolui.ui -o ${DEFAULT_UI_PATH}/configtoolui.py)
    execute_process(COMMAND pyuic4 ${DEFAULT_UI_PATH}/forms/generalui.ui -o ${DEFAULT_UI_PATH}/generalui.py)
    execute_process(COMMAND pyuic4 ${DEFAULT_UI_PATH}/forms/pluginloader.ui -o ${DEFAULT_UI_PATH}/pluginloader.py)
endif(UNIX)
if (WIN32)
    execute_process(COMMAND pyuic4.bat ${DEFAULT_UI_PATH}/forms/configtoolui.ui -o ${DEFAULT_UI_PATH}/configtoolui.py)
    execute_process(COMMAND pyuic4.bat ${DEFAULT_UI_PATH}/forms/generalui.ui -o ${DEFAULT_UI_PATH}/generalui.py)
    execute_process(COMMAND pyuic4.bat ${DEFAULT_UI_PATH}/forms/pluginloader.ui -o ${DEFAULT_UI_PATH}/pluginloader.py)
endif(WIN32)
