SERVER_DIR=$(pwd)/server-`date -Iminutes`
CLIENT_DIR=$(pwd)/client-`date -Iminutes`
mkdir $SERVER_DIR
mkdir $CLIENT_DIR
tar zxf ~/backbone-server.tgz -C ${SERVER_DIR}
tar zxf ~/backbone-client.tgz -C ${CLIENT_DIR}
cd ~/current
for i in bb_server server-env backbone_server
do
	rm $i
	ln -s ${SERVER_DIR}/server/$i
done
rm client
ln -s ${CLIENT_DIR}/client/backbone-client/dist client
