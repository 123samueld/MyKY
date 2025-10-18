using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyKYWeb.Data;
using MyKYWeb.Models;

namespace MyKYWeb.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PropertyController : ControllerBase
    {
        private readonly MyKYDbContext _context;
        private readonly ILogger<PropertyController> _logger;

        public PropertyController(MyKYDbContext context, ILogger<PropertyController> logger)
        {
            _context = context;
            _logger = logger;
        }

        [HttpPost]
        public async Task<IActionResult> CreateProperty([FromBody] Property property)
        {
            try
            {
                _context.Properties.Add(property);
                await _context.SaveChangesAsync();
                
                _logger.LogInformation("Property created with ID: {PropertyId}", property.Id);
                return CreatedAtAction(nameof(GetProperty), new { id = property.Id }, property);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating property");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpPost("batch")]
        public async Task<IActionResult> CreateProperties([FromBody] List<Property> properties)
        {
            try
            {
                _context.Properties.AddRange(properties);
                await _context.SaveChangesAsync();
                
                _logger.LogInformation("Batch created {Count} properties", properties.Count);
                return Ok(new { message = $"Successfully created {properties.Count} properties" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating properties batch");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Property>> GetProperty(int id)
        {
            var property = await _context.Properties.FindAsync(id);
            if (property == null)
            {
                return NotFound();
            }
            return property;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Property>>> GetProperties()
        {
            return await _context.Properties.ToListAsync();
        }
    }
}
