if [ -f ~/Downloads/swagger.yaml ]
then
    mv ~/Downloads/swagger.yaml ..
fi
(cd ../;./generate.sh)
cp -pr overlay/* bb_server
diff overlay/openapi_server/controllers/ ../python-flask-server/openapi_server/controllers/
