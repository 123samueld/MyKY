using Microsoft.EntityFrameworkCore;
using MyKYWeb.Models;

namespace MyKYWeb.Data
{
    public class MyKYDbContext : DbContext
    {
        public MyKYDbContext(DbContextOptions<MyKYDbContext> options) : base(options)
        {
        }

        public DbSet<Property> Properties { get; set; } = null!;

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            
            // Configure Property entity
            modelBuilder.Entity<Property>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Site).HasMaxLength(50);
                entity.Property(e => e.Address).HasMaxLength(500);
                entity.Property(e => e.FullAddress).HasMaxLength(500);
                entity.Property(e => e.StreetAddress).HasMaxLength(500);
                entity.Property(e => e.Price).HasMaxLength(100);
                entity.Property(e => e.Acres).HasMaxLength(100);
                entity.Property(e => e.County).HasMaxLength(200);
                entity.Property(e => e.Elevation).HasMaxLength(100);
                entity.Property(e => e.Coordinates).HasMaxLength(100);
                entity.Property(e => e.DetailUrl).HasMaxLength(1000);
            });
        }
    }
}
