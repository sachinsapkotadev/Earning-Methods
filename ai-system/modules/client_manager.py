import json
from datetime import datetime
from pathlib import Path
from config.settings import PROJECTS_DIR


class ClientManager:
    def __init__(self):
        self.clients_file = PROJECTS_DIR / "clients.json"
        self.clients = self._load()

    def _load(self) -> dict:
        if self.clients_file.exists():
            with open(self.clients_file, "r") as f:
                return json.load(f)
        return {"clients": []}

    def _save(self):
        with open(self.clients_file, "w") as f:
            json.dump(self.clients, f, indent=2)

    def add_client(
        self,
        name: str,
        email: str = "",
        platform: str = "",
        notes: str = "",
    ) -> dict:
        client = {
            "id": len(self.clients["clients"]) + 1,
            "name": name,
            "email": email,
            "platform": platform,
            "notes": notes,
            "total_projects": 0,
            "total_earnings": 0,
            "created_at": datetime.now().isoformat(),
            "projects": [],
        }
        self.clients["clients"].append(client)
        self._save()
        return client

    def get_client(self, client_id: int) -> dict:
        for c in self.clients["clients"]:
            if c["id"] == client_id:
                return c
        return None

    def find_client(self, name: str) -> dict:
        name_lower = name.lower()
        for c in self.clients["clients"]:
            if name_lower in c["name"].lower():
                return c
        return None

    def update_client(self, client_id: int, **kwargs) -> bool:
        for c in self.clients["clients"]:
            if c["id"] == client_id:
                for key, value in kwargs.items():
                    if key in c:
                        c[key] = value
                self._save()
                return True
        return False

    def add_project(self, client_id: int, project_name: str) -> bool:
        for c in self.clients["clients"]:
            if c["id"] == client_id:
                c["total_projects"] += 1
                c["projects"].append(project_name)
                self._save()
                return True
        return False

    def add_earning(self, client_id: int, amount: float) -> bool:
        for c in self.clients["clients"]:
            if c["id"] == client_id:
                c["total_earnings"] += amount
                self._save()
                return True
        return False

    def list_clients(self) -> list:
        return self.clients["clients"]

    def get_stats(self) -> dict:
        all_clients = self.clients["clients"]
        return {
            "total_clients": len(all_clients),
            "total_earnings": sum(c.get("total_earnings", 0) for c in all_clients),
            "top_earning": sorted(
                all_clients, key=lambda x: x.get("total_earnings", 0), reverse=True
            )[:5],
        }

    def delete_client(self, client_id: int) -> bool:
        original = len(self.clients["clients"])
        self.clients["clients"] = [
            c for c in self.clients["clients"] if c["id"] != client_id
        ]
        if len(self.clients["clients"]) < original:
            self._save()
            return True
        return False
