"""Unit tests for timer_core.Timer (user stories US1-US6).

Each test docstring states the test method, purpose and expected result.
"""

import pytest

from timer_core import LONG_BREAK, SHORT_BREAK, WORK, Timer


@pytest.fixture
def timer():
    return Timer(work_minutes=25, break_minutes=5, long_break_minutes=15)


def finish_work(timer):
    timer.start()
    timer.tick(timer.remaining)


# US1 - Start the timer
def test_us1_ac1_start_sets_running(timer):
    """Method: Unit
    Purpose: start() starts the timer.
    Expected: running is True.
    """
    timer.start()
    assert timer.running is True


def test_us1_ac2_start_counts_down(timer):
    """Method: Unit
    Purpose: a started timer counts down.
    Expected: 1500 -> 1499 after 1s.
    """
    timer.start()
    timer.tick(1)
    assert timer.remaining == 25 * 60 - 1


# US2 - Pause the timer
def test_us2_ac1_pause_stops_running(timer):
    """Method: Unit
    Purpose: pause() stops the timer.
    Expected: running is False.
    """
    timer.start()
    timer.pause()
    assert timer.running is False


def test_us2_ac2_paused_timer_does_not_count(timer):
    """Method: Unit
    Purpose: time does not pass while paused.
    Expected: remaining unchanged.
    """
    timer.start()
    timer.tick(10)
    timer.pause()
    timer.tick(30)
    assert timer.remaining == 25 * 60 - 10


# US3 - Reset the timer
def test_us3_ac1_reset_restores_work_time(timer):
    """Method: Unit
    Purpose: reset() restores the full work time.
    Expected: 1500, stopped.
    """
    timer.start()
    timer.tick(100)
    timer.reset()
    assert timer.remaining == 25 * 60
    assert timer.running is False


def test_us3_ac2_reset_clears_progress(timer):
    """Method: Unit
    Purpose: reset() clears mode and counter.
    Expected: mode work, 0 done.
    """
    finish_work(timer)
    timer.reset()
    assert timer.mode == WORK
    assert timer.completed == 0


# US4 - Automatic switch to break
def test_us4_ac1_work_end_switches_to_break(timer):
    """Method: Unit
    Purpose: work end starts a break.
    Expected: mode is short_break.
    """
    finish_work(timer)
    assert timer.mode == SHORT_BREAK


def test_us4_ac2_break_has_break_duration(timer):
    """Method: Unit
    Purpose: break uses break length.
    Expected: remaining is 300 seconds.
    """
    finish_work(timer)
    assert timer.remaining == 5 * 60


# US5 - Count completed pomodoros
def test_us5_ac1_completed_increases_after_work(timer):
    """Method: Unit
    Purpose: a finished work phase is counted.
    Expected: completed is 1.
    """
    finish_work(timer)
    assert timer.completed == 1


def test_us5_ac2_break_end_does_not_count(timer):
    """Method: Unit
    Purpose: a finished break is not counted.
    Expected: completed stays 1.
    """
    finish_work(timer)
    timer.tick(timer.remaining)
    assert timer.completed == 1
    assert timer.mode == WORK


# US6 - Long break after every 4 pomodoros
def test_us6_ac1_fourth_round_gives_long_break(timer):
    """Method: Unit
    Purpose: 4th pomodoro starts a long break.
    Expected: long_break, 900s.
    """
    for _ in range(3):
        finish_work(timer)
        timer.tick(timer.remaining)
    finish_work(timer)
    assert timer.mode == LONG_BREAK
    assert timer.remaining == 15 * 60


def test_us6_ac2_third_round_gives_short_break(timer):
    """Method: Unit
    Purpose: BVA just below 4 rounds.
    Expected: 3rd round is short_break.
    """
    for _ in range(2):
        finish_work(timer)
        timer.tick(timer.remaining)
    finish_work(timer)
    assert timer.completed == 3
    assert timer.mode == SHORT_BREAK
