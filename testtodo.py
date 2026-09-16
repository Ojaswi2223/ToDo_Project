"""
Tests for the plain-Python todo list.

Setup:
    pip install pytest

Run:
    pytest -v
"""

import pytest

from ToDo import Todo, TodoList


# ============================================================
#  FIXTURES
# ============================================================

@pytest.fixture
def todos():
    """A fresh, empty TodoList for each test."""
    return TodoList()


@pytest.fixture
def two_todos():
    """A TodoList pre-loaded with two todos, ids 1 and 2."""
    todos = TodoList()
    todos.add("Buy milk")
    todos.add("Walk dog")
    return todos


# ============================================================
#  PART 1 — the Todo class
# ============================================================

def test_new_todo_starts_incomplete():
    todo = Todo(1, "Buy milk")
    assert todo.completed is False


def test_todo_stores_its_fields():
    todo = Todo(7, "Buy milk", "semi-skimmed")
    assert todo.id == 7
    assert todo.title == "Buy milk"
    assert todo.description == "semi-skimmed"


def test_description_defaults_to_none():
    todo = Todo(1, "Buy milk")
    assert todo.description is None


def test_toggle_marks_complete():
    todo = Todo(1, "Buy milk")
    todo.toggle()
    assert todo.completed is True


def test_toggle_twice_returns_to_incomplete():
    todo = Todo(1, "Buy milk")
    todo.toggle()
    todo.toggle()
    assert todo.completed is False


def test_str_shows_empty_box_when_incomplete():
    todo = Todo(1, "Buy milk")
    assert str(todo) == "[ ] 1. Buy milk"


def test_str_shows_x_when_complete():
    todo = Todo(1, "Buy milk")
    todo.toggle()
    assert str(todo) == "[x] 1. Buy milk"


def test_str_uses_a_space_not_an_empty_string():
    """Both forms must be the same length so the list lines up."""
    incomplete = Todo(1, "Buy milk")
    complete = Todo(1, "Buy milk")
    complete.toggle()
    assert len(str(incomplete)) == len(str(complete))


# ============================================================
#  PART 2 — adding and listing
# ============================================================

def test_starts_empty(todos):
    assert todos.all() == []


def test_add_returns_the_new_todo(todos):
    todo = todos.add("Buy milk")
    assert isinstance(todo, Todo)
    assert todo.title == "Buy milk"


def test_add_stores_the_todo(todos):
    todos.add("Buy milk")
    assert len(todos.all()) == 1


def test_add_assigns_sequential_ids(todos):
    first = todos.add("Buy milk")
    second = todos.add("Walk dog")
    third = todos.add("Call mom")
    assert [first.id, second.id, third.id] == [1, 2, 3]


def test_first_id_is_one_not_zero(todos):
    assert todos.add("Buy milk").id == 1


def test_add_accepts_a_description(todos):
    todo = todos.add("Buy milk", "semi-skimmed")
    assert todo.description == "semi-skimmed"


def test_all_preserves_insertion_order(two_todos):
    titles = [todo.title for todo in two_todos.all()]
    assert titles == ["Buy milk", "Walk dog"]


def test_two_lists_have_independent_counters():
    """next_id is per-object, so unrelated lists both start at 1."""
    work = TodoList()
    personal = TodoList()
    work.add("Fix the bug")
    work.add("Write tests")
    assert personal.add("Buy milk").id == 1


# ============================================================
#  PART 3 — finding
# ============================================================

def test_find_returns_the_matching_todo(two_todos):
    assert two_todos.find(2).title == "Walk dog"


def test_find_returns_none_when_missing(two_todos):
    assert two_todos.find(999) is None


def test_find_on_empty_list_returns_none(todos):
    assert todos.find(1) is None


def test_find_checks_every_todo_not_just_the_first(todos):
    """Guards against `return None` being indented into the loop."""
    todos.add("First")
    todos.add("Second")
    todos.add("Third")
    assert todos.find(3).title == "Third"


def test_find_returns_the_same_object_not_a_copy(todos):
    """In-memory storage hands back references, so mutations stick."""
    original = todos.add("Buy milk")
    found = todos.find(1)
    assert found is original


def test_mutating_a_found_todo_affects_the_stored_one(todos):
    todos.add("Buy milk")
    todos.find(1).toggle()
    assert todos.find(1).completed is True


def test_find_rejects_a_string_id(two_todos):
    """"1" == 1 is False in Python, so a string id never matches."""
    assert two_todos.find("1") is None


# ============================================================
#  PART 4 — deleting
# ============================================================

def test_delete_removes_the_todo(todos):
    todos.add("Buy milk")
    todos.delete(1)
    assert todos.all() == []


def test_delete_returns_the_deleted_todo(todos):
    todos.add("Buy milk")
    assert todos.delete(1).title == "Buy milk"


def test_delete_returns_none_when_missing(todos):
    assert todos.delete(999) is None


def test_delete_on_empty_list_returns_none(todos):
    assert todos.delete(1) is None


def test_delete_leaves_other_todos_alone(two_todos):
    two_todos.delete(1)
    remaining = two_todos.all()
    assert len(remaining) == 1
    assert remaining[0].title == "Walk dog"


def test_deleted_todo_can_no_longer_be_found(todos):
    todos.add("Buy milk")
    todos.delete(1)
    assert todos.find(1) is None


def test_deleting_twice_returns_none_the_second_time(todos):
    todos.add("Buy milk")
    assert todos.delete(1) is not None
    assert todos.delete(1) is None


def test_ids_are_never_reused_after_delete(todos):
    """
    next_id only ever goes up, so id 2 is gone forever once deleted.
    Gaps are the price of ids that never collide.
    """
    todos.add("First")
    todos.add("Second")
    todos.delete(2)
    assert todos.add("Third").id == 3


# ============================================================
#  PART 5 — count_completed
# ============================================================

def test_count_completed_is_zero_initially(two_todos):
    assert two_todos.count_completed() == 0


def test_count_completed_counts_toggled_todos(two_todos):
    two_todos.find(1).toggle()
    assert two_todos.count_completed() == 1


def test_count_completed_ignores_untoggled(todos):
    todos.add("A")
    todos.add("B")
    todos.add("C")
    todos.find(1).toggle()
    todos.find(3).toggle()
    assert todos.count_completed() == 2


def test_count_completed_drops_when_toggled_back(two_todos):
    todo = two_todos.find(1)
    todo.toggle()
    todo.toggle()
    assert two_todos.count_completed() == 0


def test_count_completed_drops_when_a_done_todo_is_deleted(two_todos):
    two_todos.find(1).toggle()
    two_todos.delete(1)
    assert two_todos.count_completed() == 0


# ============================================================
#  PART 6 — a full workflow
# ============================================================

def test_full_lifecycle(todos):
    """Add three, complete one, delete another, check what's left."""
    todos.add("Buy milk")
    todos.add("Walk dog")
    todos.add("Call mom")

    todos.find(1).toggle()
    todos.delete(2)

    remaining = todos.all()
    assert len(remaining) == 2
    assert [t.id for t in remaining] == [1, 3]
    assert todos.count_completed() == 1
    assert str(remaining[0]) == "[x] 1. Buy milk"