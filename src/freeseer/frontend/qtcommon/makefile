ALL:
	@echo "Building Resource files."
	lrelease languages/freeseer.pro
	pyrcc4 -o resource_rc.py resource.qrc
	cp resource_rc.py ../record/
	cp resource_rc.py ../configtool/
	cp resource_rc.py ../talkeditor/
	rm languages/*.qm
	@echo "Resource files created."
