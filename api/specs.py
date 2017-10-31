from django.apps import apps

Deployment = apps.get_model('platforms', 'PlatformDeployment')
Platform = apps.get_model('platforms', 'Platform')
Project = apps.get_model('general', 'Project')
InstrumentOnPlatform = apps.get_model('instruments', 'InstrumentOnPlatform')
PlatformType = apps.get_model('platforms', 'PlatformType')
Instrument = apps.get_model('instruments', 'Instrument')
Sensor = apps.get_model('instruments', 'Sensor')

print Sensor._meta.get_field('instrument_id').help_text

specs = [
    {
        'method': 'POST',
        'name': 'get_token',
        'desc': '''Takes a user's username and password and returns a token.''',
        'args': [
            {
                'name': 'username',
                'type': 'String',
                'required': 'required',
            },
            {
                'name': 'password',
                'type': 'String',
                'required': 'required',
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_instruments',
        'desc': '''Takes a maximum of one of the two listed arguments.
            If no arguments are included, all results will be returned.''',
        'args': [
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'identifier',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_instruments_on_platform',
        'desc': '''Query must fit this boolean expression if arguments are
        included: '(id) xor (name or time or identifier).''',
        'args': [
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'optional',
                'desc': 'The id on the InstrumentOnPlatform table.'
            },
            {
                'name': 'name',
                'type': 'String',
                'required': 'optional',
                'desc': 'The name of the Platform linked to InstrumentOnPlatform.'
            },
            {
                'name': 'time',
                'type': 'String',
                'required': 'optional',
                'desc': 'A time when the Instrument was on the platform.'
            },
            {
                'name': 'identifier',
                'type': 'String',
                'required': 'optional',
                'desc': 'The identifier of the Instrument linked to InstrumentOnPlatform.'
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_sensors',
        'desc': '''Takes a maximum of one of the three listed arguments.
            If no argument is included, all results will be returned.''',
        'args': [
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'instrument_id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'identifier',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_platform',
        'desc': '''Takes a maximum of one of the two listed arguments.
            If no arguments are included, all results will be returned.''',
        'args': [
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'name',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_manufacturer',
        'desc': '''Takes a maximum of one of the two listed arguments.
            If no arguments are included, all results will be returned.''',
        'args': [
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'name',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_institutions',
        'desc': '''Takes a maximum of one of the two listed arguments.
            If no arguments are included, all results will be returned.''',
        'args': [
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'name',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_project',
        'desc': '''Takes a maximum of one of the two listed arguments.
            If no arguments are included, all results will be returned.''',
        'args': [
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'name',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_platform_type',
        'desc': '''Takes a maximum of one of the two listed arguments.
            If no arguments are included, all results will be returned.''',
        'args': [
            {
                'name': 'model',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'name',
                'type': 'String',
                'required': 'optional',
                'desc': 'The name of a platform'
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_platform_deployments',
        'desc': '''Query must fit this boolean expression if arguments are
        included: '(name and time) or (name) or (number).''',
        'args': [
            {
                'name': 'name',
                'type': 'String',
                'required': 'optional',
                'desc': 'The name of the platform.'
            },
            {
                'name': 'time',
                'type': 'Date String(Y-m-d H:M:S)',
                'required': 'optional',
                'desc': 'A time when the platform was on deployment.'
            },
            {
                'name': 'number',
                'type': 'String',
                'required': 'optional',
                'desc': 'The deployment number of the deployment.'
            },
        ]
    },
    {
        'method': 'GET',
        'name': 'get_deployment_instruments',
        'desc': '''Get all the instruments on a deployment''',
        'args': [
            {
                'name': 'name',
                'type': 'String',
                'required': 'required',
                'desc': 'The name of the platform.'
            },
            {
                'name': 'time',
                'type': 'Date String(Y-m-d H:M:S)',
                'required': 'required',
                'desc': 'A time when the platform was on deployment.'
            }
        ]
    },
    {
        'method': 'GET',
        'name': 'get_output_sensors',
        'desc': '''Takes a maximum of one of the two listed arguments.
            If no arguments are included, all results will be returned.''',
        'args': [
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'optional',
                'desc': 'The id of the instrument'
            },
            {
                'name': 'identifier',
                'type': 'String',
                'required': 'optional',
                'desc': 'The identifier of the instrument'
            },
        ]
    },
    {
        'method': 'POST',
        'name': 'insert_sensor',
        'args': [
            {
                'name': 'instrument_id',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'identifier',
                'type': 'String',
                'required': 'required'
            },
            {
                'name': 'long_name',
                'type': 'String',
                'required': 'required'
            },
            {
                'name': 'standard_name',
                'type': 'String',
                'required': 'required if included in output is true'
            },
            {
                'name': 'type',
                'type': 'String',
                'required': 'optional'
            },
            {
                'name': 'units',
                'type': 'String',
                'required': 'optional'
            },
            {
                'name': 'precision',
                'type': 'Float',
                'required': 'optional'
            },
            {
                'name': 'accuracy',
                'type': 'Float',
                'required': 'optional'
            },
            {
                'name': 'resolution',
                'type': 'Float',
                'required': 'optional'
            },
            {
                'name': 'valid_min',
                'type': 'Float',
                'required': 'optional'
            },
            {
                'name': 'valid_max',
                'type': 'Float',
                'required': 'optional'
            },
            {
                'name': 'include_in_output',
                'type': 'Boolean',
                'required': 'optional, defaults to false'
            },
            {
                'name': 'display_in_web_interface',
                'type': 'Boolean',
                'required': 'optional, defaults to false'
            },
            {
                'name': 'comment',
                'type': 'String',
                'required': 'optional'
            },

        ]
    },
    {
        'method': 'POST',
        'name': 'insert_instrument',
        'args': [
            {
                'name': 'identifier',
                'type': 'String',
                'required': 'required',
            },
            {
                'name': 'short_name',
                'type': 'String',
                'required': 'required',
            },
            {
                'name': 'long_name',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'manufacturer_id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'serial',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'instrument_id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'comment',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'POST',
        'name': 'insert_instrument_on_platform',
        'args': [
            {
                'name': 'instrument_id',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'platform_id',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'start_time',
                'type': 'Date String(Y-m-d H:M:S)',
                'required': 'required',
            },
            {
                'name': 'end_time',
                'type': 'Date String(Y-m-d H:M:S)',
                'required': 'optional',
            },
            {
                'name': 'comment',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'POST',
        'name': 'insert_deployment',
        'args': [
            {
                'name': 'wmo_id',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'deployment_number',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'platform_id',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'institution_id',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'project_id',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'title',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'start_time',
                'type': 'Date String(Y-m-d H:M:S)',
                'required': 'required',
            },
            {
                'name': 'end_time',
                'type': 'Date String(Y-m-d H:M:S)',
                'required': 'optional',
            },
            {
                'name': 'comment',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'acknowledgement',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'contributor_name',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'contributor_role',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'creator_email',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'creator_name',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'creator_url',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'data_repository_link',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'data_repository_link',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'publisher_email',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'publisher_name',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'publisher_url',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'metadata_link',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'references',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'sea_name',
                'type': 'String',
                'required': 'optional, defaults to "North Atlantic Ocean"',
            },
            {
                'name': 'latitude',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'longitude',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'depth',
                'type': 'String',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'POST',
        'name': 'insert_project',
        'args': [
            {
                'name': 'name',
                'type': 'String',
                'required': 'required',
            },
        ]
    },
    {
        'method': 'POST',
        'name': 'insert_platform_type',
        'args': [
            {
                'name': 'model',
                'type': 'String',
                'required': 'required',
            },
            {
                'name': 'manufacturer_id',
                'type': 'Integer',
                'required': 'required',
            },
        ]
    },
    {
        'method': 'POST',
        'name': 'insert_platform',
        'args': [
            {
                'name': 'name',
                'type': 'String',
                'required': 'required',
            },
            {
                'name': 'wmo_id',
                'type': 'Integer',
                'required': 'optional',
            },
            {
                'name': 'serial_number',
                'type': 'String',
                'required': 'optional',
            },
            {
                'name': 'platform_type',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'institution',
                'type': 'Integer',
                'required': 'required',
            },
            {
                'name': 'purchase_date',
                'type': 'Date String(Y-m-d H:M:S)',
                'required': 'optional',
            },
        ]
    },
    {
        'method': 'POST',
        'name': 'update_component',
        'desc': '''Used to update entries in the different sensor tracker tables.
        Any column name can be a argument. Multiple columns can be edited at a time.
        ''',
        'args': [
            {
                'name': 'component',
                'type': 'String',
                'required': 'required',
                'desc': 'The table that will be updated. Options are: sensor, platform, project, instruments_platform, platform_type, instrument, sensor.'
            },
            {
                'name': 'id',
                'type': 'Integer',
                'required': 'required',
                'desc': 'Id of the edited entry.'
            },
        ]
    },
]

# Sorters
specs.sort(key=lambda x: x['name'])

links = [x['name'] for x in specs]
