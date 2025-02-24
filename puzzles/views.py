from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from guardian.decorators import permission_required_or_403

from hunts.models import Hunt
from puzzles.models import Puzzle


@login_required(login_url="/")
@permission_required_or_403("hunt_access", (Hunt, "puzzles", "puzzle_pk"))
def redirect_to_sheet(request, puzzle_pk):
    try:
        puzzle = Puzzle.objects.select_related("hunt__settings").get(pk=puzzle_pk)
    except ObjectDoesNotExist:
        messages.error(
            request, f"Puzzle ID {puzzle_pk} does not exist, cannot redirect."
        )
        return redirect("/")

    if puzzle.sheet:
        return HttpResponseRedirect(puzzle.sheet)
    else:

        messages.error(
            request,
            f"Sheets does not exist yet for {puzzle.name}.\n"
            f"Please wait a few minutes. If you have been waiting for a while, please ping @{puzzle.hunt.settings.discord_devs_role}",
        )
        return redirect("/", {"hunt_pk": puzzle.hunt.pk})
