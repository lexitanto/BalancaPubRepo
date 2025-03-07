from pydbus import SystemBus
from gi.repository import GLib

class SimpleBLEServer:
    def __init__(self):
        self.bus = SystemBus()
        self.adapter = self.get_adapter()
        self.setup_adapter()
        print("🔵 BLE Server is running... Waiting for connections.")

    def get_adapter(self):
        """Find the Bluetooth adapter (hci0)."""
        obj_manager = self.bus.get("org.bluez", "/")
        for path, interfaces in obj_manager.GetManagedObjects().items():
            if "org.bluez.Adapter1" in interfaces:
                return self.bus.get("org.bluez", path)
        raise Exception("No Bluetooth adapter found.")

    def setup_adapter(self):
        """Enable the adapter and make it discoverable."""
        self.adapter.Powered = True
        self.adapter.Pairable = True
        self.adapter.Discoverable = True

    def monitor_connections(self):
        """Monitor device connections."""
        def properties_changed(connection, sender, path, interface, signal, parameters):
            """Callback chamado quando alguma propriedade muda."""
            iface, changed, _ = parameters
            if iface == "org.bluez.Device1" and "Connected" in changed:
                if changed["Connected"]:  # Se o dispositivo conectou
                    print(f"✅ Device connected!")
                else:  # Se o dispositivo desconectou
                    print("❌ Device disconnected.")

        # Conectar ao sinal "PropertiesChanged" corretamente
        self.bus.con.signal_subscribe(
            sender="org.bluez",
            interface_name="org.freedesktop.DBus.Properties",
            member="PropertiesChanged",
            object_path=None,  # Qualquer caminho de objeto
            arg0=None,  # Aceita todas as mudanças de propriedades
            flags=0,  # Sem flags adicionais
            callback=properties_changed
        )



if __name__ == "__main__":
    server = SimpleBLEServer()
    server.monitor_connections()
    loop = GLib.MainLoop()
    loop.run()
