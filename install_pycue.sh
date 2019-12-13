pip install -r requirements.txt
cd proto
python -m grpc_tools.protoc -I=. --python_out=../pycue/opencue/compiled_proto --grpc_python_out=../pycue/opencue/compiled_proto ./*.proto
cd ../pycue
2to3 -w -n --no-diffs opencue/compiled_proto
python setup.py install
cd ../pyoutline
python setup.py install
cd ..