"""
    habitipy_stale - cache calls to habitipy and execute them after
    command-line interface library using plumbum
    Copyright 2017 Pavel Pletenev <cpp.create@gmail.com>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""
# pylint: disable=missing-docstring,too-few-public-methods,arguments-differ
import json
from plumbum import local, cli
from habitipy.cli import ApplicationWithApi, TaskId
STALE_FILE = local.path('~/.config/habitipy/stale.json')
# still not merged into release tomerfiliba/plumbum#339
_, ngettext = cli.i18n.get_translation_functions(  # pylint: disable=no-member,invalid-name
    'habitipy_stale', names=('gettext', 'ngettext'))


class Stale(cli.Application):
    'cache calls to habitipy and execute them after'


@Stale.subcommand('add')
class StaleAdd(cli.Application):
    'add calls to habitipy to cache'
    def main(
            self,
            domain: cli.Set('habits', 'dailies', 'todos', case_sensitive=False),
            op: cli.Set('up', 'down', case_sensitive=False),
            *task_ids: TaskId):
        task_ids_list = []
        for tasks in task_ids:
            task_ids_list.extend(tasks)
        try:
            with open(STALE_FILE) as stale_file:
                stale = json.load(stale_file)
        except (OSError, json.JSONDecodeError):
            stale = {}
        if domain not in stale:
            stale[domain] = {}
        if op not in stale[domain]:
            stale[domain][op] = {}
        for task_id in task_ids_list:
            if task_id not in stale[domain][op]:
                stale[domain][op][task_id] = 0
            stale[domain][op][task_id] += 1
            print(
                _("Added '{task_id}' to {domain} with {op}").format(  # NOQA: Q000
                    task_id=task_id, domain=domain, op=op))
        with open(STALE_FILE, 'w') as stale_file:
            json.dump(stale, stale_file)


@Stale.subcommand('push')
class StalePush(ApplicationWithApi):
    'push all stale calls to server'
    def main(self):
        super().main()

        try:
            with open(STALE_FILE) as stale_file:
                stale = json.load(stale_file)
        except (OSError, json.JSONDecodeError):
            stale = {}
        for domain, directions in stale.items():  # pylint: disable=unused-variable
            for direction, tasks in directions.items():
                for task_id, number in tasks.items():
                    for i in range(1, number + 1):
                        self.api.tasks[task_id].score[direction].post()
                        print(ngettext(
                            "Pushed '{domain} {direction} {task_id}' {i} time",  # NOQA: Q000
                            "Pushed '{domain} {direction} {task_id}' {i} times",  # NOQA: Q000
                            i).format(**locals()))
        with open(STALE_FILE, 'w') as stale_file:
            json.dump({}, stale_file)
