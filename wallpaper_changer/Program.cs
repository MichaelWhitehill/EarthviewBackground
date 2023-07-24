using System.Text.Json;

public class Monitor
{
    public string? Id { get; set; }
    public string? Wallpaper { get; set; }
    public DesktopWallpaperPosition position { get; set; }
}



class Program
{
    static void Main(string[] args)
    {
        if (args.Count() < 1) {
            PrintUsage();
            return;
        }
        var wallpaper = (IDesktopWallpaper)(new DesktopWallpaperClass());
        if (args[0].Equals("monitors"))
        {
            List<Monitor> monitors = ListMonitors(wallpaper);
            Console.Write("[");
            for (int i = 0; i < monitors.Count; ++i) {
                Console.Write(monitors[i].Id);
                if (i < monitors.Count - 1) {
                    Console.Write(',');
                }
            }
            Console.Write("]");
            // foreach (Monitor monitor in monitors) {
            //     Console.WriteLine(monitor.Id);
            // }
            return;
        }
        if (args[0].Equals("set"))
        {
            SetBackground(args, wallpaper);
            return;
        }

        Console.WriteLine("Device count:{0}", wallpaper.GetMonitorDevicePathCount());

        string id_to_set = wallpaper.GetMonitorDevicePathAt(0);
        for (uint i = 0; i < wallpaper.GetMonitorDevicePathCount(); i++)
        {
            var monitorId = wallpaper.GetMonitorDevicePathAt(i);
            // var rect = wallpaper.GetMonitorRECT(monitorId);
            // Console.WriteLine("RECT: {0} {1} {2} {3}", rect.Left, rect.Top, rect.Right, rect.Bottom);
            Console.WriteLine("MonitorId: {0}", monitorId);
            Console.WriteLine("Position: {0}", wallpaper.GetPosition());
            Console.WriteLine("Wallpaper: {0}", wallpaper.GetWallpaper(monitorId));
            Console.WriteLine("");
        }
        Console.WriteLine("id: {0}", id_to_set);
    }
    private static List<Monitor> ListMonitors(IDesktopWallpaper wallpaper)
    {
        List<Monitor> monitors = new List<Monitor>();
        for (uint i = 0; i < wallpaper.GetMonitorDevicePathCount(); i++)
        {
            var monitorId = wallpaper.GetMonitorDevicePathAt(i);
            if (monitorId.Equals(""))
            {
                continue;
            }
            Monitor mon = new Monitor
            {
                Id = monitorId,
                Wallpaper = wallpaper.GetWallpaper(monitorId),
                position = new DesktopWallpaperPosition()
            };
            monitors.Add(mon);
        }
        return monitors;
    }
    private static void SetBackground(string[] args, IDesktopWallpaper wallpaper)
    {
        string mon_id = args[1];
        string path = args[2];
        List<Monitor> mons = ListMonitors(wallpaper);
        Console.WriteLine(mon_id);
        foreach (Monitor m in mons)
        {
            Console.WriteLine(m.Id);
            if (m.Id.Equals(mon_id))
            {
                Console.WriteLine("found matching id");
            }
        }
        wallpaper.SetWallpaper(mon_id, path);
        return;
    }
    private static void PrintUsage() {
        Console.WriteLine("Usage:");
        Console.WriteLine("monitors -- list monitor IDs");
        Console.WriteLine("set <monitorId> <bakcground path>");
    }
}

