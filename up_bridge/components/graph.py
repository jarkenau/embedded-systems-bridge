"""Module to convert UP Plan to Dependency Graph and execute it."""
from typing import Union

import networkx as nx
from unified_planning.plans.sequential_plan import SequentialPlan
from unified_planning.plans.time_triggered_plan import TimeTriggeredPlan
from unified_planning.shortcuts import Fraction


def plan_to_dependency_graph(plan: Union[SequentialPlan, TimeTriggeredPlan]) -> nx.DiGraph:
    """Convert UP Plan to Dependency Graph."""
    if isinstance(plan, SequentialPlan):
        return _sequential_plan_to_dependency_graph(plan)
    if isinstance(plan, TimeTriggeredPlan):
        return _time_triggered_plan_to_dependency_graph(plan)
    raise NotImplementedError("Plan type not supported")


def _sequential_plan_to_dependency_graph(plan: SequentialPlan) -> nx.DiGraph:
    """Convert UP Plan to Dependency Graph."""
    dependency_graph = nx.DiGraph()
    edge = "start"
    dependency_graph.add_node(edge, action="start", parameters=())
    for action in plan.actions:
        child = action.action.name
        child_name = f"{child}{action.actual_parameters}"
        dependency_graph.add_node(child_name, action=child, parameters=action.actual_parameters)
        dependency_graph.add_edge(edge, child_name)
        edge = child_name

    dependency_graph.add_node("end", action="end", parameters=())
    dependency_graph.add_edge(edge, "end")
    return dependency_graph


def _time_triggered_plan_to_dependency_graph(plan: TimeTriggeredPlan) -> nx.DiGraph:
    """Convert UP Plan to Dependency Graph."""
    dependency_graph = nx.DiGraph()
    edge = "start"
    dependency_graph.add_node(edge, action="start", parameters=())
    # TODO: Add timing information
    for (start, action, duration) in plan.timed_actions:
        child = action.action.name
        duration = float(duration.numerator) / float(duration.denominator)
        child_name = f"{child}{action.actual_parameters}({duration}s)"
        dependency_graph.add_node(child_name, action=child, parameters=action.actual_parameters)
        dependency_graph.add_edge(edge, child_name, weight=duration)
        edge = child_name

    dependency_graph.add_node("end", action="end", parameters=())
    dependency_graph.add_edge(edge, "end")
    return dependency_graph
