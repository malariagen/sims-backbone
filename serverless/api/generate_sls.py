import codecs

import re
import yaml

from collections import OrderedDict

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

specification = None
arguments = {}

with codecs.open('../../swagger.yaml', 'r', 'utf-8') as swagger_yaml:
    swagger_template = swagger_yaml.read()
    specification = ordered_load(swagger_template)

for path in specification['paths']:
#    print(path)
    for op in specification['paths'][path]:
#        print(op)
        op_spec = specification['paths'][path][op]
        op_id = op_spec['operationId']
#        print(specification['paths'][path][op])
        path_elements = path.split('/')
        converted_path_elements = []
        for p in path_elements:
            if p.startswith('{'):
                converted_path_elements.append(convert(p))
            else:
                converted_path_elements.append(p)

        print('''  ''' + convert(op_id) + ':\n' + \
'''    handler: ''' + convert(op_spec['tags'][0]) + '''/handler.''' + convert(op_id) + '''
    events:
      - http:
          path: sims-backbone-service/v1''' + '/'.join(converted_path_elements) + '\n          method: ' + op +\
'''\n          cors: true
          timeout: 20
          authorizer:
            name: auth_func
            type: request
            identitySource: method.request.header.Authorization
            identityValidationExpression: .*''')
        if 'parameters' in op_spec:
            paths = []
            for param in op_spec['parameters']:
                if param['in'] == 'path':
                    req = 'false'
                    if 'required' in param and param['required']:
                        req  = 'true'
                    paths.append('''                ''' + convert(param['name']) + ': ' + req)
            args = []
            for param in op_spec['parameters']:
                if param['in'] == 'query':
                    req = 'false'
                    if 'required' in param and param['required']:
                        req  = 'true'
                    args.append('''                ''' + convert(param['name']) + ': ' + req)
            if paths or args:
                print('''          request:
            parameters:''')

            if paths:
                print('''              paths:''')
                for p in paths:
                    print(p)
            if args:
                print('''              query:''')
                for arg in args:
                    print(arg)

    print('')
