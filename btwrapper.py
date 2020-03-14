import time
import pexpect
import subprocess
import sys





class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass


class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("sudo bluetoothctl", echo = False)

    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect([pexpect.EOF,"bluetooth", "Gamepad_ios","Gamepad."])
        if not start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split(b'\r\n')


    def power_on(self):
        """Start agent"""
        try:
            out = self.get_output("power on")
            print("power on")
        except BluetoothctlError as e:
            print(e)
            return None

    def agent_on(self):
        """Start agent"""
        try:
            out = self.get_output("agent on")
            print("agent Registered Successfully")
        except BluetoothctlError as e:
            print(e)
            return None

    def default_agent(self):
        """Start default agent"""
        try:
            out = self.get_output("default-agent")
            print("set as default agent")
        except BluetoothctlError as e:
            print(e)
            return None




    def start_scan(self):
        """Start bluetooth scanning process."""
        try:
            out = self.get_output("scan on")
        except BluetoothctlError as e:
            print(e)
            return None

    def make_discoverable(self):
        """Make device discoverable."""
        try:
            out = self.get_output("discoverable on")
        except BluetoothctlError as e:
            print(e)
            return None

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"] #[\x1b[0;
        string_valid = not any(keyword in info_string.decode('utf8') for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index(b"Device")
            except ValueError:
                pass
            else:
                #print(type(device_position))
                if device_position > -1:

                    attribute_list =str(info_string[device_position:]).split(" ", 2)
                    device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2]
                    }

        return device

    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        try:
            out = self.get_output("devices")
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            out = self.get_output("paired-devices")
            #print(out)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                #print(device)
                if device:
                    paired_devices.append(device)

            return paired_devices

    def get_discoverable_devices(self):
        """Filter paired devices out of available."""
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]

    def get_device_info(self, mac_address):
        """Get device info by mac address."""
        try:
            out = self.get_output("info " + mac_address)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            return out

    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            out = self.get_output("pair " + mac_address, 5)
        except BluetoothctlError as e:
            print(e)
            return None
        #else:
        #    res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
        #    success = True if res == 1 else False
        #    return success

    def remove(self, mac_address):
        """Remove paired device by mac address, return success of the operation."""
        try:
            out = self.get_output("remove " + mac_address, 3)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["not available", "Device has been removed", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address, 5)
        except BluetoothctlError as e:
            print(e)
            return None
        #else:
        #    res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
        #    success = True if res == 1 else False
        #    return success

    def disconnect(self, mac_address):
        """Try to disconnect to a device by mac address."""
        try:
            out = self.get_output("disconnect " + mac_address, 2)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False
            return success


if __name__ == "__main__":

    print("Init bluetooth...")
    bl = Bluetoothctl()
    bl.power_on()
    bl.agent_on() 
    bl.default_agent()
    bl.get_paired_devices()
