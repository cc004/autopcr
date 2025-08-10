#type: ignore
from typing import Callable, Iterator, Iterable, Dict, TypeVar, Generic, List, Set, Tuple, Any, Union
import functools

T = TypeVar('T', covariant = True)
T2 = TypeVar('T2')
T3 = TypeVar('T3')

class flow(Iterator[T], Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self.iterable: Iterator[T] = iter(iterable)
    
    def __next__(self) -> T:
        return next(self.iterable)
    
    def _select(self, func: Callable[[T], T2]) -> Iterator[T2]:
        for item in self.iterable:
            yield func(item)
    
    def select(self, func: Callable[[T], T2]) -> 'flow[T2]':
        return flow(self._select(func))
    
    def _where(self, func: Callable[[T], bool]) -> Iterator[T]:
        for item in self.iterable:
            if func(item):
                yield item
    
    def where(self, func: Callable[[T], bool]) -> 'flow[T]':
        return flow(self._where(func))
    
    def _concat(self, other: Iterable[T]) -> Iterator[T]:
        for item in self.iterable:
            yield item
        for item in other:
            yield item
    
    def concat(self, other: Iterable[T]) -> 'flow[T]':
        return flow(self._concat(other))
    
    def to_dict(self, key_func: Callable[[T], T2], value_func: Callable[[T], T3]) -> Dict[T2, T3]:
        return {key_func(item): value_func(item) for item in self.iterable}
    
    def to_list(self) -> List[T]:
        return list(self.iterable)
    
    def to_set(self) -> Set[T]:
        return set(self.iterable)
    
    def to_tuple(self) -> Tuple[T]:
        return tuple(self.iterable)

    def _group_by(self, key_func: Callable[[T], T2]) -> Iterator['groupflow[T, T2]']:
        groups: Dict[T2, List[T]] = {}
        for item in self.iterable:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        for key, value in groups.items():
            yield groupflow(value, key)

    def group_by(self, key_func: Callable[[T], T2]) -> 'flow[groupflow[T, T2]]':
        return flow(self._group_by(key_func))

    def max(self, func: Union[Callable[[T], Any], None] = None) -> T:
        if func is None:
            return max(self.iterable, default=None)
        return max(self.iterable, key=func, default=None)
    
    def min(self, func: Union[Callable[[T], Any], None] = None) -> T:
        if func is None:
            return min(self.iterable)
        return min(self.iterable, key=func)
    
    def sum(self, func: Callable[[T], T2] = lambda x: x, seed: T2 = 0) -> T2:
        return sum((func(item) for item in self.iterable), start=seed)
    
    def aggregate(self, seed: T2, func: Callable[[T2, T], T]) -> T2:
        return functools.reduce(func, self.iterable, seed)

    def _select_many(self, func: Callable[[T], Iterable[T2]]) -> Iterator[T2]:
        for item in self.iterable:
            for item2 in func(item):
                yield item2
    
    def select_many(self, func: Callable[[T], Iterable[T2]]) -> 'flow[T2]':
        return flow(self._select_many(func))
    
    def first(self, func: Union[Callable[[T], bool], None] = None) -> T:
        if func is None:
            return next(self.iterable)
        return next(self.where(func).iterable)

    def _take(self, count: int) -> Iterator[T]:
        for i, item in enumerate(self.iterable):
            if i < count:
                yield item
            else:
                break

    def take(self, count: int) -> 'flow[T]':
        return flow(self._take(count))

    def _zip(self, other: Iterable[T2]) -> Iterator[Tuple[T, T2]]:
        other_iter = iter(other)
        for item in self.iterable:
            yield (item, next(other_iter))
    
    def zip(self, other: Iterable[T2]) -> 'flow[Tuple[T, T2]]':
        return flow(self._zip(other))

    def count(self, func: Union[Callable[[T], bool], None] = None) -> int:
        if func is None:
            return sum(1 for _ in self.iterable)
        return sum(1 for item in self.iterable if func(item))

class groupflow(flow[T], Generic[T, T2]):
    def __init__(self, iterable: Iterable[T], key: T2):
        super().__init__(iterable)
        self.key: T2 = key
