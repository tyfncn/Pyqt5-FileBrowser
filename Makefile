all:
	( \
		python3 -m venv .env \
		source .env/bin/activate; \
		pip install -r requirements.txt; \
		pyinstaller --onefile --add-data "FileBrowser.ui:FileBrowser.ui" FileBrowser.py \
    )	


clean:
	rm -rf .env
	rm -rf build
	rm -rf dist
	rm -rf source
	rm -rf __pycache__