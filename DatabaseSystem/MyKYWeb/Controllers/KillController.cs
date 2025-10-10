using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System.Diagnostics;
using System.IO;

namespace MyKYWeb.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class KillController : ControllerBase
    {
        private readonly ILogger<KillController> _logger;

        public KillController(ILogger<KillController> logger)
        {
            _logger = logger;
        }

        [HttpPost]
        public IActionResult KillAll()
        {
            _logger.LogInformation("Kill endpoint hit! Starting script...");

            try
            {
                string scriptPath = "/home/samuel/Desktop/MyKY/kill_protocol.sh";
                
                if (!System.IO.File.Exists(scriptPath))  // Fully qualify to avoid ambiguity with ControllerBase.File method
                {
                    _logger.LogError("Script not found at {ScriptPath}", scriptPath);
                    return BadRequest("Script not found.");
                }

                _logger.LogInformation("Executing script: {ScriptPath}", scriptPath);

                var processInfo = new ProcessStartInfo
                {
                    FileName = "bash",
                    Arguments = $"\"{scriptPath}\"",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };

                using var process = Process.Start(processInfo);
                if (process == null)
                {
                    _logger.LogError("Failed to start bash process");
                    return StatusCode(500, "Failed to start script.");
                }

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                _logger.LogInformation("Script completed. Output: {Output}, Error: {Error}, ExitCode: {ExitCode}", output, error, process.ExitCode);

                if (process.ExitCode != 0)
                {
                    return StatusCode(500, $"Script error: {error}");
                }

                return Ok(new { message = "All processes killed successfully.", output });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error in KillAll");
                return StatusCode(500, $"Unexpected error: {ex.Message}");
            }
        }
    }
}