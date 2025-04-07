import os
import asyncio
from httpx import AsyncClient, HTTPError, RequestError
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastmcp import FastMCP
import json
from datetime import datetime, timedelta

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

# Initialize the MCP server
mcp = FastMCP("job_links")

async def search_web(query: str) -> dict:
    """
    Searches the web using the Serper API for job links.
    Args:
        query: The search query (e.g., "Software Engineer jobs in New York").
    Returns:
        JSON response with search results.
    """
    api_key = os.getenv('SERPER_API_KEY')
    if not api_key:
        print("Error: SERPER_API_KEY environment variable not set or found.")
        return {"error": "API key not configured"}

    try:
        async with AsyncClient() as client:
            print(f"Attempting Serper search for query: '{query}'")
            response = await client.post(
                url="https://google.serper.dev/search",
                headers={"X-API-KEY": api_key},
                json={
                    "q": query,
                    "gl": "us",  # Set region to US
                    "hl": "en",  # Set language to English
                    "num": 100  # Get more results
                }
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Error during search: {e}")
        return {"error": str(e)}

@mcp.tool()
async def get_job_links(query: str, platform: str = "LinkedIn") -> dict:
    """
    Retrieves job links based on user profile and platform.
    Args:
        query: Search query (e.g., "Software Engineer")
        platform: Job board to search (e.g., "LinkedIn", "Indeed")
    Returns:
        Dictionary containing job results.
    """
    # Parse location from query if specified
    location = None
    if "chicago" in query.lower():
        location = "Chicago"
        query = query.lower().replace("chicago", "").strip()
    elif "new york" in query.lower():
        location = "New York"
        query = query.lower().replace("new york", "").strip()
    elif "los angeles" in query.lower():
        location = "Los Angeles"
        query = query.lower().replace("los angeles", "").strip()
    elif "san francisco" in query.lower():
        location = "San Francisco" 
        query = query.lower().replace("san francisco", "").strip()
    
    # Clean query for search
    base_query = query.strip()
    
    # Add time filter for the last 24 hours
    time_filter = "when:24h"
    
    # Construct search query to focus on job listings with location
    if platform.lower() == "linkedin":
        if location:
            search_query = f'site:linkedin.com/jobs "{base_query}" "{location}" {time_filter}'
        else:
            search_query = f'site:linkedin.com/jobs "{base_query}" "United States" {time_filter}'
    else:
        if location:
            search_query = f'site:{platform.lower()}.com/jobs "{base_query}" "{location}" {time_filter}'
        else:
            search_query = f'site:{platform.lower()}.com/jobs "{base_query}" "United States" {time_filter}'
    
    print(f"Searching with query: {search_query}")
    search_results = await search_web(search_query)

    if "error" in search_results:
        return search_results

    jobs = []
    for result in search_results.get("organic", []):
        url = result.get("link")
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        
        # Accept any job-related results
        if url and title:
            # Extract company and location from title or snippet
            company = "N/A"
            job_location = location if location else "N/A"
            
            # Try to extract company from title
            if " | " in title:
                parts = title.split(" | ")
                if len(parts) > 1:
                    title = parts[0].strip()
                    company = parts[1].strip()
                    
            # Try to extract location from snippet if not already known
            if job_location == "N/A":
                if " in " in snippet:
                    job_location = snippet.split(" in ")[1].split(".")[0].strip()
                elif "· " in snippet:
                    snippet_parts = snippet.split("· ")
                    if len(snippet_parts) > 1:
                        job_location = snippet_parts[1].strip()
            
            jobs.append({
                "title": title.strip(),
                "company": company,
                "location": job_location,
                "url": url,
                "description": snippet
            })
    
    return {
        "jobs": jobs,
        "total": len(jobs),
        "search_query": search_query,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("Starting MCP server for job search...")
    asyncio.run(mcp.run(transport="stdio"))