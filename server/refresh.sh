if [ -f ~/Downloads/swagger.yaml ]
then
    mv ~/Downloads/swagger.yaml ..
fi
(cd ../;./generate.sh)
cp -pr overlay/* bb-server
diff overlay/swagger_server/controllers/ ../python-flask-server/swagger_server/controllers/
