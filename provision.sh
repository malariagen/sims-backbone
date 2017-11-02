sed -i -e "s/^host: .*/host: $1/" -e "s/- http/- https/" swagger.yaml
(cd server;./refresh.sh)
(cd client/backbone-client;ng build -prod --bh /backbone/)
tar czvf backbone-server.tgz server/backbone_server server/server-env server/bb_server
tar czvf backbone-client.tgz client/backbone-client/dist/
tar czvf backbone-db.tgz database
scp backbone-*.tgz $1:~
git checkout -- swagger.yaml
(cd server;./refresh.sh)
