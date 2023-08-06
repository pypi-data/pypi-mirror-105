from typing import Optional, Tuple, Union

from atoti.hierarchy import Hierarchy
from atoti.level import Level

from ._utils import CumulativeTimeWindow, CumulativeWindow, LeafLevels, SiblingsWindow
from .scope import Scope


def cumulative(
    level: Level,
    *,
    dense: bool = False,
    partitioning: Optional[Level] = None,
    window: Optional[Union[range, Tuple[Optional[str], Optional[str]]]] = None,
) -> Scope:
    """Create a scope to be used in the computation of cumulative aggregations.

    Cumulative aggregations include cumulative sums (also called running sum or prefix sum), mean, min, max, etc.

    Args:
        level: The level along which the aggregation is performed.
        dense: When ``True``, all members of the level, even those with no value for the underlying measure, will be taken into account for the cumulative aggregation (resulting in repeating values).
        partitioning: The levels in the hierarchy at which to start the aggregation over.
        window: The custom aggregation window.
            The window defines the set of members before and after a given member (using the level comparator) to be considered in the computation of the cumulative aggregation.

            The window can be a:

            * ``range`` starting with a <=0 value and ending with a >=0 value.

               By default the window is ``range(-∞, 0)``, meaning that the value for a given member is computed using all of the members before it and none after it.
            * time period as a two-element tuple starting with an offset of the form ``-xxDxxWxxMxxQxxY`` or ``None`` and ending with an offset of the form ``xxDxxWxxMxxQxxY`` or ``None``.

              For instance, to compute the 5 previous days sliding mean::

                m2 = atoti.agg.mean(m1, scope=tt.scope.cumulative("date", window=("-5D", None)))

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["Year", "Month", "Day", "Quantity"],
        ...     data=[
        ...         (2019, 7, 1, 15.0),
        ...         (2019, 7, 2, 20.0),
        ...         (2019, 6, 1, 25.0),
        ...         (2019, 6, 2, 15.0),
        ...         (2018, 7, 1, 5.0),
        ...         (2018, 7, 2, 10.0),
        ...         (2018, 6, 1, 15.0),
        ...         (2018, 6, 2, 5.0),
        ...     ],
        ... )
        >>> store = session.read_pandas(
        ...     df, store_name="Cumulative", hierarchized_columns=[]
        ... )
        >>> cube = session.create_cube(store)
        >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
        >>> h["Date"] = [store["Year"], store["Month"], store["Day"]]
        >>> m["Cumulative quantity"] = tt.agg.sum(
        ...     m["Quantity.SUM"], scope=tt.scope.cumulative(l["Day"])
        ... )
        >>> m["Cumulative quantity partitioned by month"] = tt.agg.sum(
        ...     m["Quantity.SUM"],
        ...     scope=tt.scope.cumulative(l["Day"], partitioning=l["Month"]),
        ... )
        >>> cube.query(
        ...     m["Quantity.SUM"],
        ...     m["Cumulative quantity"],
        ...     m["Cumulative quantity partitioned by month"],
        ...     levels=[l["Day"]],
        ... )
                       Quantity.SUM Cumulative quantity Cumulative quantity partitioned by month
        Year Month Day
        2018 6     1          15.00               15.00                                    15.00
                   2           5.00               20.00                                    20.00
             7     1           5.00               25.00                                     5.00
                   2          10.00               35.00                                    15.00
        2019 6     1          25.00               60.00                                    25.00
                   2          15.00               75.00                                    40.00
             7     1          15.00               90.00                                    15.00
                   2          20.00              110.00                                    35.00

    """
    if window is not None and isinstance(window, Tuple):
        back = window[0]
        if back is not None and not back.startswith("-"):
            raise ValueError("back period parameter must be a negative time frame.")
        forward = window[1]
        if forward is not None and forward.startswith("-"):
            raise ValueError("forward period parameter must be a positive time frame")
        return CumulativeTimeWindow(level, window, partitioning)

    if window is not None and isinstance(window, range):
        if window.step != 1:
            raise ValueError(
                "Running aggregation windows only support ranges with step of size 1."
            )
        if window.start > 0 or window.stop < 0:
            raise ValueError(
                "Running aggregation window should have a start value less than or equal to 0, "
                "and a stop value greater than or equal to 0."
            )

    return CumulativeWindow(level, dense, window, partitioning)


def siblings(hierarchy: Hierarchy, *, exclude_self: bool = False) -> Scope:
    """Create a "siblings" aggregation scope.

    In a siblings scope, the value for the member of a given level in the hierarchy is computed by taking the contribution of all of the members on the same level (its siblings).

    A siblings aggregation is an appropriate tool for operations such as marginal aggregations (marginal VaR, marginal mean) for non-linear aggregation functions.

    Args:
        hierarchy: The hierarchy containing the levels along which the aggregation is performed.
        exclude_self: Whether to include the current member's contribution in its cumulative value.
    """
    return SiblingsWindow(
        hierarchy,
        exclude_self,
    )


def origin(*levels: Level) -> Scope:
    """Create an aggregation scope with an arbitrary number of levels.

    The passed levels define a boundary above and under which the aggregation is performed differently.
    When those levels are not expressed in a query, the measure will drill down until finding the value for all members of these levels, and then aggregate those values using the user-defined aggregation function.
    This allows to compute measures that show the yearly mean when looking at the grand total, but the sum of each month's value when looking at each year individually.

    Args:
        levels: The levels defining the dynamic aggregation domain.
    """
    if len(levels) == 1 and isinstance(levels[0], list):
        raise TypeError("origin takes one or more levels, not a list.")

    return LeafLevels(list(levels))
