import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export interface SearchResult {
    vc_id: number;       // LMSVideoContents.VCId (PK)
    subtopic_id: number; // LMSSubTopicMaster.SubTopicID (FK)
    subtopic: string;    // matched subtopic text
    caption: string;     // VideoCaption
    file_name: string;   // VideoFileName
    thumbnail: string;   // Thumbnail
    score: number;       // cosine similarity (0–1)
}

export interface SearchResponse {
    query: string;
    results: SearchResult[];
    total: number;
    time_ms: number;
}

export async function semanticSearch(
    query: string,
    top_k: number = 5
): Promise<SearchResponse> {
    const { data } = await axios.post<SearchResponse>(`${API_BASE}/search`, {
        query,
        top_k,
    });
    return data;
}

export async function healthCheck(): Promise<boolean> {
    try {
        await axios.get(`${API_BASE}/health`);
        return true;
    } catch {
        return false;
    }
}
