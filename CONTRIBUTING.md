# Contributing to TerraPulse AI

First off, thank you for considering contributing to TerraPulse AI! It's people like you that make TerraPulse AI such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check if the bug has already been reported. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (OS, Node version, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and the proposed behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the styleguides
* Include appropriate test cases
* End all files with a newline
* Avoid platform-specific code

## Development Setup

### Prerequisites

- **Node.js 18+** and **npm**
- **Python 3.11+**
- **PostgreSQL 15**
- **Docker & Docker Compose** (recommended)

### Getting Started

1. **Fork & Clone**
   ```bash
   git clone https://github.com/yourusername/terrapulse-ai.git
   cd terrapulse-ai
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   # Copy environment file
   cp .env.example .env
   
   # Start services with Docker
   docker-compose up -d
   ```

4. **Install dependencies**
   ```bash
   # Frontend
   cd frontend && npm install
   
   # Backend
   cd backend && pip install -r requirements.txt
   ```

5. **Make your changes** and test thoroughly

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** to the main repository

## Styleguides

### Python Code Style

* Follow [PEP 8](https://pep8.org/)
* Use 4 spaces for indentation
* Maximum line length: 100 characters
* Use type hints for function definitions
* Write docstrings for all functions

```python
def get_city_data(city: str, days: int = 7) -> Dict[str, Any]:
    """
    Retrieve historical environmental data for a city.
    
    Args:
        city: City name
        days: Number of days to retrieve
        
    Returns:
        Dictionary containing city data
    """
    # Implementation here
    pass
```

### TypeScript/React Code Style

* Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
* Use 2 spaces for indentation
* Use meaningful variable names
* Write JSDoc comments for complex functions
* Use TypeScript strict mode

```typescript
interface CityData {
  city: string
  aqi: number
  temperature: number
}

/**
 * Fetch city environmental data from API
 * @param city - City name
 * @param days - Number of days to retrieve
 * @returns Promise with city data
 */
async function fetchCityData(
  city: string,
  days: number = 7
): Promise<CityData> {
  // Implementation here
}
```

### Commit Message Style

* Use imperative mood ("add feature" not "added feature")
* Start with a capital letter
* Use the present tense
* Limit the first line to 50 characters
* Reference issues when applicable

```
Add WebSocket support for real-time updates

- Implement WebSocket endpoint at /api/ws/cities
- Add real-time data synchronization
- Fixes #123
```

## Testing Requirements

### Backend Tests

```bash
cd backend
python -m pytest tests/
python -m pytest tests/ --cov=app
```

### Frontend Tests

```bash
cd frontend
npm run test
npm run test:watch
```

### Type Checking

```bash
# Backend
mypy app/

# Frontend
npm run type-check
```

### Linting

```bash
# Backend
flake8 app/
black app/

# Frontend
npm run lint
```

## Building for Production

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Start production environment
docker-compose -f docker-compose.prod.yml up -d
```

## Documentation

* Keep documentation updated with your changes
* Update README.md if you add new features
* Add docstrings to new functions
* Update CHANGELOG if making significant changes

## Additional Notes

### Issue and Pull Request Labels

* **bug** - Something isn't working
* **enhancement** - New feature or request
* **documentation** - Improvements or additions to documentation
* **good first issue** - Good for newcomers
* **help wanted** - Extra attention is needed
* **question** - Further information is requested

## Questions?

Feel free to open an issue with the `question` label or contact us at support@terrapulse.ai

---

**Happy Contributing! 🎉**
