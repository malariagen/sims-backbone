# vim: set textwidth=0 wrapmargin=0:
for i in $(grep '/' ../openapi/sims-backbone.yaml | grep :$ | sed -e 's/:$//' -e "s/'//g" -e 's/^\s//' -e 's/{\([a-z_]*\)\([A-Z].\)/{\1_\l\2/g' -e 's#\/##' -e 's/\([A-Z].\)\([a-z]*\)}/_\l\1\2}/g' )
do
    SEARCH="path: ${i}$"
    egrep -q "${SEARCH}" */serverless.yml
    if [ $? -eq 1 ]
    then
        SEARCH="path: sims-backbone-service/v1/${i}$"
        egrep -q "${SEARCH}" */serverless.yml
        if [ $? -eq 1 ]
        then
            echo "Missing $i"
        fi
    fi
done
