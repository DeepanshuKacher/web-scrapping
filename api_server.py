from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any
import uvicorn
import main_app_advanced

app = FastAPI(
    title="Scraping API",
    description="API for scraping data using queries or URLs. Automatically generates docs at /docs (Swagger UI) and /redoc (ReDoc).",
    version="1.0.0"
)

class ScrapeRequest(BaseModel):
    mode: Literal["query", "url"] = Field(..., description="Choose 'query' to search by queries or 'url' to scrape from URLs.")
    scrape_level: Literal["basic", "medium", "advanced"] = Field(..., description="Level of scraping detail.")
    queries: Optional[List[str]] = Field(None, description="List of search queries (required if mode is 'query').")
    seed_urls: Optional[List[str]] = Field(None, description="List of URLs to scrape (required if mode is 'url').")
    output_type: Literal["csv", "json"] = Field("json", description="Output format.")

class ScrapeResponse(BaseModel):
    message: Optional[str] = None
    error: Optional[str] = None
    data: Optional[Any] = None


@app.post("/process", summary="Process scraping request", tags=["Scraping"])
async def process(request: ScrapeRequest):
    """
    Process a scraping request based on mode, queries/urls, and scrape level.
    """
    req_dict = request.model_dump() if hasattr(request, 'model_dump') else request.dict()
    result = main_app_advanced.run(req_dict)
    # If error or message, return as JSON
    if isinstance(result, dict) and ("error" in result or "message" in result):
        return JSONResponse(content=result)
    # If CSV requested, return file as attachment
    if req_dict.get("output_type", "json") == "csv":
        # Assuming save_as_csv always writes to 'output.csv' in the current directory
        # If your save_as_csv uses a different filename, adjust here
        return FileResponse(
            path="output.csv", 
            filename="output.csv", 
            media_type="text/csv"
        )
    # Otherwise, return JSON data
    return JSONResponse(content={"data": result})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
