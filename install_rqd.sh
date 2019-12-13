pip install -r requirements.txt
cd proto
python -m grpc_tools.protoc -I=. --python_out=../rqd/rqd/compiled_proto --grpc_python_out=../rqd/rqd/compiled_proto ./*.proto
cd ../rqd
rm -R dist
rm -R build
rm -R *.egg-info
2to3 -w -n --no-diffs rqd/compiled_proto
python setup.py install
cd ..