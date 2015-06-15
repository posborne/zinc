import six


def _check_type(value, expected_type):
    """Perform type checking on the provided value

    This is a helper that will raise ``TypeError`` if the provided value is
    not an instance of the provided type.  This method should be used sparingly
    but can be good for preventing problems earlier when you want to restrict
    duck typing to make the types of fields more obvious.

    If the value passed the type check it will be returned from the call.
    """
    if not isinstance(value, expected_type):
        raise TypeError("Value {value!r} has unexpected type {actual_type!r}, expected {expected_type!r}".format(
            value=value,
            expected_type=expected_type,
            actual_type=type(value),
        ))
    return value


class SVDEnumeratedValue(object):

    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __repr__(self):
        return repr(self.__dict__)


class SVDField(object):

    def __init__(self, name, description, bit_offset, bit_width, access, enumerated_values):
        self.name = name
        self.description = description
        self.bit_offset = bit_offset
        self.bit_width = bit_width
        self.access = access
        self.enumerated_values = enumerated_values

    def __repr__(self):
        return repr(self.__dict__)

    @property
    def is_enumerated_type(self):
        """Return True if the field is an enumerated type"""
        return self.enumerated_values is not None

    @property
    def is_reserved(self):
        return self.name.lower() == "reserved"


class SVDRegister(object):

    def __init__(self, name, description, address_offset, size, access, reset_value, reset_mask, fields):
        self.name = name
        self.description = description
        self.address_offset = address_offset
        self.size = size
        self.access = access
        self.reset_value = reset_value
        self.reset_mask = reset_mask
        self.fields = fields

    def __repr__(self):
        return repr(self.__dict__)


class SVDAddressBlock(object):

    def __init__(self, offset, size, usage):
        self.offset = offset
        self.size = size
        self.usage = usage

    def __repr__(self):
        return repr(self.__dict__)


class SVDInterrupt(object):

    def __init__(self, name, value):
        self.name = name
        self.value = _check_type(value, six.integer_types)


class SVDPeripheral(object):

    def __init__(self, name, description, prepend_to_name, base_address, address_block, interrupts, registers):
        self.name = name
        self.description = description
        self.prepend_to_name = prepend_to_name
        self.base_address = base_address
        self.address_block = address_block
        self.interrupts = interrupts
        self.registers = registers

    def __repr__(self):
        return repr(self.__dict__)


class SVDDevice(object):

    def __init__(self, vendor, vendor_id, name, version, description, cpu, address_unit_bits, width, peripherals):
        self.vendor = vendor
        self.vendor_id = vendor_id
        self.name = name
        self.version = version
        self.description = description
        self.cpu = cpu
        self.address_unit_bits = _check_type(address_unit_bits, six.integer_types)
        self.width = _check_type(width, six.integer_types)
        self.peripherals = peripherals

    def __repr__(self):
        return repr(self.__dict__)


