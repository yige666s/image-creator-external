#!/usr/bin/env python3
import os
import sys
import json
from typing import Dict, Any, Optional, List


def _get_requests():
    try:
        import requests
        return requests
    except ImportError:
        raise ImportError("requests is required: pip install requests")


class ShortArtClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self._requests = _get_requests()

    def _headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json", "Accept": "*/*"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def _post(self, path: str, payload: dict) -> dict:
        resp = self._requests.post(
            f"{self.base_url}{path}",
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()

    def _get(self, path: str, params: dict = None) -> dict:
        resp = self._requests.get(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def create_project(
        self,
        prompt: str,
        model: str,
        count: int = 1,
        images: Optional[List[str]] = None,
        resolution: str = "2k",
        aspect_ratio: str = "1:1",
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "count": count,
            "resolution": resolution,
            "aspectRatio": aspect_ratio,
        }
        if images:
            payload["images"] = images

        try:
            data = self._post("/api/project/create", payload)
            if data.get("code") == 0:
                d = data.get("data", {})
                return {
                    "status": "success",
                    "project_id": d.get("projectId"),
                    "credit": d.get("credit"),
                    "sub_credit": d.get("subCredit"),
                    "consumed_credit": d.get("consumedCredit"),
                }
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def fetch_status(self, project_ids: str) -> Dict[str, Any]:
        try:
            data = self._get("/api/project/fetch-status", params={"projectIds": project_ids})
            if data.get("code") == 0:
                projects = data.get("data", {}).get("projects", [])
                if projects:
                    project = projects[0]
                    return {
                        "status": "success",
                        "project_status": project.get("status"),
                        "project_error": project.get("error"),
                    }
                return {"status": "error", "error": "No project found"}
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_project(self, project_id: str) -> Dict[str, Any]:
        try:
            data = self._get("/api/project/get", params={"projectID": project_id})
            if data.get("code") == 0:
                project = data["data"].get("project", {})
                domain = project.get("domain", "")
                result = project.get("result") or {}
                images = []
                for img in result.get("images") or []:
                    path = img.get("path", "")
                    images.append({
                        "id": img.get("id"),
                        "path": path,
                        "url": f"{domain}{path}" if domain and not path.startswith("http") else path,
                        "width": img.get("width"),
                        "height": img.get("height"),
                        "risk_level": img.get("riskLevel"),
                    })
                return {
                    "status": "success",
                    "project_status": project.get("status"),
                    "project_error": project.get("error"),
                    "domain": domain,
                    "images": images,
                    "result": result,
                }
            return {"status": "error", "error": data.get("message", "Unknown error")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def upload_image(self, file_path: str) -> Dict[str, Any]:
        requests = self._requests
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        try:
            with open(file_path, "rb") as f:
                resp = requests.post(
                    f"{self.base_url}/api/oss/upload",
                    headers=headers,
                    files={"file": f},
                    data={"type": "image"},
                    timeout=60,
                )
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") == 0:
                d = data.get("data", {})
                return {
                    "status": "success",
                    "path": d.get("path"),
                    "domain": d.get("domain"),
                    "width": d.get("width"),
                    "height": d.get("height"),
                }
            return {"status": "error", "error": data.get("message", "Upload failed")}
        except Exception as e:      
            return {"status": "error", "error": str(e)} 
        
        