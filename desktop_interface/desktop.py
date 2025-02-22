from desktop_interface.idesktop import IDesktopWallpaper

def get_monitors() -> list[str]:
        """Only works for Windows. Gets each monitor ID which is uesed for setting its background"""
        desktop = IDesktopWallpaper.CoCreateInstance()
        mon_count = desktop.GetMonitorDevicePathCount()
        monitors = []
        for i in range(0, mon_count):
            if desktop.GetMonitorDevicePathAt(i) == "":
                continue
            monitors.append(desktop.GetMonitorDevicePathAt(i))
        return monitors

def set_background(monitor_id: str, path: str) -> None:
    """Sets the background for the given monitor"""
    desktop = IDesktopWallpaper.CoCreateInstance()
    desktop.SetWallpaper(monitor_id, path)