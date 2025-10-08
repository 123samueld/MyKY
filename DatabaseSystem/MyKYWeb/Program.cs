var builder = WebApplication.CreateBuilder(args);

// Configure the server to listen on port 5000 for HTTP
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenLocalhost(5000); // HTTP on port 5000
});

var app = builder.Build();

// Enable static file serving from the Dashboard directory
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new Microsoft.Extensions.FileProviders.PhysicalFileProvider(
        "/home/samuel/Desktop/MyKY/Dashboard"),
    RequestPath = "/dashboard"
});

// Enable static file serving from the Resources directory
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new Microsoft.Extensions.FileProviders.PhysicalFileProvider(
        "/home/samuel/Desktop/MyKY/Resources"),
    RequestPath = "/resources"
});

// Serve the dashboard.html as the main page
app.MapGet("/", () => Results.Redirect("/dashboard/dashboard.html"));
app.MapGet("/dashboard", () => Results.Redirect("/dashboard/dashboard.html"));

// Kill application endpoint
app.MapPost("/kill-app", () =>
{
    try
    {
        // Execute the kill script
        var scriptPath = "/home/samuel/Desktop/MyKY/kill_protocol.sh";
        var process = new System.Diagnostics.Process
        {
            StartInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "bash",
                Arguments = scriptPath,
                UseShellExecute = false,
                CreateNoWindow = true
            }
        };
        process.Start();
        process.WaitForExit();
        
        return Results.Ok("Kill signal sent successfully");
    }
    catch (System.Exception ex)
    {
        return Results.Problem($"Failed to execute kill script: {ex.Message}");
    }
});

app.Run();