ps -ef| grep mainApp.py| awk '{print $2}'| xargs kill -9;
echo "stop success!"
