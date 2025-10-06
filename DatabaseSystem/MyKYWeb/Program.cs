var builder = WebApplication.CreateBuilder(args);

// Configure the server to listen on port 5000 for HTTP
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenLocalhost(5000); // HTTP on port 5000
});

var app = builder.Build();

app.MapGet("/", () => "Goodbye Cruel World!");
app.MapGet("/dashboard", () => "Goodbye Cruel World!");

app.Run();