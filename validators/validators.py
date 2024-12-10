from datetime import datetime

from messages.date_time_messages import bad_format_for_date, bad_format_for_time, time_start_before_time_and
from messages.participant_messages import participants_must_be_correct, participants_not_correct


class ValidationError(Exception):
    """Custom exception for easy handling of validation error."""
    pass


def validate_date(date_text: str) -> datetime:
    """
    Checks that the date is entered in the format DD.MM.YYYY.
    """
    try:
        return datetime.strptime(date_text, "%d.%m.%Y")
    except ValueError:
        raise ValidationError(bad_format_for_date)


def validate_time_range(time_text: str) -> tuple[datetime.time, datetime.time]:
    """
    Checks that the time range is entered in HH:MM - HH:MM format.
    Returns the start and as time object.
    """
    try:
        if "-" not in time_text:
            raise ValidationError(bad_format_for_time)

        start_time, end_time = [t.strip() for t in time_text.split("-")]
        start_time_obj = datetime.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()

        if start_time_obj >= end_time_obj:
            raise ValidationError(time_start_before_time_and)

        return start_time_obj, end_time_obj
    except ValueError:
        raise ValidationError(bad_format_for_time)


def validate_participants(participants_text: str) -> int:
    """
    Checks that the number of participants is a positive integer.
    """
    try:
        participants = int(participants_text)
        if participants <= 0:
            raise ValidationError(participants_must_be_correct)
        return participants
    except ValueError:
        raise ValidationError(participants_not_correct)
