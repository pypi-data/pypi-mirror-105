"""
TimeSeriesSimulation
Author: Thomas Meli
2021

A base set of classes to run a simulation.
"""


class TimeSeries:
    """
    Base Sequence Type for Simulation.

    Can be an array of discrete timesteps.
    Or can be an array of more continuous timesteps.

    """

    def __init__(self, start, end):
        pass

    pass

class DiscreteSeries(TimeSeries):
    """
    A discrete series.

    """

    # super().__init__()

    pass

class ContinuousSeries(TimeSeries):
    """
    A pseudo-continuous series.

    """
    # super().__init__()

    pass



class Agent:
    """
    Base Object type for what is participating in the simulation.

    """
    pass


class AllAgents:
    """
    A Collection type for all of the Agents.
    Receives a list of Agents in the simulation.

    This allows for parallel or async processing.

    """

    def __init__(self, list_of_agents):
        pass

    pass

class Event:
    """
    This is a base class for something that can happen
    between timesteps.

    There are inherited subtyptes that are
    deterministic, stochastic, or extensible to
    something else below.

    """
    pass

class DeterministicEvent(Event):
    pass

class StochasticEvent(Event):
    pass

class EventUpdateManager:
    """
    This encapsulates the event updating at each timestep.

    """