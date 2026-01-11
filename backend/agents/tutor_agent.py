class TutorAgent:
    def suggest_revision(self, user_id, concept_id):
        return {"type": "explain", "concept_id": concept_id}
