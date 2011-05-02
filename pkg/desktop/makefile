
ALL: desktop_entry

desktop_entry: ./freeseer.desktop
	@echo "checking desktop entry"
	desktop-file-validate ./freeseer.desktop

install: ./freeseer.desktop
	sudo desktop-file-install ./freeseer.desktop
