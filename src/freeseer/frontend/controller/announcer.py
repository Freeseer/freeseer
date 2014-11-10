import avahi
import dbus


class ServiceAnnouncer:
    def __init__(self, name, service, port, info):
        bus = dbus.SystemBus()
        server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), avahi.DBUS_INTERFACE_SERVER)
        self.group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()), avahi.DBUS_INTERFACE_ENTRY_GROUP)
        self.service = service
        self.name = name
        self.port = port
        self.info = info

    def announce(self):
        self.group.AddService(avahi.IF_UNSPEC, avahi.PROTO_INET, 0,
                              self.name, self.service, '', '', self.port,
                              avahi.string_array_to_txt_array(self.info))
        self.group.Commit()

    def unpublish(self):
        self.group.Reset()
