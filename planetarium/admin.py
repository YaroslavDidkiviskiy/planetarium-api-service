from django.contrib import admin

from planetarium.models import ShowSession, AstronomyShow, ShowTheme, Ticket, PlanetariumDome, Reservation

admin.site.register(ShowSession)
admin.site.register(AstronomyShow)
admin.site.register(ShowTheme)
admin.site.register(Ticket)
admin.site.register(PlanetariumDome)
admin.site.register(Reservation)
