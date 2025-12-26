from pydantic import BaseModel

class AgentGuidedModel(BaseModel):
    """
    Base class for schemas that must guide an AI agent.
    """

    @classmethod
    def example(cls) -> BaseModel:
        raise NotImplementedError(
            f"{cls.__name__} must implement example()"
        )

    @classmethod
    def example_json(cls) -> dict:
        return cls.example().model_dump(mode="json")
