using System.IO;
using System.Text.Json;

public static class AppConfig
{
    private static string? _rootPath;
    
    public static string RootPath
    {
        get
        {
            if (_rootPath == null)
            {
                // Read the RootPath from config.json
                string jsonFilePath = "../../Utilities/FilePathCompendium.json";
                string jsonString = System.IO.File.ReadAllText(jsonFilePath);
                using JsonDocument doc = JsonDocument.Parse(jsonString);
                string? rootPathFromJson = doc.RootElement.GetProperty("RootPath").GetString();
                _rootPath = string.IsNullOrWhiteSpace(rootPathFromJson) ? "/home/samuel" : rootPathFromJson;
            }
            return _rootPath;
        }
    }
}
