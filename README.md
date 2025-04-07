# Job Search Automation MCP 

This project is a Python-based MCP designed to automate job searches across popular platforms like LinkedIn and Indeed. It leverages web scraping, API integration, and natural language processing to retrieve job postings based on user-defined queries.

---

## Features

- **Search for Jobs**: Retrieve job postings from platforms like LinkedIn, Indeed, or other job boards.
- **Location Filtering**: Automatically parse and filter jobs by location (e.g., Chicago, New York, Los Angeles).
- **Time Filtering**: Focus on recent job postings (e.g., last 24 hours).
- **Company and Location Extraction**: Extract company names and locations from search results.
- **Customizable Search Queries**: Tailor your search queries to specific roles or industries.
- **FastMCP Integration**: Use FastMCP to expose the functionality as a tool for broader workflows.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/job-search-tool.git
cd job-search-tool
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Serper API key:

```
SERPER_API_KEY=your_serper_api_key_here
```


---

## Usage

### Running the Application

To start the tool, simply run:

```bash
python main.py
```

This will start the FastMCP server, allowing you to interact with the job search functionality.

### Example Query

Use the `get_job_links` function to search for jobs. For example:

```python
await get_job_links(query="Software Engineer", platform="LinkedIn")
```

This will return a list of software engineering jobs posted on LinkedIn in the last 24 hours.

---

## Environment Variables

The application uses environment variables for configuration. Make sure to set these in your `.env` file:


| Variable | Description |
| :-- | :-- |
| `SERPER_API_KEY` | API key for Serper (Google Search API). |

---

## Project Structure

```
job-search-tool/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not included in repo)
└── README.md            # Project documentation
```

---

## Dependencies

The project uses the following Python libraries:

- `httpx`: For making asynchronous HTTP requests.
- `beautifulsoup4`: For parsing HTML content.
- `fastmcp`: To expose functions as tools for broader workflows.
- `dotenv`: For managing environment variables.

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## How It Works

1. **Search Query Construction**: The tool constructs a search query based on user input, platform, and location filters.
2. **Serper API Integration**: The query is sent to the Serper API, which performs a Google search and returns results.
3. **Result Parsing**: The tool parses the results to extract relevant information like job title, company, location, and description.
4. **Output**: The results are returned as a JSON object containing job details.

---

## Example Output

A sample response from `get_job_links` might look like this:

```json
{
  "jobs": [
    {
      "title": "Software Engineer",
      "company": "Google",
      "location": "New York",
      "url": "https://www.linkedin.com/jobs/view/123456789",
      "description": "Join our team as a Software Engineer..."
    },
    {
      "title": "Backend Developer",
      "company": "Amazon",
      "location": "Chicago",
      "url": "https://www.linkedin.com/jobs/view/987654321",
      "description": "We are hiring a Backend Developer..."
    }
  ],
  "total": 2,
  "search_query": 'site:linkedin.com/jobs "Software Engineer" "United States" when:24h',
  "timestamp": "2025-04-07T03:37:00"
}
```
Example:
![image](https://github.com/user-attachments/assets/4eee3616-bdf6-4f0c-b462-276bab350909)
