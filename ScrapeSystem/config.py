import json
import os
from pathlib import Path

class ScrapeConfig:
    """Configuration class for ScrapeSystem that reads from FilePathCompendium.json"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScrapeConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()
    
    def _load_config(self):
        """Load configuration from FilePathCompendium.json"""
        try:
            # Get the project root directory (two levels up from ScrapeSystem)
            script_dir = Path(__file__).parent
            project_root = script_dir.parent
            
            # Path to the JSON config file
            config_file = project_root / "Utilities" / "FilePathCompendium.json"
            
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # Extract paths
            self._config = {
                'root_path': config_data.get('RootPath', '/home/samuel'),
                'project_root': str(project_root),
                'utilities_dir': str(project_root / 'Utilities'),
                'scraped_data_cache': str(project_root / 'ScrapeSystem' / 'ScrapedDataCache'),
                'chromedriver_path': str(project_root / 'Utilities' / 'chromedriver_linux64' / 'chromedriver'),
            }
            
        except Exception as e:
            print(f"Warning: Could not load config from FilePathCompendium.json: {e}")
            # Fallback to default paths
            self._config = {
                'root_path': '/home/samuel',
                'project_root': str(Path(__file__).parent.parent),
                'utilities_dir': str(Path(__file__).parent.parent / 'Utilities'),
                'scraped_data_cache': str(Path(__file__).parent / 'ScrapedDataCache'),
                'chromedriver_path': str(Path(__file__).parent.parent / 'Utilities' / 'chromedriver_linux64' / 'chromedriver'),
            }
    
    @property
    def root_path(self):
        """Get the root path from configuration"""
        return self._config['root_path']
    
    @property
    def project_root(self):
        """Get the project root directory"""
        return self._config['project_root']
    
    @property
    def utilities_dir(self):
        """Get the utilities directory path"""
        return self._config['utilities_dir']
    
    @property
    def scraped_data_cache(self):
        """Get the scraped data cache directory"""
        return self._config['scraped_data_cache']
    
    @property
    def chromedriver_path(self):
        """Get the ChromeDriver executable path"""
        return self._config['chromedriver_path']
    
    def get_chrome_options(self):
        """Get Chrome options for Selenium WebDriver"""
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')  # Run in background
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        # Set ChromeDriver path
        options.binary_location = self.chromedriver_path
        
        return options

# Create a global instance
config = ScrapeConfig()
