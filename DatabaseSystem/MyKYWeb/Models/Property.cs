using System.ComponentModel.DataAnnotations;

namespace MyKYWeb.Models
{
    public class Property
    {
        [Key]
        public int Id { get; set; }
        
        public string Site { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
        public string FullAddress { get; set; } = string.Empty;
        public string StreetAddress { get; set; } = string.Empty;
        public string Price { get; set; } = string.Empty;
        public string Acres { get; set; } = string.Empty;
        public DateTime ListedDate { get; set; }
        public string County { get; set; } = string.Empty;
        public string Elevation { get; set; } = string.Empty;
        public string Coordinates { get; set; } = string.Empty;
        public string DetailUrl { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime ScrapedAt { get; set; } = DateTime.UtcNow;
    }
}
