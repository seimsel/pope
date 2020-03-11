from io import BytesIO
from re import sub
from pathlib import Path
from ariadne import load_schema_from_path, make_executable_schema, ObjectType, MutationType, SubscriptionType, InterfaceType
from ariadne.asgi import GraphQL
from starlette.middleware.cors import CORSMiddleware
from matplotlib.figure import Figure
from matplotlib.pyplot import style
from numpy.random import rand
from numpy import linspace, frombuffer

from drivers.demo_scope import DemoScope

subscription = SubscriptionType()

style.use(str(Path(__file__).with_name('dark.mplstyle')))

class State:
    instruments = []

    instrument_types = [
        DemoScope
    ]

    @classmethod
    def get_instrument_by_address(cls, address):
        return next(filter(
            lambda instrument: instrument.address == address,
            cls.instruments))

    @classmethod
    def get_instrument_type_by_name(cls, name):
        return next(filter(
            lambda instrument_type: instrument_type.__name__ == name,
            cls.instrument_types))

@subscription.source('waveform')
async def waveform_generator(obj, info, instrumentAddress):
    instrument = State.get_instrument_by_address(instrumentAddress)
    figure = Figure()
    lines = {}

    while True:
        for channel in instrument.channels:
            if not channel.name in lines:
                lines[channel.name] = figure.gca().plot(instrument.t, channel.y)[0]
            else:
                lines[channel.name].set_ydata(channel.y)

        buffer = BytesIO()
        figure.savefig(buffer, format='svg')
        buffer.seek(0)
        image = buffer.read()
        buffer.close()

        yield  {
            'figure': image.decode('utf-8')
        }

@subscription.field('waveform')
def waveform_resolver(waveform, info, instrumentAddress):
    return waveform

mutation = MutationType()

@mutation.field('createInstrument')
def create_instrument(mutation, info, address, instrumentTypeName):
    instrument_type = State.get_instrument_type_by_name(instrumentTypeName)
    instrument_number = len(State.instruments)

    if not address:
        address = f'{instrumentTypeName}{instrument_number}'

    instrument = instrument_type(address)
    State.instruments.append(instrument)
    return instrument

@mutation.field('createChannel')
def create_channel(mutation, info, instrumentAddress, channelTypeName):
    instrument = State.get_instrument_by_address(sub(r'_', '.', instrumentAddress))
    channel_number = len(instrument.channels)
    channel_type = instrument.get_channel_type_by_name(channelTypeName)
    channel = channel_type(f'{channelTypeName}{channel_number}')
    instrument.add_channel(channel)
    return channel

@mutation.field('updateParameter')
def update_parameter(mutation, info, instrumentAddress, channelName, parameterName, value):
    instrument = State.get_instrument_by_address(sub(r'_', '.', instrumentAddress))
    channel = instrument.get_channel_by_name(channelName)
    parameter = channel.get_parameter_by_name(parameterName)
    parameter.value = value

    return parameter

query = ObjectType('Query')

@query.field('instruments')
def instruments_resolver(query, info):
    return State.instruments

@query.field('instrument')
def instrument_resolver(query, info, address):
    instrument = State.get_instrument_by_address(address)
    return instrument

@query.field('instrumentTypes')
def instrument_types_resolver(query, info):
    return map(
        lambda instrument_type: {
            'id': id(instrument_type),
            'name': instrument_type.__name__
        },
        State.instrument_types)

instrument = ObjectType('Instrument')

@instrument.field('channel')
def channel_resolver(instrument, info, name):
    channel = instrument.get_channel_by_name(name)
    return channel

@instrument.field('channelTypes')
def channel_types_resolver(instrument, info):
    return map(
        lambda channel_type: {
            'id': id(channel_type),
            'name': channel_type.__name__
        },
        instrument.channel_types)

channel = ObjectType('Channel')

@channel.field('parameter')
def parameter_resolver(channel, info, name):
    return channel.get_parameter_by_name(name)

parameter = InterfaceType('Parameter')

@parameter.type_resolver
def parameter_type_resolver(obj, *_):
    return obj.__class__.__name__

type_defs = load_schema_from_path('./graphql')
schema = make_executable_schema(type_defs, query, mutation, instrument, channel, parameter, subscription)

app = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
