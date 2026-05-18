from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List


class ExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, fn: Callable, test_case: Dict[str, Any], namespace: Dict[str, Any]) -> Any:
        pass


class FunctionStrategy(ExecutionStrategy):
    def execute(self, fn: Callable, test_case: Dict[str, Any], namespace: Dict[str, Any]) -> Any:
        args = test_case.get("args", [])
        kwargs = test_case.get("kwargs", {})
        return fn(*args, **kwargs)


class ClassStrategy(ExecutionStrategy):
    def execute(self, fn: Callable, test_case: Dict[str, Any], namespace: Dict[str, Any]) -> Any:
        ctor_args = test_case.get("ctor_args", [])
        method_name = test_case.get("method")
        method_args = test_case.get("method_args", [])
        
        instance = fn(*ctor_args)
        method = getattr(instance, method_name)
        return method(*method_args)


class StatefulStrategy(ExecutionStrategy):
    def execute(self, fn: Callable, test_case: Dict[str, Any], namespace: Dict[str, Any]) -> Any:
        operations = test_case.get("operations", [])
        
        ctor_args = test_case.get("ctor_args", [])
        instance = fn(*ctor_args)
        
        result = None
        for op in operations:
            method_name = op.get("method")
            method_args = op.get("args", [])
            method = getattr(instance, method_name)
            result = method(*method_args)
        
        return result


STRATEGIES = {
    "function": FunctionStrategy(),
    "class": ClassStrategy(),
    "stateful": StatefulStrategy(),
}


def get_strategy(execution_model: str) -> ExecutionStrategy:
    return STRATEGIES.get(execution_model, STRATEGIES["function"])
