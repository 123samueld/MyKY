using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace MyKYWeb.Migrations
{
    public partial class InitialCreate : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Properties",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Site = table.Column<string>(type: "TEXT", maxLength: 50, nullable: false),
                    Address = table.Column<string>(type: "TEXT", maxLength: 500, nullable: false),
                    FullAddress = table.Column<string>(type: "TEXT", maxLength: 500, nullable: false),
                    StreetAddress = table.Column<string>(type: "TEXT", maxLength: 500, nullable: false),
                    Price = table.Column<string>(type: "TEXT", maxLength: 100, nullable: false),
                    Acres = table.Column<string>(type: "TEXT", maxLength: 100, nullable: false),
                    ListedDate = table.Column<DateTime>(type: "TEXT", nullable: false),
                    County = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    Elevation = table.Column<string>(type: "TEXT", maxLength: 100, nullable: false),
                    Coordinates = table.Column<string>(type: "TEXT", maxLength: 100, nullable: false),
                    DetailUrl = table.Column<string>(type: "TEXT", maxLength: 1000, nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "TEXT", nullable: false),
                    ScrapedAt = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Properties", x => x.Id);
                });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Properties");
        }
    }
}
