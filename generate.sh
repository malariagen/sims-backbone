npm install @openapitools/openapi-generator-cli@cli-4.0.0-beta -D
for i in "$@"
do
case $i in
    noauth)
    NO_AUTH=true
    sed -i -e 's/^security:/#&/' -e '/^#security:/{n;s/.*/#&/}' openapi/sims-backbone.yaml
    ;;
    server)
    SERVER_ONLY=true
    ;;
    client)
    CLIENT_ONLY=true
    ;;
    *)
          # unknown option
    ;;
esac
done
if [ -n "$SERVER_ONLY" -o -z "$CLIENT_ONLY" ]
then
    rm -rf python-flask-server
    (cd openapi && npx openapi-generator generate -i sims-backbone.yaml -g python-flask -o ../python-flask-server)
    rm -rf server/bb_server
    cp -pr python-flask-server server/bb_server
fi
if [ -n "$CLIENT_ONLY" -o -z "$SERVER_ONLY" ]
then
    (cd openapi && npx openapi-generator generate -i sims-backbone.yaml -g typescript-angular -o ../client/sims-backbone/src/app/typescript-angular-client)
    rm -rf python_client
    (cd openapi && npx openapi-generator generate -i sims-backbone.yaml -g python -o ../python_client)
fi
if [ -n "$NO_AUTH" ]
then
    sed -i -e '/^#security:/{s/^#//}' -e '/^security:/{n;s/^#//}' openapi/sims-backbone.yaml
fi
