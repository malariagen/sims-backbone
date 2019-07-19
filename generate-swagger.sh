test -f swagger-codegen-cli.jar || wget https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.9/swagger-codegen-cli-3.0.9.jar -O swagger-codegen-cli.jar
for i in "$@"
do
case $i in
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
    rm -rf python-flask-server.swagger
    (cd openapi && java -jar ../swagger-codegen-cli.jar generate -i sims-backbone.yaml -l python-flask -o ../python-flask-server.swagger)
    sed -i  -e '/x-tokenInfoFunc/d' -e '/x-scopeValidateFunc/d' python-flask-server.swagger/openapi_server/openapi/openapi.yaml
fi
if [ -n "$CLIENT_ONLY" -o -z "$SERVER_ONLY" ]
then
    (cd openapi && java -jar ../swagger-codegen-cli.jar generate -i sims-backbone.yaml -l typescript-angular -o ../typescript-angular-client.swagger -c client.config.json)
    rm -rf python_client.swagger
    (cd openapi && java -jar ../swagger-codegen-cli.jar generate -i sims-backbone.yaml -l python -o ../python_client.swagger -c client.config.json)
    sed -i -e "/discriminator = None/a\\\n    def get_real_child_model(self, data):\n      return 'dict(str, Location)'\n\n" python_client.swagger/swagger_client/models/location_map.py
fi

