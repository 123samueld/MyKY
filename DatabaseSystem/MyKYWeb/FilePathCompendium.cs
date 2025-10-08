using System.IO;

namespace MyKYWeb
{
    public static class FilePathCompendium
    { 
        // Base directory for the entire project
        public static string BaseDirectory => Path.GetFullPath(Path.Combine(Directory.GetCurrentDirectory(), "..", "..", "..", ".."));
        
        // Physical directory paths
        public static string DashboardDirectory => Path.Combine(BaseDirectory, "Dashboard");
        public static string ResourcesDirectory => Path.Combine(BaseDirectory, "Resources");
        
        // URL route constants
        public const string DashboardRoute = "/dashboard";
        public const string ResourcesRoute = "/resources";
        public const string RootRoute = "/";
        public const string DatabaseSystemRoute = "/DatabaseSystem/MyKYWeb";
    }
}
