from . import types
from ..broker import broker
import functools
import inspect
from opentrons.containers import Well, Container, Slot, location_to_list


def stringify_location(location):
    def get_slot(location):
        trace = location.get_trace()
        for item in trace:
            if isinstance(item, Slot):
                return item

    type_to_text = {
        Slot: 'slot',
        Container: 'container',
        Well: 'well'
    }

    # Coordinates only
    if location is None:
        return '?'

    location = location_to_list(location)
    multiple = len(location) > 1

    return '{object_text}{suffix} {first}{last} in "{slot_text}"'.format(
            object_text=type_to_text[type(location[0])],
            suffix='s' if multiple else '',
            first=location[0].get_name(),
            last='...'+location[-1].get_name() if multiple else '',
            slot_text=get_slot(location[0]).get_name()
        )


def make_command(name, payload):
    return {'name': name, 'payload': payload}


def home(mount):
    text = 'Homing pipette plunger on mount {mount}'.format(mount=mount)
    return make_command(
        name=types.HOME,
        payload={
            'axis': mount,
            'text': text
        }
    )


def aspirate(instrument, volume, location, rate):
    location_text = stringify_location(location)
    text = 'Aspirating {volume} uL from {location} at {rate} speed'.format(
        volume=volume, location=location_text, rate=rate
    )
    return make_command(
        name=types.ASPIRATE,
        payload={
            'instrument': instrument,
            'volume': volume,
            'location': location,
            'rate': rate,
            'text': text
        }
    )


def dispense(instrument, volume, location, rate):
    location_text = stringify_location(location)
    text = 'Dispensing {volume} uL into {location}'.format(
        volume=volume, location=location_text, rate=rate
    )

    return make_command(
        name=types.DISPENSE,
        payload={
            'instrument': instrument,
            'volume': volume,
            'location': location,
            'rate': rate,
            'text': text
        }
    )


def consolidate(instrument, volume, source, dest):
    text = 'Consolidating {volume} from {source} to {dest}'.format(
        volume=volume,
        source=stringify_location(source),
        dest=stringify_location(dest)
    )
    # incase either source or dest is list of tuple location
    # strip both down to simply lists of Placeables
    locations = [] + location_to_list(source) + location_to_list(dest)
    return make_command(
        name=types.CONSOLIDATE,
        payload={
            'instrument': instrument,
            'locations': locations,
            'volume': volume,
            'source': source,
            'dest': dest,
            'text': text
        }
    )


def distribute(instrument, volume, source, dest):
    text = 'Distributing {volume} from {source} to {dest}'.format(
        volume=volume,
        source=stringify_location(source),
        dest=stringify_location(dest)
    )
    # incase either source or dest is list of tuple location
    # strip both down to simply lists of Placeables
    locations = [] + location_to_list(source) + location_to_list(dest)
    return make_command(
        name=types.DISTRIBUTE,
        payload={
            'instrument': instrument,
            'locations': locations,
            'volume': volume,
            'source': source,
            'dest': dest,
            'text': text
        }
    )


def transfer(instrument, volume, source, dest):
    text = 'Transferring {volume} from {source} to {dest}'.format(
        volume=volume,
        source=stringify_location(source),
        dest=stringify_location(dest)
    )
    # incase either source or dest is list of tuple location
    # strip both down to simply lists of Placeables
    locations = [] + location_to_list(source) + location_to_list(dest)
    return make_command(
        name=types.TRANSFER,
        payload={
            'instrument': instrument,
            'locations': locations,
            'volume': volume,
            'source': source,
            'dest': dest,
            'text': text
        }
    )


def comment(msg):
    text = msg
    return make_command(
        name=types.COMMENT,
        payload={
            'text': text
        }
    )


def mix(instrument, repetitions, volume, location):
    text = 'Mixing {repetitions} times with a volume of {volume}ul'.format(
        repetitions=repetitions, volume=volume
    )
    return make_command(
        name=types.MIX,
        payload={
            'instrument': instrument,
            'location': location,
            'volume': volume,
            'repetitions': repetitions,
            'text': text
        }
    )


def blow_out(instrument, location):
    location_text = stringify_location(location)
    text = 'Blowing out'

    if location is not None:
        text += ' at {location}'.format(location=location_text)

    return make_command(
        name=types.BLOW_OUT,
        payload={
            'instrument': instrument,
            'location': location,
            'text': text
        }
    )


def touch_tip(instrument):
    text = 'Touching tip'
    return make_command(
        name=types.TOUCH_TIP,
        payload={
            'instrument': instrument,
            'text': text
        }
    )


def air_gap():
    text = 'Air gap'
    return make_command(
        name=types.AIR_GAP,
        payload={
            'text': text
        }
    )


def return_tip():
    text = 'Returning tip'
    return make_command(
        name=types.RETURN_TIP,
        payload={
            'text': text
        }
    )


def pick_up_tip(instrument, location):
    location_text = stringify_location(location)
    text = 'Picking up tip {location}'.format(location=location_text)
    return make_command(
        name=types.PICK_UP_TIP,
        payload={
            'instrument': instrument,
            'location': location,
            'text': text
        }
    )


def drop_tip(instrument, location):
    location_text = stringify_location(location)
    text = 'Dropping tip {location}'.format(location=location_text)
    return make_command(
        name=types.DROP_TIP,
        payload={
            'instrument': instrument,
            'location': location,
            'text': text
        }
    )


def magdeck_engage():
    text = "Engaging magnetic deck module"
    return make_command(
        name=types.MAGDECK_ENGAGE,
        payload={'text': text}
    )


def magdeck_disengage():
    text = "Disengaging magnetic deck module"
    return make_command(
        name=types.MAGDECK_DISENGAGE,
        payload={'text': text}
    )


def magdeck_calibrate():
    text = "Calibrating magnetic deck module"
    return make_command(
        name=types.MAGDECK_CALIBRATE,
        payload={'text': text}
    )


def tempdeck_set_temp():
    text = "Setting temperature deck module temperature " \
           "(rounded off to nearest integer)"
    return make_command(
        name=types.TEMPDECK_SET_TEMP,
        payload={'text': text}
    )


def tempdeck_deactivate():
    text = "Deactivating temperature deck module"
    return make_command(
        name=types.TEMPDECK_DEACTIVATE,
        payload={'text': text}
    )


def delay(seconds, minutes):
    text = "Delaying for {minutes}m {seconds}s"
    return make_command(
        name=types.DELAY,
        payload={
            'minutes': minutes,
            'seconds': seconds,
            'text': text
        }
    )


def pause(msg):
    text = 'Pausing robot operation'
    if msg:
        text = text + ': {}'.format(msg)
    return make_command(
        name=types.PAUSE,
        payload={
            'text': text
        }
    )


def resume():
    return make_command(
        name=types.RESUME,
        payload={
            'text': 'Resuming robot operation'
        }
    )


def _do_publish(before, after, command, meta=None):
    publish_command = functools.partial(
        broker.publish,
        topic=types.COMMAND)

    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            call_args = _get_args(f, args, kwargs)
            command_args = dict(
                zip(
                    reversed(inspect.getfullargspec(command).args),
                    reversed(inspect.getfullargspec(command).defaults
                             or [])))

            # TODO (artyom, 20170927): we are doing this to be able to use
            # the decorator in Instrument class methods, in which case
            # self is effectively an instrument.
            # To narrow the scope of this hack, we are checking if the
            # command is expecting instrument first.
            if 'instrument' in inspect.getfullargspec(command).args:
                # We are also checking if call arguments have 'self' and
                # don't have instruments specified, in which case
                # instruments should take precedence.
                if 'self' in call_args and 'instrument' not in call_args:
                    call_args['instrument'] = call_args['self']

            command_args.update({
                key: call_args[key]
                for key in
                (set(inspect.getfullargspec(command).args)
                 & call_args.keys())
            })

            if meta:
                command_args['meta'] = meta

            payload = command(**command_args)

            if before:
                publish_command(
                    message={**payload, '$': 'before'})

            res = f(*args, **kwargs)

            if after:
                publish_command(
                    message={**payload, '$': 'after', 'return': res})

            return res
        return decorated

    return decorator


class publish:
    """ Class that allows namespaced decorators with valid mypy types

    These were previously defined by adding them as attributes to the
    publish function, which is not currently supported by mypy:
    https://github.com/python/mypy/issues/2087

    Making a simple class with these as attributes does the same thing
    but in a way that mypy can actually verify.
    """
    before = functools.partial(_do_publish, before=True, after=False)
    after = functools.partial(_do_publish, before=False, after=True)
    both = functools.partial(_do_publish, before=True, after=True)


def _get_args(f, args, kwargs):
    # Create the initial dictionary with args that have defaults
    res = {}

    if inspect.getfullargspec(f).defaults:
        res = dict(
            zip(
                reversed(inspect.getfullargspec(f).args),
                reversed(inspect.getfullargspec(f).defaults)))

    # Update / insert values for positional args
    res.update(dict(zip(inspect.getfullargspec(f).args, args)))

    # Update it with values for named args
    res.update(kwargs)
    return res
