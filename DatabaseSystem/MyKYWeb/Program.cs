using System;
using System.IO;
using System.Text.Json;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.FileProviders;

// Get RootPath from shared configuration
string updateThis_rootPath = AppConfig.RootPath;

var builder = WebApplication.CreateBuilder(args);


// Add this line to enable MVC controllers
builder.Services.AddControllers();

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
        updateThis_rootPath+"/Desktop/MyKY/Dashboard"),
    RequestPath = "/dashboard"
});

// Enable static file serving from the Resources directory
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new Microsoft.Extensions.FileProviders.PhysicalFileProvider(
        updateThis_rootPath+"/Desktop/MyKY/Resources"),
    RequestPath = "/resources"
});

// Serve the dashboard.html as the main page
app.MapGet("/", () => Results.Redirect("/dashboard/dashboard.html"));
app.MapGet("/dashboard", () => Results.Redirect("/dashboard/dashboard.html"));

// Add this line to map controller routes (should be after static files)
app.MapControllers();

// Your existing minimal API endpoint (optional—remove if using only controller)
app.MapPost("/kill-app", () =>
{
    try
    {
        // Execute the kill script
        var scriptPath = updateThis_rootPath+"/Desktop/MyKY/kill_protocol.sh";
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