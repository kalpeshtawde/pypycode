from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List


def _convert_args(args: list, arg_types: list, namespace: dict) -> list:
    if not arg_types:
        return args

    converted = []
    list_to_linked = namespace.get("list_to_linked")
    list_to_tree = namespace.get("list_to_tree")

    for arg, atype in zip(args, arg_types + [None] * len(args)):
        if atype == "linked_list" and list_to_linked:
            converted.append(list_to_linked(arg))
        elif atype == "tree" and list_to_tree:
            converted.append(list_to_tree(arg))
        else:
            converted.append(arg)
    return converted


class ExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, fn: Callable, test_case: Dict[str, Any], namespace: Dict[str, Any]) -> Any:
        pass


class FunctionStrategy(ExecutionStrategy):
    def execute(self, fn: Callable, test_case: Dict[str, Any], namespace: Dict[str, Any]) -> Any:
        args = test_case.get("args", [])
        arg_types = test_case.get("arg_types", [])
        kwargs = test_case.get("kwargs", {})
        converted_args = _convert_args(args, arg_types, namespace)
        return fn(*converted_args, **kwargs)


class ClassStrategy(ExecutionStrategy):
    def execute(self, fn: Callable, test_case: Dict[str, Any], namespace: Dict[str, Any]) -> Any:
        ctor_args = test_case.get("ctor_args", [])
        ctor_arg_types = test_case.get("ctor_arg_types", [])
        method_name = test_case.get("method")
        method_args = test_case.get("method_args", [])
        method_arg_types = test_case.get("method_arg_types", [])
        
        converted_ctor_args = _convert_args(ctor_args, ctor_arg_types, namespace)
        converted_method_args = _convert_args(method_args, method_arg_types, namespace)
        
        instance = fn(*converted_ctor_args)
        method = getattr(instance, method_name)
        return method(*converted_method_args)


class StatefulStrategy(ExecutionStrategy):
    def execute(self, fn: Callable, test_case: Dict[str, Any], namespace: Dict[str, Any]) -> Any:
        operations = test_case.get("operations", [])
        
        ctor_args = test_case.get("ctor_args", [])
        ctor_arg_types = test_case.get("ctor_arg_types", [])
        converted_ctor_args = _convert_args(ctor_args, ctor_arg_types, namespace)
        instance = fn(*converted_ctor_args)
        
        result = None
        for op in operations:
            method_name = op.get("method")
            method_args = op.get("args", [])
            method_arg_types = op.get("arg_types", [])
            converted_method_args = _convert_args(method_args, method_arg_types, namespace)
            method = getattr(instance, method_name)
            result = method(*converted_method_args)
        
        return result


STRATEGIES = {
    "function": FunctionStrategy(),
    "class": ClassStrategy(),
    "stateful": StatefulStrategy(),
}


def get_strategy(execution_model: str) -> ExecutionStrategy:
    return STRATEGIES.get(execution_model, STRATEGIES["function"])
