import json
from datetime import datetime
from pathlib import Path
from config.settings import PROJECTS_DIR, PROJECT_STATUSES, TASK_TYPES


class ProjectManager:
    def __init__(self):
        self.projects_file = PROJECTS_DIR / "projects.json"
        self.projects = self._load()

    def _load(self) -> dict:
        if self.projects_file.exists():
            with open(self.projects_file, "r") as f:
                return json.load(f)
        return {"projects": []}

    def _save(self):
        with open(self.projects_file, "w") as f:
            json.dump(self.projects, f, indent=2)

    def create_project(
        self,
        name: str,
        client: str,
        task_type: str,
        budget: float = 0,
        deadline: str = "",
        description: str = "",
    ) -> dict:
        project = {
            "id": len(self.projects["projects"]) + 1,
            "name": name,
            "client": client,
            "task_type": task_type,
            "budget": budget,
            "deadline": deadline,
            "description": description,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "tasks": [],
            "earnings": 0,
        }
        self.projects["projects"].append(project)
        self._save()
        return project

    def get_project(self, project_id: int) -> dict:
        for p in self.projects["projects"]:
            if p["id"] == project_id:
                return p
        return None

    def update_status(self, project_id: int, status: str) -> bool:
        if status not in PROJECT_STATUSES:
            return False
        for p in self.projects["projects"]:
            if p["id"] == project_id:
                p["status"] = status
                p["updated_at"] = datetime.now().isoformat()
                self._save()
                return True
        return False

    def add_task(self, project_id: int, task: dict) -> bool:
        for p in self.projects["projects"]:
            if p["id"] == project_id:
                task["created_at"] = datetime.now().isoformat()
                task["done"] = False
                p["tasks"].append(task)
                p["updated_at"] = datetime.now().isoformat()
                self._save()
                return True
        return False

    def complete_task(self, project_id: int, task_index: int) -> bool:
        for p in self.projects["projects"]:
            if p["id"] == project_id:
                if 0 <= task_index < len(p["tasks"]):
                    p["tasks"][task_index]["done"] = True
                    p["tasks"][task_index]["completed_at"] = datetime.now().isoformat()
                    p["updated_at"] = datetime.now().isoformat()
                    self._save()
                    return True
        return False

    def record_earning(self, project_id: int, amount: float) -> bool:
        for p in self.projects["projects"]:
            if p["id"] == project_id:
                p["earnings"] += amount
                p["updated_at"] = datetime.now().isoformat()
                self._save()
                return True
        return False

    def list_projects(self, status: str = None) -> list:
        projects = self.projects["projects"]
        if status:
            projects = [p for p in projects if p["status"] == status]
        return projects

    def get_stats(self) -> dict:
        all_projects = self.projects["projects"]
        return {
            "total_projects": len(all_projects),
            "active": sum(1 for p in all_projects if p["status"] in ["in_progress", "pending"]),
            "completed": sum(1 for p in all_projects if p["status"] == "completed"),
            "total_earnings": sum(p.get("earnings", 0) for p in all_projects),
            "by_status": {
                s: sum(1 for p in all_projects if p["status"] == s)
                for s in PROJECT_STATUSES
            },
        }

    def delete_project(self, project_id: int) -> bool:
        original_len = len(self.projects["projects"])
        self.projects["projects"] = [
            p for p in self.projects["projects"] if p["id"] != project_id
        ]
        if len(self.projects["projects"]) < original_len:
            self._save()
            return True
        return False
