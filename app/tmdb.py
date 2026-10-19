import httpx
from fastapi import HTTPException, status
from .config import settings 

Base_URL = "https://api.themoviedb.org/3"



def search_media(query: str):
    try:
        response = httpx.get(
            f"{Base_URL}/search/multi", 
            params={"api_key": settings.TMDB_API_KEY, "query": query},
            timeout = 10.0)
        response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=f"External movie database is currently unreachable due to network restrictions. Please try again later.")
      
    if not response.json()["results"]:
        return []
    
    results =  response.json()["results"]

    return [
        {
            "tmdb_id": r["id"],
            "title": r.get("title") or r.get("name"),
            "kind": "movie" if r["media_type"] == "movie" else "show",
            "overview": r.get("overview"),
            "poster_path": r.get("poster_path"),
        }
        for r in results
        if r["media_type"] in ("movie", "tv")
    ]

    

def get_media_details(tmdb_id: int, kind: str):
    path = "movie" if kind == "movie" else "tv"
    response = httpx.get(
        f"{Base_URL}/{path}/{tmdb_id}",
        params = {"api_key": settings.TMDB_API_KEY},
        timeout = 10.0
    )
    response.raise_for_status()
    data = response.json()
    return data.get("title") or data.get("name")
