"""Postgresql Quiz CLI."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Callable

import pgcli.main
from prompt_toolkit.shortcuts import message_dialog
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

postgres_lexer = get_lexer_by_name('postgres')
terminal256_formatter = get_formatter_by_name('terminal256')

FULL_PROMPT = """
\x1b[38;5;47;01m{title}\x1b[39;00m

{prompt}

This should return:

{output}
"""


@dataclass
class Quiz:
    """A quiz: questions for users to solve."""

    title: str
    description: str
    questions: list

    _expected_attached: bool = False
    _current_num: int = 0

    @property
    def question(self):
        return self.questions[self._current_num]

    @classmethod
    def load_from_json_file(cls, filepath: str) -> Quiz:
        """Get quiz from JSON file and return new instance."""

        return cls(**json.load(open(filepath)))

    def attach_expected(self, eval_fn: Callable) -> None:
        """Run quiz answers and get expected outcome."""

        for q in self.questions:
            output, query = eval_fn(' '.join(q['solution']))
            q['expected'] = output

        self._expected_attached = True

    def start(self) -> dict:
        """Start quiz: set first question, return title/description to display."""

        self._current_num = 0

        return dict(title=self.title,
                    description=self.description,
                    num_questions=len(self.questions))

    def verify_answer(self, output: List[str]) -> bool:
        """Compare student output to expected."""

        return output == self.question['expected']

    def full_prompt(self) -> str:
        """Return full prompt for this question, to display."""

        output = "    " + "\n    ".join(self.question['expected'])
        return FULL_PROMPT.format(
            title=self.question['title'],
            prompt=self.question['prompt'],
            output=output)

    def goto_next(self) -> str:
        """Go to next question."""

        if self._current_num < len(self.questions) - 1:
            self._current_num += 1
            return self.full_prompt()

        else:
            return "\nAll done! Congrats!"

    def solution(self) -> str:
        """Show complete answer."""

        # TODO: use pygments to colorize
        return "\n".join(self.question['solution'])


class QuizCli(pgcli.main.PGCli):
    def register_special_commands(self):
        """Hook for both our commands and quiz state, since this is called at init."""

        super().register_special_commands()

        self.pgspecial.register(
            self.quiz_show_prompt,
            "\\question",
            "\\question",
            "Show quiz question",
            arg_type=pgcli.main.NO_QUERY)

        self.pgspecial.register(
            self.quiz_next_question,
            "\\next",
            "\\next",
            "Move to next question",
            arg_type=pgcli.main.NO_QUERY)

        self.pgspecial.register(
            self.quiz_show_solution,
            "\\solution",
            "\\solution",
            "Show solution to problem",
            arg_type=pgcli.main.NO_QUERY)

        # noinspection PyAttributeOutsideInit
        self.quiz = Quiz.load_from_json_file("quiz.json")
        welcome = self.quiz.start()

        message_dialog(title=welcome['title'], text=welcome['description']).run()

    def _evaluate_command(self, text):
        """Hook into the PGCli query evaluation so we can check for correct output."""

        # noinspection PyProtectedMember
        if not self.quiz._expected_attached:
            # Just once, we have to get the expected output for each question and
            # put in on the quiz. There isn't a good, post-database-connection hook for
            # this, so we'll do it here once
            self.quiz.attach_expected(super()._evaluate_command)

        output, query = super()._evaluate_command(text)

        if self.quiz.verify_answer(output):
            message_dialog(title="Success!",
                           text="You can continue to the next question with \\next").run()
        return output, query

    def quiz_next_question(self, **_):
        """Move to next question (or message showing no more questions."""
        yield None, None, None, self.quiz.goto_next()

    def quiz_show_prompt(self, **_):
        """Show prompt to user."""
        yield None, None, None, self.quiz.full_prompt()

    def quiz_show_solution(self, **_):
        """Show answer."""
        yield None, None, None, highlight(
            self.quiz.solution(),
            postgres_lexer,
            terminal256_formatter)


if __name__ == '__main__':
    # PGCli is an awesome & well-developed project, but it doesn't have great hooks for
    # subclassing like this --- we'd need to override methods that have the REPL loop,
    # which would involve putting the REPL loop in our code. Joel has filed a PR with them
    # that decomposes the core REPL loop to be more easily extensible.

    # For now, we'll monkey-patch in our quiz as the one that their cli() function runs.
    # Dynamic languages FTW!
    origPGCli = pgcli.main.PGCli
    pgcli.main.PGCli = QuizCli
    pgcli.main.cli()
