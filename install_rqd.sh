BASEDIR=$(dirname "$0")
$1 -m pip install -r $BASEDIR/requirements.txt
cd $BASEDIR/proto
$1 -m grpc_tools.protoc -I=. --python_out=../rqd/rqd/compiled_proto --grpc_python_out=../rqd/rqd/compiled_proto ./*.proto
cd $BASEDIR/rqd
rm -R dist
rm -R build
rm -R *.egg-info
2to3 -w -n --no-diffs rqd/compiled_proto
$1 setup.py install
cd $BASEDIR