"""SVD XML File Parser"""
from xml.etree import ElementTree as ET


class SVDField(object):

    def __init__(self, name, description, offset, width, access):
        self.name = name
        self.description = description
        self.offset = offset
        self.width = width
        self.access = access

    def __repr__(self):
        return repr(self.__dict__)


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

    def __init__(self, vendor, vendor_id, name, version, description, cpu, bit_offset, bit_width, peripherals):
        self.vendor = vendor
        self.vendor_id = vendor_id
        self.name = name
        self.version = version
        self.description = description
        self.cpu = cpu
        self.bit_offset = bit_offset
        self.bit_width = bit_width
        self.peripherals = peripherals

    def __repr__(self):
        return repr(self.__dict__)


class SVDParser(object):
    """THe SVDParser is responsible for mapping the SVD XML to Python Objects"""

    @classmethod
    def for_xml_file(cls, path):
        return cls(ET.parse(path))

    def __init__(self, tree):
        self._tree = tree
        self._root = self._tree.getroot()

    def _get_text(self, node, tag, default=None):
        """Get the text for the provided tag from the provided node"""
        try:
            return node.find(tag).text
        except AttributeError:
            return default

    def _parse_field(self, field_node):
        return SVDField(
            name=self._get_text(field_node, 'name'),
            description=self._get_text(field_node, 'description'),
            offset=self._get_text(field_node, 'offset'),
            width=self._get_text(field_node, 'width'),
            access=self._get_text(field_node, 'access')
        )

    def _parse_register(self, register_node):
        fields = []
        for field_node in register_node.findall('.//field'):
            fields.append(self._parse_field(field_node))
        return SVDRegister(
            name=self._get_text(register_node, 'name'),
            description=self._get_text(register_node, 'description'),
            address_offset=self._get_text(register_node, 'addressOffset'),
            size=self._get_text(register_node, 'size'),
            access=self._get_text(register_node, 'access'),
            reset_value=self._get_text(register_node, 'resetValue'),
            reset_mask=self._get_text(register_node, 'resetMask'),
            fields=fields,
        )

    def _parse_address_block(self, address_block_node):
        return SVDAddressBlock(
            self._get_text(address_block_node, 'offset'),
            self._get_text(address_block_node, 'size'),
            self._get_text(address_block_node, 'usage')
        )

    def _parse_peripheral(self, peripheral_node):
        registers = []
        for register_node in peripheral_node.findall('.//register'):
            registers.append(self._parse_register(register_node))
        address_block = self._parse_address_block(peripheral_node.findall('./addressBlock')[0])
        return SVDPeripheral(
            name=self._get_text(peripheral_node, 'name'),
            description=self._get_text(peripheral_node, 'description'),
            prepend_to_name=self._get_text(peripheral_node, 'prependToName'),
            base_address=self._get_text(peripheral_node, 'baseAddress'),
            address_block=address_block,
            interrupts=None,  # TODO
            registers=registers,
        )

    def _parse_device(self, device_node):
        peripherals = []
        for peripheral_node in device_node.findall('.//peripheral'):
            peripherals.append(self._parse_peripheral(peripheral_node))
        return SVDDevice(
            vendor=self._get_text(device_node, 'vendor'),
            vendor_id=self._get_text(device_node, 'vendorID'),
            name=self._get_text(device_node, 'name'),
            version=self._get_text(device_node, 'version'),
            description=self._get_text(device_node, 'description'),
            cpu=None,  # TODO
            bit_offset=self._get_text(device_node, 'bitOffset'),
            bit_width=self._get_text(device_node, 'bitWidth'),
            peripherals=peripherals,
        )

    def get_device(self):
        """Get the device described by this SVD"""
        return self._parse_device(self._root)
