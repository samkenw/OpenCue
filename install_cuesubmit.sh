pip install -r requirements.txt
pip install -r requirements_gui.txt
cd cuesubmit
rm -R dist
rm -R build
rm -R *.egg-info
python setup.py install
cd ..