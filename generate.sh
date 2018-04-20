test -f swagger-codegen-cli.jar || wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar -O swagger-codegen-cli.jar
#test -f swagger-codegen-cli.jar || wget https://oss.sonatype.org/content/repositories/snapshots/io/swagger/swagger-codegen-cli/3.0.0-SNAPSHOT/swagger-codegen-cli-3.0.0-20171009.075709-6.jar -O swagger-codegen-cli.jar
for i in "$@"
do
case $i in
    noauth)
    NO_AUTH=true
    sed -i -e 's/^security:/#&/' -e '/^#security:/{n;s/.*/#&/}' swagger.yaml
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
    java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python-flask -o python-flask-server
    rm -rf server/bb_server
    cp -pr python-flask-server server/bb_server
fi
if [ -n "$CLIENT_ONLY" -o -z "$SERVER_ONLY" ]
then
    rm -rf typescript-angular-client
    java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l typescript-angular -o client/sims-backbone/src/app/typescript-angular-client -c client.config.json
    rm -rf python_client
    java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python -o python_client -c client.config.json
fi
rm -rf apache2
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l apache2 -o apache2
if [ -n "$NO_AUTH" ]
then
    sed -i -e '/^#security:/{s/^#//}' -e '/^security:/{n;s/^#//}' swagger.yaml
fi
