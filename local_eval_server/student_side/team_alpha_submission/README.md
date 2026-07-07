# Team Alpha Example Submission

This folder simulates the content that would be mounted inside a student Docker
container.

The agent exposes:

```python
def make_agent() -> StudentAgent:
    ...
```

The teacher-side evaluator owns the ChemWorld environment and sends this agent
only sanitized task information, public observations, rewards, and info fields.
