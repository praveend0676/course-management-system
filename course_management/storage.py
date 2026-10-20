import json
from pathlib import Path


class JsonStorage:
    def __init__(self, path="data/course_data.json"):
        self.path = Path(path)

    def save(self, payload):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temp.replace(self.path)

    def load(self):
        if not self.path.exists():
            return {"students": [], "mentors": [], "courses": [], "enrollments": []}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Stored data must be a JSON object")
        return {key: data.get(key, []) for key in ("students", "mentors", "courses", "enrollments")}
