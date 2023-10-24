from django.shortcuts import render
from .forms import InputValueInventary


def main_inventory(request):
    search_window = InputValueInventary()

    return render(request, 'inventory.html', {'form': search_window})
