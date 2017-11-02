if [ -f ~/Downloads/swagger.yaml ]
then
    mv ~/Downloads/swagger.yaml ..
fi
(cd ../;./generate.sh)
cp -pr overlay/* bb_server
diff overlay/swagger_server/controllers/ ../python-flask-server/swagger_server/controllers/
